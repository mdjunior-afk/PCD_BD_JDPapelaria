from src.database import get_connection

def getService(data={}):
    # Recuperar N serviços pelo intervalo de datas
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.close()

    return cursor.fetchall()

def addService(data={}):
    # Adicionar um serviço levando em consideração todos os serviços prestados e pagamentos dele
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()

def editService(id, data):
    # Editar algum dado do serviço de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()

def removeService(id):
    # Remover um serviço de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.commit()
    conn.close()