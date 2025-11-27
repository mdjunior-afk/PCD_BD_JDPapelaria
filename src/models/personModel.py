from src.database import get_connection

def getPerson(data={}):
    conn = get_connection()
    cursor = conn.cursor()
    
    tipo = data["tipo"]
    termo_pesquisa = f"%{data.get('pesquisa', '')}%"

    args = [termo_pesquisa]


    query = """
    SELECT
        Pessoa.IDPessoa,
        Pessoa.Nome,
        -- CNPJ e CPF (ou outros dados específicos) virão como NULL para o tipo oposto de pessoa
        PessoaJuridica.CNPJ, 
        PessoaFisica.CPF, -- Adicionando CPF para vermos quem é PF
        Contato.Valor AS Contato, 
        Endereco.Logradouro, 
        Endereco.Numero, 
        Endereco.Cidade, 
        Endereco.Estado
    FROM
        Pessoa
    -- LEFT JOIN para dados opcionais (Pessoa Física)
    LEFT JOIN 
        PessoaFisica ON Pessoa.IDPessoa = PessoaFisica.IDPessoa
    -- LEFT JOIN para dados opcionais (Pessoa Jurídica)
    LEFT JOIN 
        PessoaJuridica ON Pessoa.IDPessoa = PessoaJuridica.IDPessoa
    -- INNER JOIN para dados obrigatórios (Toda pessoa deve ter Contato e Endereço)
    INNER JOIN 
        Endereco ON Endereco.IDPessoa = Pessoa.IDPessoa
    INNER JOIN
        Contato ON Contato.IDPessoa = Pessoa.IDPessoa
    WHERE
        Pessoa.Nome LIKE ? 
    """

    if tipo == "Cliente":
        query += " AND Pessoa.Cliente = 1"
    elif tipo == "Fornecedor":
        query += " AND PessoaJuridica.Fornecedor = 1"
        
    try:
        cursor.execute(query, tuple(args))
        
        products = cursor.fetchall()
        return products

    except sqlite3.Error as e:
        print(f"Erro ao buscar produtos: {e}")
        return []

    finally:
        if conn:
            conn.close()

def addPerson(data={}):
    # Adicionar os dados de uma pessoa usando as informações de data
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
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