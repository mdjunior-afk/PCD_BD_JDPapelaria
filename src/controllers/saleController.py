from src.database import get_connection

def getSale(data={}):
    # Recuperar N vendas pela intervalo de datas
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.close()

    return cursor.fetchall()

def addSale(data={}):
    # Adicionar uma venda levando em consideração todos os produtos e pagamentos dela
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()

def editSale(id, data):
    # Editar alguma venda de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()

def removeSale(id):
    # Remover uma venda de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()