from src.database import get_connection

import sqlite3

from datetime import datetime

def getEditSale(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        Pedido.IDPedido, Pedido.DataPedido, Pessoa.Nome, Pedido.ValorTotal, ProdutoServico.Nome, ItemPedido.PrecoUnitario, ItemPedido.Quantidade, ItemPedido.SubTotal
    FROM
        Pedido
    INNER JOIN
        ItemPedido ON ItemPedido.IDPedido = Pedido.IDPedido
    INNER JOIN
        ProdutoServico ON ProdutoServico.IDProdutoServico = ItemPedido.IDProdutoServico
    INNER JOIN
        Pessoa ON Pessoa.IDPessoa = Pedido.IDPessoa
    WHERE
        Pedido.IDPedido = ?
    """

    cursor.execute(query, (id, ))

    return cursor.fetchall()

def getSale(data={}):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Trata os termos de pesquisa
    start_date_str = data["data_inicio"]
    end_date_str = data["data_final"]

    start_date_obj = datetime.strptime(start_date_str, '%d/%m/%Y')
    end_date_obj = datetime.strptime(end_date_str, '%d/%m/%Y')

    # 3. Formata para o padrão SQL YYYY-MM-DD
    start_date_sql = start_date_obj.strftime('%Y-%m-%d')  # Resultado: '2025-11-27'
    end_date_sql = end_date_obj.strftime('%Y-%m-%d')

    query = """
    SELECT
        P.IDPedido, 
        P.DataPedido,
        Pe.Nome AS NomeCliente, 
        P.ValorTotal, 
        PS.Nome AS NomeItem,
        IP.PrecoUnitario, 
        IP.Quantidade, 
        IP.SubTotal,
        (
            SELECT GROUP_CONCAT(DISTINCT FormaPagamento.Nome)
            FROM Pagamento
            INNER JOIN FormaPagamento ON FormaPagamento.IDFormaPagamento = Pagamento.IDFormaPagamento
            WHERE Pagamento.IDPedido = P.IDPedido
        ) AS FormasPagamento
    FROM
        Pedido AS P
    INNER JOIN Pessoa AS Pe ON Pe.IDPessoa = P.IDPessoa
    INNER JOIN ItemPedido AS IP ON IP.IDPedido = P.IDPedido
    INNER JOIN ProdutoServico AS PS ON PS.IDProdutoServico = IP.IDProdutoServico
    WHERE
        PS.Tipagem = 'Produto' AND P.DataPedido BETWEEN ? AND ?
    GROUP BY P.IDPedido
    """
    
    args = [start_date_sql, end_date_sql]

    try:
        cursor.execute(query, tuple(args))
        
        sales = cursor.fetchall()
        print(sales)
        return sales

    except sqlite3.Error as e:
        print(f"Erro ao buscar produtos: {e}")
        return []

    finally:
        if conn:
            conn.close()

def addSale(data={}):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Preparação dos dados e data atual

        id_pessoa = getPersonID(data["cliente"])
        if id_pessoa:
            id_pessoa = id_pessoa[0]
        else:
            id_pessoa = 1

        valor_total = data.get("valor_total", 0.0)
        itens = data.get("itens", [])
        pagamentos = data.get("pagamentos", [])
        
        # Obter a data atual no formato SQL 'YYYY-MM-DD'
        data_pedido = datetime.now().strftime('%Y-%m-%d')

        if not id_pessoa or not itens:
            raise ValueError("ID da Pessoa e Itens são obrigatórios para registrar uma venda.")

        # --- 2. Inserir na tabela Pedido (Venda principal) ---
        if "id_pedido" not in data:
            query_pedido = """
            INSERT INTO Pedido (IDPessoa, DataPedido, ValorTotal) 
            VALUES (?, ?, ?);
            """

            cursor.execute(query_pedido, (
                id_pessoa, 
                data_pedido, 
                valor_total
            ))
        else:
            query_pedido = """
            INSERT INTO Pedido (IDPedido, IDPessoa, DataPedido, ValorTotal) 
            VALUES (?, ?, ?, ?);
            """ 
            cursor.execute(query_pedido, (
                data["id_pedido"],
                id_pessoa, 
                data_pedido, 
                valor_total
            ))
        
        # Obter o ID do pedido recém-inserido
        id_pedido = cursor.lastrowid
        if not id_pedido:
            raise sqlite3.Error("Falha ao obter o ID do Pedido inserido.")

        # --- 3. Inserir na tabela ItemPedido ---
        query_item_pedido = """
        INSERT INTO ItemPedido (IDPedido, IDProdutoServico, Quantidade, PrecoUnitario, Subtotal) 
        VALUES (?, ?, ?, ?, ?);
        """

        query_estoque = "UPDATE Produto SET EstoqueAtual = ? WHERE Produto.IDProdutoServico = ?"
        for item in itens:
            item_id = getProductID(item["nome"])
            cursor.execute(query_item_pedido, (
                id_pedido, 
                item_id, 
                item.get("quantidade"), 
                item.get("preco"),
                item.get("subtotal")
            ))

            new_stock = getProductStock(item_id) - int(item["quantidade"])
            if new_stock < 0:
                new_stock = 0
                
            cursor.execute(query_estoque, (new_stock, item_id))

        # --- 4. Inserir na tabela Pagamento ---
        query_pagamento = """
        INSERT INTO Pagamento (IDPedido, IDFormaPagamento, Valor) 
        VALUES (?, ?, ?);
        """
        for pagamento in pagamentos:
            cursor.execute(query_pagamento, (
                id_pedido, 
                getFormaDePagamentoID(pagamento["forma_pagamento"])[0],
                pagamento.get("valor")
            ))



        # --- 5. Commit da Transação ---
        conn.commit()
        return id_pedido # Retorna o ID da venda inserida

    except sqlite3.Error as e:
        # Rollback em caso de erro no DB
        conn.rollback()
        print(f"Erro ao adicionar venda (Pedido): {e}")
        return None
    
    except ValueError as e:
        # Rollback em caso de dados inválidos
        conn.rollback()
        print(f"Erro de validação: {e}")
        return None

    finally:
        if conn:
            conn.close()

def getAllPaymentMethods():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT Nome FROM FormaPagamento"

    cursor.execute(query)

    return cursor.fetchall()

def removeSale(id):
    # Remover um produto de ID=id, caso o produto existe em alguma venda. Não poderá ser excluido
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM ItemPedido WHERE IDPedido = ?"

    cursor.execute(query, (id, ))

    query = "DELETE FROM Pedido WHERE IDPedido = ?"

    cursor.execute(query, (id, ))

    query = "DELETE FROM Pagamento WHERE IDPedido = ?"

    cursor.execute(query, (id, ))

    conn.commit()
    conn.close()

def getPersonID(name):
    # Remover uma venda de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT IDPessoa FROM Pessoa WHERE Pessoa.Nome = ?"

    cursor.execute(query, (name, ))

    return cursor.fetchone()

def getProductID(name):
    # Remover uma venda de ID=id
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT IDProdutoServico FROM ProdutoServico WHERE ProdutoServico.Nome = ?"

    cursor.execute(query, (name, ))

    return cursor.fetchone()[0]

def getProductStock(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT Produto.EstoqueAtual FROM Produto WHERE Produto.IDProdutoServico = ?"

    cursor.execute(query, (id, ))

    return cursor.fetchone()[0]

def getFormaDePagamentoID(name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT FormaPagamento.IDFormaPagamento FROM FormaPagamento WHERE FormaPagamento.Nome = ?"

    cursor.execute(query, (name, ))

    return cursor.fetchone()

def getSalePayments(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        Pagamento.Valor, FormaPagamento.Nome
    FROM
        Pagamento
    INNER JOIN
        FormaPagamento ON FormaPagamento.IDFormaPagamento = Pagamento.IDFormaPagamento
    INNER JOIN
        Pedido ON Pedido.IDPedido = Pagamento.IDPedido
    WHERE Pedido.IDPedido = ?
    """

    cursor.execute(query, (id, ))

    return cursor.fetchall()