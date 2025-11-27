from src.database import get_connection

import sqlite3

def getProduct(data={}):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Trata os termos de pesquisa
    termo_pesquisa = f"%{data.get('pesquisa', '')}%"
    categoria_selecionada = data.get('categoria', 'Todos') # Assume 'Todos' se não estiver definido
    
    # 2. Query base (sem WHERE)
    query = """
        SELECT 
            ProdutoServico.IDProdutoServico, ProdutoServico.Nome, Produto.EstoqueAtual, 
            Produto.PrecoCompra, Produto.Reajuste, Produto.PrecoVenda, Marca.Nome AS Marca, 
            Categoria.Nome AS Categoria, Produto.CodBarra 
        FROM 
            Produto 
        INNER JOIN 
            ProdutoServico ON Produto.IDProdutoServico = ProdutoServico.IDProdutoServico 
        INNER JOIN 
            Categoria ON Produto.IDCategoria = Categoria.IDCategoria 
        INNER JOIN 
            Marca ON Produto.IDMarca = Marca.IDMarca
    """
    
    args = []

    if "id_produto" not in data:
        query += " WHERE ProdutoServico.Nome LIKE ?"
        args.append(termo_pesquisa)

        if categoria_selecionada != "Todos":
            query += " AND Categoria.Nome = ?"
            args.append(categoria_selecionada)
    else:
        query += "WHERE ProdutoServico.IDProdutoServico = ?"
        args.append(data["id_produto"])
    
    try:
        cursor.execute(query, tuple(args))
        
        products = cursor.fetchall()
        return products

    except sqlite3.Error as e:
        print(f"Erro ao buscar produtos: {e}")
        return []

    finally:
        if conn:
            conn.close()

def addProduct(data={}):
    conn = get_connection()
    cursor = conn.cursor()

    # --- 1. INSERIR NA TABELA PAI (ProdutoServico) ---
    query_prodservico = "INSERT INTO ProdutoServico(Nome, Tipagem) VALUES (?, 'Produto')"
    
    try:
        # Correção: Passar o argumento como uma tupla (data['nome'],)
        cursor.execute(query_prodservico, (data['nome'],))
        
        # 2. OBTER O ID RECÉM-CRIADO
        id_produto_servico = cursor.lastrowid
        
        data["id_categoria"] = getCategoryID(data["id_categoria"])[0]
        data["id_marca"] = getBrandID(data["id_marca"])[0]

        print(data["id_categoria"], data["id_marca"])

        # Verificação (opcional):
        if not id_produto_servico:
             raise Exception("Falha ao obter IDProdutoServico.")

        # --- 3. INSERIR NA TABELA FILHA (Produto) ---
        query_produto = """
        INSERT INTO 
            Produto(IDProdutoServico, IDCategoria, IDMarca, EstoqueMinimo, EstoqueAtual, CodBarra, PrecoCompra, Reajuste, PrecoVenda)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Cria a tupla de argumentos para a segunda query
        args_produto = (
            id_produto_servico,          # <--- ID OBTIDO
            data['id_categoria'],
            data['id_marca'],
            data['estoque_minimo'],
            data['estoque_atual'],
            data['cod_barra'],
            data['preco_compra'],
            data['reajuste'],
            data['preco_venda']
        )
        
        cursor.execute(query_produto, args_produto)
        
        # 4. Comitar e Fechar (dentro do bloco try/finally para segurança)
        conn.commit()
        return id_produto_servico

    except sqlite3.Error as e:
        print(f"Erro ao adicionar produto: {e}")
        conn.rollback() # Desfaz as operações em caso de erro
        return None

    finally:
        if conn:
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

def getCategories():
    # Remover um produto de ID=id, caso o produto existe em alguma venda. Não poderá ser excluido
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT Nome FROM Categoria"

    cursor.execute(query)

    return cursor.fetchall()

def getBrands():
    # Remover um produto de ID=id, caso o produto existe em alguma venda. Não poderá ser excluido
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT Nome FROM Marca"

    cursor.execute(query)

    return cursor.fetchall()

def getCategoryID(name):
    # Remover um produto de ID=id, caso o produto existe em alguma venda. Não poderá ser excluido
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT IDCategoria FROM Categoria WHERE Nome = ?"

    cursor.execute(query, (name, ))

    return cursor.fetchone()

def getBrandID(name):
    # Remover um produto de ID=id, caso o produto existe em alguma venda. Não poderá ser excluido
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT IDMarca FROM Marca WHERE Nome = ?"

    cursor.execute(query, (name, ))

    return cursor.fetchone()