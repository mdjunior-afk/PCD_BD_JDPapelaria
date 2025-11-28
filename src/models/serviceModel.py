from src.database import get_connection

def getService(data={}):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            s.IDServico,
            ps.Nome,
            s.Descricao,
            s.Preco
        FROM Servico s
        JOIN ProdutoServico ps ON ps.IDProdutoServico = s.IDProdutoServico
        WHERE 1=1
    """

    params = []

    if "nome" in data and data["nome"]:
        query += " AND ps.Nome LIKE ?"
        params.append(f"%{data['nome']}%")

    if "descricao" in data and data["descricao"]:
        query += " AND s.Descricao LIKE ?"
        params.append(f"%{data['descricao']}%")

    if "preco_min" in data:
        query += " AND s.Preco >= ?"
        params.append(data["preco_min"])

    if "preco_max" in data:
        query += " AND s.Preco <= ?"
        params.append(data["preco_max"])

    query += " ORDER BY ps.Nome;"

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results


def addService(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO ProdutoServico (Nome, Tipagem) VALUES (?, 'servico');"
    cursor.execute(query, (data["nome"],))
    id_prodserv = cursor.lastrowid

    query = """
        INSERT INTO Servico (IDProdutoServico, Descricao, Preco)
        VALUES (?, ?, ?);
    """
    cursor.execute(query, (
        id_prodserv,
        data["descricao"],
        data["preco"]
    ))

    conn.commit()
    conn.close()


def editService(id_servico, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT IDProdutoServico FROM Servico WHERE IDServico = ?", (id_servico,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False  

    id_prodserv = row[0]

    query = "UPDATE ProdutoServico SET Nome = ? WHERE IDProdutoServico = ?;"
    cursor.execute(query, (data["nome"], id_prodserv))

    query = """
        UPDATE Servico
        SET Descricao = ?, Preco = ?
        WHERE IDServico = ?;
    """
    cursor.execute(query, (
        data["descricao"],
        data["preco"],
        id_servico
    ))

    conn.commit()
    conn.close()
    return True


def removeService(id_servico):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT IDProdutoServico FROM Servico WHERE IDServico = ?", (id_servico,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    id_prodserv = row[0]

    cursor.execute("DELETE FROM Servico WHERE IDServico = ?", (id_servico,))

    cursor.execute("DELETE FROM ProdutoServico WHERE IDProdutoServico = ?", (id_prodserv,))

    conn.commit()
    conn.close()
    return True
