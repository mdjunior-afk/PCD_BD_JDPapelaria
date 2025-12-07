from src.database import get_connection

from PySide6.QtCore import QDate

def getPaymentsMethods(name):
    conn = get_connection()
    cursor = conn.cursor()

    termo_pesquisa = f"%{name}%"

    # 1. Ajuste a query para incluir a contagem de produtos
    # Usamos LEFT JOIN para incluir marcas que não têm produtos (contagem = 0)
    base_query = """
    SELECT 
        IDFormaPagamento, 
        Nome
    FROM 
        FormaPagamento
    """

    if name == '':
        query = f"{base_query} GROUP BY IDFormaPagamento, Nome ORDER BY Nome"
        cursor.execute(query)
    else:
        # 2. Adicione a cláusula WHERE para filtragem segura
        query = f"{base_query} WHERE Nome LIKE ? GROUP BY IDFormaPagamento, Nome ORDER BY Nome"
        # Mantenha a forma segura de passar o parâmetro de filtro
        cursor.execute(query, (termo_pesquisa, ))

    # Boas práticas: o fetchall() deve vir após o cursor ser fechado
    results = cursor.fetchall()

    conn.close() # Sempre feche a conexão
    return results

def addPaymenthMethod(name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO FormaPagamento(Nome) VALUES (?)"

    cursor.execute(query, (name, ))

    conn.commit()
    conn.close()

def updatePaymentMethods(id, name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE FormaPagamento SET Nome = ? WHERE IDFormaPagamento = ?"

    cursor.execute(query, (name, id, ))

    conn.commit()
    conn.close()

def removePaymentMethods(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM FormaPagamento WHERE IDFormaPagamento = ?"

    cursor.execute(query, (id, ))

    conn.commit()
    conn.close()

# SERVICO
def getServices(name):
    conn = get_connection()
    cursor = conn.cursor()

    termo_pesquisa = f"%{name}%"

    # 1. Ajuste a query para incluir a contagem de produtos
    # Usamos LEFT JOIN para incluir marcas que não têm produtos (contagem = 0)
    base_query = """
    SELECT 
        ProdutoServico.IDProdutoServico, 
        ProdutoServico.Nome,
        Servico.Preco,
        Servico.Descricao
    FROM 
        ProdutoServico
    INNER JOIN
        Servico ON Servico.IDProdutoServico = ProdutoServico.IDProdutoServico
    WHERE
        ProdutoServico.Tipagem = 'Servico'
    """

    if name == '':
        query = f"{base_query} GROUP BY ProdutoServico.IDProdutoServico, ProdutoServico.Nome ORDER BY ProdutoServico.Nome"
        cursor.execute(query)
    else:
        # 2. Adicione a cláusula WHERE para filtragem segura
        query = f"{base_query} WHERE ProdutoServico.Nome LIKE ? GROUP BY ProdutoServico.IDProdutoServico, ProdutoServico.Nome ORDER BY ProdutoServico.Nome"
        # Mantenha a forma segura de passar o parâmetro de filtro
        cursor.execute(query, (termo_pesquisa, ))

    # Boas práticas: o fetchall() deve vir após o cursor ser fechado
    results = cursor.fetchall()

    conn.close() # Sempre feche a conexão
    return results

def addService(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO ProdutoServico(Nome, Tipagem) VALUES (?, 'Servico')"

    cursor.execute(query, (data["name"], ))

    id_produto_servico = cursor.lastrowid

    query = "INSERT INTO Servico(IDProdutoServico, Preco, Descricao) VALUES (?, ?, ?)"

    cursor.execute(query, (id_produto_servico, data["price"], data["description"], ))

    conn.commit()
    conn.close()

def updateService(id, data):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE ProdutoServico SET Nome = ? WHERE IDProdutoServico = ?"

    cursor.execute(query, (data["name"], id, ))

    query = "UPDATE Servico SET Descricao = ?, Preco = ? WHERE IDProdutoServico = ?"

    cursor.execute(query, (data["description"], data["price"], id, ))

    conn.commit()
    conn.close()

def removeService(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM Servico WHERE IDProdutoServico = ?"
    
    cursor.execute(query, (id, ))

    query = "DELETE FROM ProdutoServico WHERE IDProdutoServico = ?"
    
    cursor.execute(query, (id, ))

    conn.commit()
    conn.close()

def getLowerStocks():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT COUNT(EstoqueAtual) FROM Produto WHERE EstoqueAtual < EstoqueMinimo"

    cursor.execute(query)

    return cursor.fetchone()

def getAnniversaries():
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT
    COUNT(T1.Nome)
    FROM Pessoa AS T1
    JOIN PessoaFisica AS T2 ON T1.IDPessoa = T2.IDPessoa
    WHERE strftime('%m', T2.DataNascimento) = strftime('%m', 'now');
    """

    cursor.execute(query)

    return cursor.fetchone()

def getTodaySale():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
    SUM(T1.ValorTotal) as ValorTotalDia,
    T1.DataPedido
    FROM Pedido AS T1
    WHERE T1.DataPedido = ?
    GROUP BY T1.DataPedido;
    """

    cursor.execute(query, (QDate.currentDate().toString('yyyy-MM-dd'), ))

    return cursor.fetchone()
