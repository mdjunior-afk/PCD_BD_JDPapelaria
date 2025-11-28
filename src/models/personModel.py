from database import get_connection

def getPerson(nome, tipo_pessoa="todos"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.IDPessoa,
            p.Nome,
            p.Cliente,
            pf.CPF,
            pf.Sexo,
            pf.DataNascimento,
            pj.CNPJ,
            pj.RazaoSocial,
            pj.Fornecedor
        FROM Pessoa p
        LEFT JOIN PessoaFisica pf ON pf.IDPessoa = p.IDPessoa
        LEFT JOIN PessoaJuridica pj ON pj.IDPessoa = p.IDPessoa
        WHERE p.Nome LIKE ?
    """

    params = [f"%{nome}%"]

    if tipo_pessoa == "cliente":
        query += " AND p.Cliente = 1"
    elif tipo_pessoa == "fornecedor":
        query += " AND pj.Fornecedor = 1"

    query += " ORDER BY p.Nome;"

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results



def addPerson(data={}):
    conn = get_connection()
    cursor = conn.cursor()

    
    query = "INSERT INTO Pessoa(Nome, Cliente) VALUES (?, ?);"
    cursor.execute(query, (data["nome"], data["cliente"]))
    id_pessoa = cursor.lastrowid

 
    if data["tipo_pessoa"] == "Pessoa física":
        query = """
            INSERT INTO PessoaFisica(CPF, IDPessoa, Sexo, DataNascimento)
            VALUES (?, ?, ?, ?);
        """
        cursor.execute(query, (
            data["cpf"],
            id_pessoa,
            data["sexo"],
            data["datanascimento"]
        ))
    else:
        query = """
            INSERT INTO PessoaJuridica(CNPJ, IDPessoa, RazaoSocial, Fornecedor)
            VALUES (?, ?, ?, ?);
        """
        cursor.execute(query, (
            data["cnpj"],
            id_pessoa,
            data["razaosocial"],
            data["fornecedor"]
        ))

    if "enderecos" in data:
        for end in data["enderecos"]:
            query = """
                INSERT INTO Endereco
                (IDPessoa, Logradouro, Numero, Complemento, Bairro, Cidade, Estado, CEP)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(query, (
                id_pessoa,
                end.get("logradouro"),
                end.get("numero"),
                end.get("complemento"),
                end.get("bairro"),
                end.get("cidade"),
                end.get("estado"),
                end.get("cep")
            ))

    if "contatos" in data:
        for c in data["contatos"]:
            query = """
                INSERT INTO Contato (IDPessoa, Tipo, Valor)
                VALUES (?, ?, ?);
            """
            cursor.execute(query, (
                id_pessoa,
                c.get("tipo"),
                c.get("valor")
            ))

    conn.commit()
    conn.close()




def editPerson(id_pessoa, data):
    conn = get_connection()
    cursor = conn.cursor()

    # 1) Atualizar tabela Pessoa
    query = "UPDATE Pessoa SET Nome = ?, Cliente = ? WHERE IDPessoa = ?;"
    cursor.execute(query, (
        data["nome"],
        data["cliente"],
        id_pessoa
    ))

    cursor.execute("SELECT CPF FROM PessoaFisica WHERE IDPessoa = ?", (id_pessoa,))
    pf = cursor.fetchone()

    if pf:  
        query = """
            UPDATE PessoaFisica
            SET CPF = ?, Sexo = ?, DataNascimento = ?
            WHERE IDPessoa = ?;
        """
        cursor.execute(query, (
            data["cpf"],
            data["sexo"],
            data["datanascimento"],
            id_pessoa
        ))
    else:
        query = """
            UPDATE PessoaJuridica
            SET CNPJ = ?, RazaoSocial = ?, Fornecedor = ?
            WHERE IDPessoa = ?;
        """
        cursor.execute(query, (
            data["cnpj"],
            data["razaosocial"],
            data["fornecedor"],
            id_pessoa
        ))

    cursor.execute("DELETE FROM Endereco WHERE IDPessoa = ?;", (id_pessoa,))

    if "enderecos" in data:
        for end in data["enderecos"]:
            query = """
                INSERT INTO Endereco
                (IDPessoa, Logradouro, Numero, Complemento, Bairro, Cidade, Estado, CEP)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(query, (
                id_pessoa,
                end.get("logradouro"),
                end.get("numero"),
                end.get("complemento"),
                end.get("bairro"),
                end.get("cidade"),
                end.get("estado"),
                end.get("cep")
            ))

    cursor.execute("DELETE FROM Contato WHERE IDPessoa = ?;", (id_pessoa,))

    if "contatos" in data:
        for c in data["contatos"]:
            query = """
                INSERT INTO Contato (IDPessoa, Tipo, Valor)
                VALUES (?, ?, ?);
            """
            cursor.execute(query, (
                id_pessoa,
                c.get("tipo"),
                c.get("valor")
            ))

    conn.commit()
    conn.close()




def removePerson(id_pessoa):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM Pessoa WHERE IDPessoa = ?;"
    cursor.execute(query, (id_pessoa,))

    conn.commit()
    conn.close()
