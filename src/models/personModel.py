from src.database import get_connection

import sqlite3

import sqlite3 # Importação adicionada para que o 'except' funcione

def getPersonID(name):
    # Remover uma pessoa de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT IDPessoa FROM Pessoa WHERE Nome LIKE ?"

    cursor.execute(query, (f"%{name}%", ))

    person = cursor.fetchone()

    conn.close()

    return person

def getPerson(data={}):
    conn = get_connection() # Assumindo que esta função está definida
    cursor = conn.cursor()
    
    # Prepara o termo de pesquisa de nome (para uso em LIKE)
    termo_pesquisa = f"%{data.get('pesquisa', '')}%"
    args = []

    # Se 'id_pessoa' não está presente, a intenção é LISTAR (agregação é necessária)
    is_listing = "id_pessoa" not in data
    
    # 1. Base da Query: SELECT e FROM/JOINs
    # Note que a seleção de campos muda. Vamos definir ambos os SELECTs.

    if is_listing:
        # Query para LISTAGEM (com GROUP_CONCAT para agregar contatos e endereços)
        select_fields = """
            DISTINCT Pessoa.IDPessoa, Pessoa.Nome, Pessoa.Cliente, PessoaFisica.CPF, PessoaJuridica.CNPJ, 
            PessoaJuridica.Fornecedor, PessoaFisica.Sexo, PessoaFisica.DataNascimento, 
            PessoaJuridica.RazaoSocial, 
            group_concat(DISTINCT Contato.Valor) AS ContatoValor,
            CONCAT_WS(' ', Endereco.Logradouro, Endereco.Numero, Endereco.Complemento, 
            Endereco.Bairro, Endereco.Cidade, Endereco.Estado, Endereco.CEP) AS EnderecoCompleto
        """
    else:
        # Query para BUSCA por ID (retorna apenas dados da pessoa, sem duplicatas)
        select_fields = """
            DISTINCT Pessoa.IDPessoa, Pessoa.Nome, Pessoa.Cliente, PessoaFisica.CPF, PessoaJuridica.CNPJ, 
            PessoaJuridica.Fornecedor, PessoaFisica.Sexo, PessoaFisica.DataNascimento, 
            PessoaJuridica.RazaoSocial
        """

    query = f"""
        SELECT {select_fields}
        FROM Pessoa
        LEFT JOIN PessoaFisica ON Pessoa.IDPessoa = PessoaFisica.IDPessoa
        LEFT JOIN PessoaJuridica ON Pessoa.IDPessoa = PessoaJuridica.IDPessoa
        LEFT JOIN Contato ON Contato.IDPessoa = Pessoa.IDPessoa
        LEFT JOIN Endereco ON Endereco.IDPessoa = Pessoa.IDPessoa
    """

    # 2. Cláusula WHERE
    if "id_pessoa" in data:
        query += " WHERE Pessoa.IDPessoa = ?"
        args.append(data["id_pessoa"])
    elif "pesquisa" in data and data["pesquisa"]:
        query += " WHERE Pessoa.Nome LIKE ?"
        args.append(termo_pesquisa)
    
    # 3. Cláusulas GROUP BY e ORDER BY
    if is_listing:
        # Lista de campos que NÃO são agregados
        group_fields = """
            Pessoa.IDPessoa, Pessoa.Nome, Pessoa.Cliente, PessoaFisica.CPF, PessoaJuridica.CNPJ, 
            PessoaJuridica.Fornecedor, PessoaFisica.Sexo, PessoaFisica.DataNascimento, 
            PessoaJuridica.RazaoSocial, EnderecoCompleto
        """
        query += f" GROUP BY {group_fields} ORDER BY Pessoa.Nome"
    else:
        # Ao buscar por ID com DISTINCT, não precisa de GROUP BY
        query += " ORDER BY Pessoa.Nome" 


    try:
        cursor.execute(query, tuple(args))
        
        people_data = cursor.fetchall()
        
        return people_data

    except sqlite3.Error as e:
        print(f"Erro ao buscar pessoa: {e}")
        return []

    finally:
        if conn:
            conn.close()

