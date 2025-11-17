from database import get_connection

def getPerson(data={}):
    # Recuperar N pessoas pelo CPF/CNPJ ou Nome, levando em consideração o tipo dela
    conn = get_connection()
    cursor = conn.cursor()

    query = ""

    cursor.execute(query)

    conn.close()

    return cursor.fetchall()

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