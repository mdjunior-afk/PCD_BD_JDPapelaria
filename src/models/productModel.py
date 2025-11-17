from src.database import get_connection

def getProduct(data={}):
    # Recuperar N produtos pelo Código, Nome. Cód. barra levando em consideração a categoria dela
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.close()

    return cursor.fetchall()

def addProduct(data={}):
    # Adicionar os dados de um produto usando as informações de data
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()

def editProduct(id, data):
    # Editar algum dado de produto de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()

def removeProduct(id):
    # Remover um produto de ID=id, caso o produto existe em alguma venda. Não poderá ser excluido
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()