def addPerson(data={}):
    # 1. Conexão e Início da Transação
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Obter flags de Cliente/Fornecedor (Assumindo que foram passadas para 'data')
        is_client = data.get("is_client", False)
        is_supplier = data.get("is_supplier", False)
        
        cliente_flag = 1 if is_client else 0
        fornecedor_flag = 1 if is_supplier else 0
        
        # --- 2. Inserir na tabela base Pessoa ---
        query_pessoa = """
        INSERT INTO Pessoa (Nome, Cliente) 
        VALUES (?, ?);
        """
        cursor.execute(query_pessoa, (
            data.get("nome"), 
            cliente_flag, 
        ))
        
        # Obter o ID da pessoa recém-inserida (importante para os dados relacionados)
        id_pessoa = cursor.lastrowid

        # --- 3. Inserir em PessoaFisica ou PessoaJuridica ---
        if data.get("type") == "Pessoa física":
            # Remove formatação do CPF para armazenamento
            cpf_limpo = data.get("document")
            
            
            query_pf = """
            INSERT INTO PessoaFisica (IDPessoa, CPF, Sexo, DataNascimento) 
            VALUES (?, ?, ?, ?);
            """
            cursor.execute(query_pf, (
                id_pessoa, 
                cpf_limpo, 
                data.get("sex"),
                data.get("birthday")
            ))
            
        elif data.get("type") == "Pessoa jurídica":
            # Remove formatação do CNPJ para armazenamento
            cnpj_limpo = data.get("document", "")
            
            query_pj = """
            INSERT INTO PessoaJuridica (IDPessoa, CNPJ, RazaoSocial, Fornecedor) 
            VALUES (?, ?, ?, ?);
            """
            cursor.execute(query_pj, (
                id_pessoa, 
                cnpj_limpo, 
                data.get("fantasy_name", ""),
                fornecedor_flag
            ))
            
        # --- 4. Inserir Endereços ---
        if "address" in data and data["address"]:
            query_endereco = """
            INSERT INTO Endereco (IDPessoa, CEP, Logradouro, Numero, Bairro, Cidade, Estado, Complemento) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            for addr in data["address"]:
                cursor.execute(query_endereco, (
                    id_pessoa,
                    addr.get("cep", "").replace('-', ''), # Remove formatação do CEP
                    addr.get("logradouro"),
                    addr.get("numero"),
                    addr.get("bairro"),
                    addr.get("cidade"),
                    addr.get("estado"),
                    addr.get("complemento")
                ))

        # --- 5. Inserir Contatos ---
        if "contact" in data and data["contact"]:
            query_contato = """
            INSERT INTO Contato (IDPessoa, Tipo, Valor) 
            VALUES (?, ?, ?);
            """
            for contact in data["contact"]:
                cursor.execute(query_contato, (
                    id_pessoa,
                    contact.get("tipo"),
                    contact.get("valor")
                ))

        # 6. Commit (Confirmação) da Transação
        conn.commit()
        return id_pessoa # Retorna o ID da pessoa inserida

    except sqlite3.Error as e:
        # Rollback em caso de erro
        conn.rollback()
        print(f"Erro ao adicionar pessoa: {e}")
        return None

    finally:
        if conn:
            conn.close()

def editPerson(id, data):
    # Editar algum dado da pessoa de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Pessoa SET Nome = ?, Cliente = ? WHERE IDPessoa = ?"

    cursor.execute(query, (data["nome"], data["is_client"], id, ))

    if data["type"] == "Pessoa física":
        # Converte birthday para formato SQLite (YYYY-MM-DD)
        birthday = data.get("birthday")
        if hasattr(birthday, 'toString'):
            birthday = birthday.toString('yyyy-MM-dd')
        
        query = "UPDATE PessoaFisica SET CPF = ?, Sexo = ?, DataNascimento = ? WHERE IDPessoa = ?"
        cursor.execute(query, (data["document"], data["sex"], birthday, id, ))
    else:
        query = "UPDATE PessoaJuridica SET CNPJ = ?, RazaoSocial = ?, Fornecedor = ? WHERE IDPessoa = ?"
        cursor.execute(query, (data["document"], data["fantasy_name"], data["is_supplier"], id, ))

    for address in data["address"]:
        query = "UPDATE Endereco SET Logradouro = ?, Numero = ?, Complemento = ?, Bairro = ?, Cidade = ?, Estado = ?, CEP = ? WHERE IDPessoa = ?"
        cursor.execute(query, (address["logradouro"], address["numero"], address["complemento"], address["bairro"], address["cidade"], address["estado"], address["cep"], id, )),
    
    for contact in data["contact"]:
        query = "UPDATE Contato SET Tipo = ?, Valor = ? WHERE IDPessoa = ?"
        cursor.execute(query, (contact["tipo"], contact["valor"], id, ))

    conn.commit()
    conn.close()

def removePerson(id):
    """
    Remove uma pessoa do banco de dados (ID=id), incluindo seus dados 
    relacionados (PessoaFisica/Juridica, Endereco, Contato).
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # A ordem das exclusões é importante, mas aqui não há dependência circular.
        # Excluímos dos dados relacionados primeiro:
        
        # 1. Excluir Contatos
        query_contato = "DELETE FROM Contato WHERE IDPessoa = ?"
        cursor.execute(query_contato, (id,))

        # 2. Excluir Endereços
        query_endereco = "DELETE FROM Endereco WHERE IDPessoa = ?"
        cursor.execute(query_endereco, (id,))

        # 3. Excluir dados específicos (Física e/ou Jurídica)
        # O SQLite deve permitir a exclusão de ambas, mesmo que apenas uma exista.
        query_pf = "DELETE FROM PessoaFisica WHERE IDPessoa = ?"
        cursor.execute(query_pf, (id,))
        
        query_pj = "DELETE FROM PessoaJuridica WHERE IDPessoa = ?"
        cursor.execute(query_pj, (id,))

        # 4. Excluir a Pessoa principal
        query_pessoa = "DELETE FROM Pessoa WHERE IDPessoa = ?"
        cursor.execute(query_pessoa, (id,))

        conn.commit()
        return True
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erro ao remover pessoa e dados relacionados: {e}")
        return False

    finally:
        if conn:
            conn.close()

