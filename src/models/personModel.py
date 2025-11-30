from src.database import get_connection

import sqlite3

def getPerson(data={}):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Prepara o termo de pesquisa de nome (se for o caso)
    termo_pesquisa = f"%{data.get('pesquisa', '')}%"
    
    # A lista de argumentos é iniciada vazia e preenchida dinamicamente
    args = []

    query = """
    SELECT
        Pessoa.IDPessoa,
        Pessoa.Nome,
        Pessoa.Cliente,
        PessoaFisica.CPF,
        PessoaJuridica.CNPJ,
        PessoaJuridica.Fornecedor,
        PessoaFisica.Sexo,
        PessoaFisica.DataNascimento,
        -- Tabela de Contatos (Precisa de JOIN para buscar todos, mas o SELECT é simplificado aqui)
        Contato.Tipo AS ContatoTipo,
        Contato.Valor AS ContatoValor,
        -- Tabela de Endereços (Precisa de JOIN para buscar todos)
        Endereco.CEP,
        Endereco.Logradouro, 
        Endereco.Numero, 
        Endereco.Bairro, 
        Endereco.Cidade, 
        Endereco.Estado,
        Endereco.Complemento
    FROM
        Pessoa
    LEFT JOIN 
        PessoaFisica ON Pessoa.IDPessoa = PessoaFisica.IDPessoa
    LEFT JOIN 
        PessoaJuridica ON Pessoa.IDPessoa = PessoaJuridica.IDPessoa
    -- LEFT JOIN para Contato e Endereço, para não eliminar pessoas que ainda não têm esses dados
    LEFT JOIN 
        Contato ON Contato.IDPessoa = Pessoa.IDPessoa
    LEFT JOIN 
        Endereco ON Endereco.IDPessoa = Pessoa.IDPessoa
    """

    # --- Lógica da Cláusula WHERE ---
    
    # 1. Busca por IDPessoa (Usada para carregar uma pessoa para edição)
    if "id_pessoa" in data and data["id_pessoa"]:
        query += " WHERE Pessoa.IDPessoa = ?"
        args.append(data["id_pessoa"])
        
    # 2. Busca por Termo de Pesquisa no Nome (Usada na aba de pesquisa geral)
    elif "pesquisa" in data and data["pesquisa"]:
        query += " WHERE Pessoa.Nome LIKE ?"
        args.append(termo_pesquisa)
        
    # 3. Filtro Adicional de Tipo (Se for necessário, a depender do seu Front-end)
    # Exemplo:
    # if data.get("tipo") == "Pessoa jurídica":
    #     query += " AND PessoaJuridica.CNPJ IS NOT NULL"
    # elif data.get("tipo") == "Pessoa física":
    #     query += " AND PessoaFisica.CPF IS NOT NULL"


    try:
        # Nota: Como você está usando LEFT JOIN em Contato/Endereco, 
        # a query pode retornar múltiplas linhas para a mesma pessoa (uma para cada Contato/Endereco).
        # Você precisará tratar isso no Python para agrupar os dados corretamente.
        cursor.execute(query, tuple(args))
        
        people_data = cursor.fetchall()
        
        # O processamento para agrupar múltiplos contatos/endereços
        # DEVE ser feito aqui ou no Controller (PersonController)
        
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

            print(cpf_limpo)
            
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
            cnpj_limpo = data.get("document", "").replace('.', '').replace('/', '').replace('-', '')
            
            query_pj = """
            INSERT INTO PessoaJuridica (IDPessoa, CNPJ, NomeFantasia, Fornecedor) 
            VALUES (?, ?, ?);
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
                    contact.get("contato")
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

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()

def removePerson(id):
    # Remover uma pessoa de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()