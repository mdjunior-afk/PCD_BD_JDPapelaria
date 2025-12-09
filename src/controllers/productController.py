from src.models.productModel import *

from PySide6.QtWidgets import *

class ProductController:
    @staticmethod
    def save(data):

        addProduct(data)

    @staticmethod
    def get(window, data, type):
        print(data) 

        products = getProduct(data)

        print(products)

        if type == "edit":
            window.id_input.setValue(products[0][0])
            window.name_input.setText(products[0][1])
            window.brand_input.setCurrentText(products[0][7])
            window.category_input.setCurrentText(products[0][8])
            window.barcode_input.setText(products[0][9])
            window.purchase_input.setValue(products[0][4])
            window.adjust_input.setValue(products[0][5])
            window.sale_input.setValue(products[0][6])
            window.minimum_stock_input.setValue(products[0][2])
            window.current_stock_input.setValue(products[0][3])
        elif type == "search_item":
            data = []

            for product in products:
                data.append({"nome": product[1], "valor": product[6], "quantidade": 1, "subtotal": product[6]})

            return data
            
        elif type == "search":
            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for product in products:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                for column in range(table.columnCount()):
                    table.setItem(row, column, QTableWidgetItem(str(product[column + 1 if column > 1 else column])))
                    
    @staticmethod
    def getCategories(window):
        categories = getCategories(name='')
        
        categories_list = [t[1] for t in categories]

        window.category_input.clear()
        window.category_input.addItems(categories_list)

        window.search_category_input.clear()
        window.search_category_input.addItem("Todos")
        window.search_category_input.addItems(categories_list)
        window.search_category_input.updateSize()

    @staticmethod
    def getBrands(window):
        brands = getBrands(name='')
        
        brand_list = [t[1] for t in brands]

        window.brand_input.clear()
        window.brand_input.addItems(brand_list)
        window.brand_input.updateSize()

    @staticmethod
    def edit(window, id, data):
        data["id_marca"] = getBrandID(data["id_marca"])[0]
        data["id_categoria"] = getCategoryID(data["id_categoria"])[0]

        editProduct(id, data)

    @staticmethod
    def remove(window, id):
        removeProduct(id)

        ProductController.get(window, {"pesquisa": window.search_input.text()}, type="search")