def getAllAddress(id):
    # Remover uma pessoa de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Endereco WHERE IDPessoa = ?"

    cursor.execute(query, (id, ))

    address = cursor.fetchall()

    conn.close()

    return address

def getAllContacts(id):
    # Remover uma pessoa de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Contato WHERE IDPessoa = ?"

    cursor.execute(query, (id, ))

    contacts = cursor.fetchall()

    conn.close()

    return contacts

def getSuppliers(data):
    conn = get_connection()
    cursor = conn.cursor()

    # Prepara o termo de pesquisa, garantindo que a chave exista e o valor seja tratado
    termo_pesquisa = f"%{data.get('pesquisa', '')}%"
    
    # Se você quiser retornar o CNPJ junto com o Nome, adicione-o no SELECT
    query = """
    SELECT 
        Pessoa.Nome
    FROM 
        Pessoa 
    INNER JOIN 
        PessoaJuridica ON PessoaJuridica.IDPessoa = Pessoa.IDPessoa 
    WHERE 
        PessoaJuridica.Fornecedor = 1 AND Pessoa.Nome LIKE ?
    """
    
    try:
        cursor.execute(query, (termo_pesquisa,))
        
        results = cursor.fetchall()
        
        # --- Formatação dos resultados em lista de dicionários ---
        suppliers_list = []
        
        # Itera sobre as tuplas retornadas (ex: ('Nome da Empresa',))
        for row in results:
            # Pega o primeiro (e único) elemento da tupla, que é o Nome
            nome_fornecedor = row[0]
            
            # Cria o dicionário no formato desejado
            suppliers_list.append({"nome": nome_fornecedor})
            
        return suppliers_list

    except sqlite3.Error as e:
        print(f"Erro ao buscar fornecedores: {e}")
        return []

    finally:
        if conn:
            conn.close()
