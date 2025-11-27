from src.database import get_connection

import sqlite3

from datetime import datetime

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
        Pedido.IDPedido,
        Pedido.DataPedido,
        Pessoa.Nome AS NomeCliente,
        Pedido.ValorTotal,
        GROUP_CONCAT(DISTINCT FormaPagamento.Nome) AS FormasPagamento
    FROM
        Pedido
    INNER JOIN Pessoa ON Pessoa.IDPessoa = Pedido.IDPessoa
    INNER JOIN Pagamento ON Pagamento.IDPedido = Pedido.IDPedido
    INNER JOIN FormaPagamento ON Pagamento.IDFormaPagamento = FormaPagamento.IDFormaPagamento
    WHERE
        (Pedido.DataPedido BETWEEN ? AND ?)
        AND Pedido.IDPedido IN (
            SELECT IP.IDPedido
            FROM ItemPedido AS IP
            INNER JOIN ProdutoServico AS PS ON PS.IDProdutoServico = IP.IDProdutoServico
            WHERE PS.Tipagem = 'Produto'
        )
    GROUP BY
        Pedido.IDPedido
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