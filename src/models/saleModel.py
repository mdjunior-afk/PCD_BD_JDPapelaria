from src.database import get_connection

def getSale(data={}):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.IDPedido,
            p.DataPedido,
            p.Status,
            p.ValorTotal,
            pes.Nome AS Cliente
        FROM Pedido p
        LEFT JOIN Pessoa pes ON pes.IDPessoa = p.IDPessoa
        WHERE p.DataPedido BETWEEN ? AND ?
    """

    params = [data["data_inicio"], data["data_fim"]]

    if "cliente" in data and data["cliente"]:
        query += " AND p.IDPessoa = ?"
        params.append(data["cliente"])

    query += " ORDER BY p.DataPedido DESC;"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return rows


def addSale(data={}):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO Pedido (IDPessoa, DataPedido, Status, ValorTotal)
        VALUES (?, ?, ?, 0)
    """, (data["cliente"], data["data"], data["status"]))

    id_pedido = cursor.lastrowid

    total = 0

    for item in data["itens"]:
        subtotal = item["qtd"] * item["preco"]
        total += subtotal

        cursor.execute("""
            INSERT INTO ItemPedido (IDPedido, IDProdutoServico, Quantidade, PrecoUnitario, SubTotal)
            VALUES (?, ?, ?, ?, ?)
        """, (id_pedido, item["id_prodserv"], item["qtd"], item["preco"], subtotal))

    cursor.execute("UPDATE Pedido SET ValorTotal = ? WHERE IDPedido = ?", (total, id_pedido))

    for p in data["pagamentos"]:
        cursor.execute("""
            INSERT INTO Pagamento (IDPedido, IDFormaPagamento, Valor, DataPagamento, NumeroParcelas)
            VALUES (?, ?, ?, ?, ?)
        """, (id_pedido, p["forma"], p["valor"], data["data"], p["parcelas"]))

    conn.commit()
    conn.close()

    return id_pedido


def editSale(id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Pedido
        SET IDPessoa = ?, DataPedido = ?, Status = ?
        WHERE IDPedido = ?
    """, (data["cliente"], data["data"], data["status"], id))

    cursor.execute("DELETE FROM ItemPedido WHERE IDPedido = ?", (id,))
    
    total = 0
    for item in data["itens"]:
        subtotal = item["qtd"] * item["preco"]
        total += subtotal
        
        cursor.execute("""
            INSERT INTO ItemPedido (IDPedido, IDProdutoServico, Quantidade, PrecoUnitario, SubTotal)
            VALUES (?, ?, ?, ?, ?)
        """, (id, item["id_prodserv"], item["qtd"], item["preco"], subtotal))

    cursor.execute("UPDATE Pedido SET ValorTotal = ? WHERE IDPedido = ?", (total, id))

    cursor.execute("DELETE FROM Pagamento WHERE IDPedido = ?", (id,))
    
    for p in data["pagamentos"]:
        cursor.execute("""
            INSERT INTO Pagamento (IDPedido, IDFormaPagamento, Valor, DataPagamento, NumeroParcelas)
            VALUES (?, ?, ?, ?, ?)
        """, (id, p["forma"], p["valor"], data["data"], p["parcelas"]))

    conn.commit()
    conn.close()


def removeSale(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Pedido WHERE IDPedido = ?", (id,))

    conn.commit()
    conn.close()
