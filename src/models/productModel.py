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
            ProdutoServico.IDProdutoServico, ProdutoServico.Nome, Produto.EstoqueMinimo, Produto.EstoqueAtual, 
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

        if "fornecedores" in data:
            fornece_query = "INSERT INTO Fornece(IDPessoa, DataCompra, ValorTotal) VALUES (?, ?, ?)"
            cursor.execute(fornece_query, (data["id_pessoa"], data["fornecedores"]["data_compra"], data["fornecedores"]["valor_total"]))

            fornece_id = cursor.lastrowid

            fornecimento_query = "INSERT INTO ItemFornecido(IDFornece, IDProduto, Quantidade, PrecoUnitario, DataValidade) VALUES (?, ?, ?, ?, ?)"

            for forn in data["fornecedores"]["fornecedores"]:
                cursor.execute(fornecimento_query, (fornece_id, id_produto_servico, forn["quantidade"], forn["valor"], forn["data_validade"]))

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

    # 1. Update na tabela ProdutoServico (usa o 'id' direto)
    query_servico = "UPDATE ProdutoServico SET Nome = ? WHERE IDProdutoServico = ?"
    cursor.execute(query_servico, (data["nome"], id))

    # 2. Obtém o ID da tabela Produto (chave primária/secundária)
    product_id = getProductID(id)[0]

    if product_id is None:
        # Se não encontrar o produto, faz um rollback e encerra a operação
        conn.rollback()
        conn.close()
        print(f"Erro: ProdutoServico ID {id} não tem um registro correspondente em Produto.")
        return

    # 3. Update na tabela Produto (usa o 'product_id' obtido)
    query_produto = """
    UPDATE Produto 
    SET 
        IDMarca = ?, IDCategoria = ?, CodBarra = ?, PrecoCompra = ?, Reajuste = ?, 
        PrecoVenda = ?, EstoqueMinimo = ?, EstoqueAtual = ? 
    WHERE IDProduto = ?
    """

    params_produto = (
        data["id_marca"], data["id_categoria"], data["cod_barra"], data["preco_compra"], 
        data["reajuste"], data["preco_venda"], data["estoque_minimo"], 
        data["estoque_atual"], product_id,
    )

    cursor.execute(query_produto, params_produto) 

    conn.commit()
    conn.close()

def getProductID(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT Produto.IDProduto FROM Produto INNER JOIN ProdutoServico ON ProdutoServico.IDProdutoServico = Produto.IDProdutoServico WHERE ProdutoServico.IDProdutoServico = ?"

    cursor.execute(query, (id, ))

    return cursor.fetchone()

def removeProduct(id):
    # Remover um produto de ID=id, caso o produto existe em alguma venda. Não poderá ser excluido
    conn = get_connection()
    cursor = conn.cursor()

    product_id = getProductID(id)[0]

    print(id, product_id)

    query = "DELETE FROM Produto WHERE IDProduto = ?"

    cursor.execute(query, (product_id, ))

    query = "DELETE FROM ProdutoServico WHERE IDProdutoServico = ?"

    cursor.execute(query, (id, ))

    conn.commit()
    conn.close()

def getCategories(name=''):
    conn = get_connection()
    cursor = conn.cursor()

    termo_pesquisa = f"%{name}%"

    # 1. Ajuste a query para incluir a contagem de produtos
    # Usamos LEFT JOIN para incluir marcas que não têm produtos (contagem = 0)
    base_query = """
    SELECT 
        C.IDCategoria, 
        C.Nome, 
        COUNT(P.IDProduto) AS QuantidadeProdutos
    FROM 
        Categoria C
    LEFT JOIN 
        Produto P ON C.IDCategoria = P.IDCategoria
    """

    if name == '':
        query = f"{base_query} GROUP BY C.IDCategoria, C.Nome ORDER BY C.Nome"
        cursor.execute(query)
    else:
        # 2. Adicione a cláusula WHERE para filtragem segura
        query = f"{base_query} WHERE C.Nome LIKE ? GROUP BY C.IDCategoria, C.Nome ORDER BY C.Nome"
        # Mantenha a forma segura de passar o parâmetro de filtro
        cursor.execute(query, (termo_pesquisa, ))

    # Boas práticas: o fetchall() deve vir após o cursor ser fechado
    results = cursor.fetchall()

    conn.close() # Sempre feche a conexão
    return results

def getBrands(name=''):
    conn = get_connection()
    cursor = conn.cursor()

    termo_pesquisa = f"%{name}%"

    # 1. Ajuste a query para incluir a contagem de produtos
    # Usamos LEFT JOIN para incluir marcas que não têm produtos (contagem = 0)
    base_query = """
    SELECT 
        M.IDMarca, 
        M.Nome, 
        COUNT(P.IDProduto) AS QuantidadeProdutos
    FROM 
        Marca M
    LEFT JOIN 
        Produto P ON M.IDMarca = P.IDMarca
    """

    if name == '':
        query = f"{base_query} GROUP BY M.IDMarca, M.Nome ORDER BY M.Nome"
        cursor.execute(query)
    else:
        # 2. Adicione a cláusula WHERE para filtragem segura
        query = f"{base_query} WHERE M.Nome LIKE ? GROUP BY M.IDMarca, M.Nome ORDER BY M.Nome"
        # Mantenha a forma segura de passar o parâmetro de filtro
        cursor.execute(query, (termo_pesquisa, ))

    # Boas práticas: o fetchall() deve vir após o cursor ser fechado
    results = cursor.fetchall()

    conn.close() # Sempre feche a conexão
    return results

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

def addCategory(name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Categoria(Nome) VALUES (?)"

    cursor.execute(query, (name, ))

    conn.commit()
    conn.close()

def updateCategory(id, name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Categoria SET Nome = ? WHERE IDCategoria = ?"

    cursor.execute(query, (name, id, ))

    conn.commit()
    conn.close()

def removeCategory(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM Categoria WHERE IDCategoria = ?"

    cursor.execute(query, (id, ))

    conn.commit()
    conn.close()

def addBrand(name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Marca(Nome) VALUES (?)"

    cursor.execute(query, (name, ))

    conn.commit()
    conn.close()

def updateBrand(id, name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Marca SET Nome = ? WHERE IDMarca = ?"

    cursor.execute(query, (name, id, ))

    conn.commit()
    conn.close()

def removeBrand(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM Marca WHERE IDMarca = ?"

    cursor.execute(query, (id, ))

    conn.commit()
    conn.close()