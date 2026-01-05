from src.database import get_connection
from src.controllers.productController import ProductController

from PySide6.QtCore import QDate

from datetime import datetime

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
    COUNT(T1.Nome) AS total_aniversariantes
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

def getProductID(name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT IDProduto FROM Produto JOIN ProdutoServico ON Produto.IDProdutoServico = ProdutoServico.IDProdutoServico WHERE ProdutoServico.Nome = ?"

    cursor.execute(query, (name, ))

    return cursor.fetchone()

def getEntries(data):
    conn = get_connection()
    cursor = conn.cursor()

    start_date_obj = datetime.strptime(data["initial_date"], '%d/%m/%Y')
    end_date_obj = datetime.strptime(data["final_date"], '%d/%m/%Y')

    # 3. Formata para o padrão SQL YYYY-MM-DD
    start_date_sql = start_date_obj.strftime('%Y-%m-%d')  # Resultado: '2025-11-27'
    end_date_sql = end_date_obj.strftime('%Y-%m-%d')

    query = """
    SELECT 
        Fornece.IDFornece,
        Fornece.DataCompra,
        Pessoa.Nome,
        Fornece.ValorTotal
    FROM 
        Fornece
    INNER JOIN 
        Pessoa ON Fornece.IDPessoa = Pessoa.IDPessoa
    WHERE
        Fornece.DataCompra BETWEEN ? AND ?
    ORDER BY 
        Fornece.DataCompra DESC
    """

    cursor.execute(query, (start_date_sql, end_date_sql, ))

    results = cursor.fetchall()

    conn.close()

    return results

def getEntryByID(entry_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        Pessoa.Nome,
        ProdutoServico.Nome,
        ItemFornecido.Quantidade,
        ItemFornecido.PrecoUnitario,
        ItemFornecido.DataValidade,
        Fornece.IDFornece
    FROM 
        Fornece
    INNER JOIN 
        Pessoa ON Fornece.IDPessoa = Pessoa.IDPessoa
    INNER JOIN
        ItemFornecido ON ItemFornecido.IDFornece = Fornece.IDFornece
    INNER JOIN
        Produto ON ItemFornecido.IDProduto = Produto.IDProduto
    INNER JOIN
        ProdutoServico ON Produto.IDProdutoServico = ProdutoServico.IDProdutoServico
    WHERE
        Fornece.IDFornece = ?
    """

    cursor.execute(query, (entry_id,))

    result = cursor.fetchall()

    conn.close()

    return result

def addEntry(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO 
        Fornece(IDPessoa, DataCompra, ValorTotal)
    VALUES 
        (?, ?, ?)
    """

    cursor.execute(query, (data["fornecedor"], data["data"], data["valor_total"], ))

    query = """
    INSERT INTO
        ItemFornecido(IDFornece, IDProduto, Quantidade, PrecoUnitario, DataValidade)
    VALUES
        (?, ?, ?, ?, ?)
    """

    update_query = """
    UPDATE 
        Produto 
    SET 
        EstoqueAtual = EstoqueAtual + ?, 
        PrecoCompra = ?, 
        PrecoVenda = PrecoCompra + (PrecoCompra * Reajuste) 
    WHERE 
        IDProduto = ?
    """

    for item in data["itens"]:
        product_id = getProductID(item["nome"])[0]

        cursor.execute(query, (
            cursor.lastrowid,
            product_id,
            item["quantidade"],
            item["preco_compra"],
            item["data_validade"]
        ))

        cursor.execute(update_query, (
            item["quantidade"],
            item["preco_compra"],
            product_id
        ))

    conn.commit()
    conn.close()

def editEntry(entry_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE 
        Fornece
    SET 
        IDPessoa = ?, 
        ValorTotal = ?
    WHERE 
        IDFornece = ?
    """

    cursor.execute(query, (data["fornecedor"], data["valor_total"], entry_id, ))

    # Primeiro, precisamos reverter o estoque dos itens antigos
    select_query = """
    SELECT 
        IDProduto, Quantidade
    FROM 
        ItemFornecido
    WHERE 
        IDFornece = ?
    """

    cursor.execute(select_query, (entry_id, ))
    old_items = cursor.fetchall()

    update_stock_query = """
    UPDATE
        Produto
    SET
        EstoqueAtual = EstoqueAtual - ?
    WHERE
        IDProduto = ?
    """

    for item in old_items:
        cursor.execute(update_stock_query, (item[1], item[0], ))

    # Agora, removemos os itens antigos
    delete_items_query = "DELETE FROM ItemFornecido WHERE IDFornece = ?"
    cursor.execute(delete_items_query, (entry_id, ))

    # Agora, adicionamos os novos itens e atualizamos o estoque
    insert_item_query = """
    INSERT INTO
        ItemFornecido(IDFornece, IDProduto, Quantidade, PrecoUnitario, DataValidade)
    VALUES  
        (?, ?, ?, ?, ?)
    """

    update_stock_query = """
    UPDATE 
        Produto
    SET
        EstoqueAtual = EstoqueAtual + ?, 
        PrecoCompra = ?, 
        PrecoVenda = PrecoCompra + (PrecoCompra * Reajuste)
    WHERE 
        IDProduto = ?
    """

    for item in data["itens"]:
        product_id = getProductID(item["nome"])[0]

        cursor.execute(insert_item_query, (
            entry_id,
            product_id,
            item["quantidade"],
            item["preco_compra"],
            item["data_validade"]
        ))

        cursor.execute(update_stock_query, (
            item["quantidade"],
            item["preco_compra"],
            product_id
        ))
    
    conn.commit()
    conn.close()
