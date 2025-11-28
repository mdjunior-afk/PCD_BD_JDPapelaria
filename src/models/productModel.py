from src.database import get_connection

def getProduct(filters={}):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            pr.IDProduto,
            ps.Nome AS NomeProduto,
            m.Nome AS Marca,
            c.Nome AS Categoria,
            pr.CodBarra,
            pr.PrecoCompra,
            pr.PrecoVenda,
            pr.Reajuste,
            pr.EstoqueMinimo,
            pr.EstoqueAtual
        FROM Produto pr
        INNER JOIN ProdutoServico ps ON ps.IDProdutoServico = pr.IDProdutoServico
        LEFT JOIN Marca m ON m.IDMarca = pr.IDMarca
        LEFT JOIN Categoria c ON c.IDCategoria = pr.IDCategoria
        WHERE 1=1
    """

    params = []

    if "nome" in filters and filters["nome"]:
        query += " AND ps.Nome LIKE ?"
        params.append(f"%{filters['nome']}%")

    if "codbarra" in filters and filters["codbarra"]:
        query += " AND pr.CodBarra LIKE ?"
        params.append(f"%{filters['codbarra']}%")

    if "categoria" in filters and filters["categoria"]:
        query += " AND c.IDCategoria = ?"
        params.append(filters["categoria"])

    if "marca" in filters and filters["marca"]:
        query += " AND m.IDMarca = ?"
        params.append(filters["marca"])

    query += " ORDER BY ps.Nome;"

    cursor.execute(query, params)
    results = cursor.fetchall()

    
    full_products = []
    for r in results:
        produtos_dict = {
            "IDProduto": r[0],
            "Nome": r[1],
            "Marca": r[2],
            "Categoria": r[3],
            "CodBarra": r[4],
            "PrecoCompra": r[5],
            "PrecoVenda": r[6],
            "Reajuste": r[7],
            "EstoqueMinimo": r[8],
            "EstoqueAtual": r[9],
            "Fornecedores": getProductSuppliers(r[0])
        }
        full_products.append(produtos_dict)

    conn.close()
    return full_products


def getProductSuppliers(idProduto):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            pj.CNPJ,
            pj.RazaoSocial,
            i.DataValidade,
            i.PrecoUnitario
        FROM ItemFornecido i
        INNER JOIN Fornece f ON f.IDFornece = i.IDFornece
        INNER JOIN PessoaJuridica pj ON pj.IDPessoa = f.IDPessoa
        WHERE i.IDProduto = ?
        ORDER BY i.DataValidade DESC;
    """

    cursor.execute(query, (idProduto,))
    res = cursor.fetchall()
    conn.close()

    fornecedores = []
    for f in res:
        fornecedores.append({
            "CNPJ": f[0],
            "RazaoSocial": f[1],
            "DataValidade": f[2],
            "PrecoCompra": f[3]
        })

    return fornecedores


def addProduct(data={}):
    conn = get_connection()
    cursor = conn.cursor()

    
    cursor.execute("""
        INSERT INTO ProdutoServico (Nome, Tipagem)
        VALUES (?, 'produto')
    """, (data["nome"],))

    id_ps = cursor.lastrowid

    cursor.execute("""
        INSERT INTO Produto 
            (IDProdutoServico, IDCategoria, IDMarca, EstoqueMinimo, EstoqueAtual, 
             CodBarra, PrecoCompra, PrecoVenda, Reajuste)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_ps,
        data.get("categoria"),
        data.get("marca"),
        data.get("estoque_minimo", 0),
        data.get("estoque_atual", 0),
        data["codbarra"],
        data.get("preco_compra", 0),
        data.get("preco_venda", 0),
        data.get("reajuste", 0)
    ))

    conn.commit()
    conn.close()


def editProduct(id, data):
    conn = get_connection()
    cursor = conn.cursor()

    
    cursor.execute("""
        UPDATE ProdutoServico
        SET Nome = ?
        WHERE IDProdutoServico = (SELECT IDProdutoServico FROM Produto WHERE IDProduto = ?)
    """, (data["nome"], id))

    
    cursor.execute("""
        UPDATE Produto
        SET IDCategoria = ?,
            IDMarca = ?,
            EstoqueMinimo = ?,
            EstoqueAtual = ?,
            CodBarra = ?,
            PrecoCompra = ?,
            PrecoVenda = ?,
            Reajuste = ?
        WHERE IDProduto = ?
    """, (
        data.get("categoria"),
        data.get("marca"),
        data.get("estoque_minimo"),
        data.get("estoque_atual"),
        data["codbarra"],
        data.get("preco_compra"),
        data.get("preco_venda"),
        data.get("reajuste"),
        id
    ))

    conn.commit()
    conn.close()

def removeProduct(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ItemPedido WHERE IDProdutoServico = (SELECT IDProdutoServico FROM Produto WHERE IDProduto = ?)", (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise Exception("Produto não pode ser removido pois está em vendas (ItemPedido).")

    cursor.execute("SELECT COUNT(*) FROM ItemFornecido WHERE IDProduto = ?", (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise Exception("Produto não pode ser removido pois está em compras (ItemFornecido).")

    
    cursor.execute("""
        DELETE FROM ProdutoServico 
        WHERE IDProdutoServico = (SELECT IDProdutoServico FROM Produto WHERE IDProduto = ?)
    """, (id,))

    conn.commit()
    conn.close()
