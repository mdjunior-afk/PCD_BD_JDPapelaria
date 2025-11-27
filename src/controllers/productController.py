from src.models.productModel import *

from PySide6.QtWidgets import *

class ProductController:
    @staticmethod
    def save(data):
        addProduct(data)

    @staticmethod
    def get(window, data, type):
        products = getProduct(data)

        print(products)

        if type == "edit":
            print(data)

        elif type == "search":
            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for product in products:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                for column in range(table.columnCount()):
                    table.setItem(row, column, QTableWidgetItem(str(product[column])))
                    
    @staticmethod
    def getCategories(window):
        categories = getCategories()
        
        categories_list = [t[0] for t in categories]

        window.category_input.addItems(categories_list)
        window.search_category_input.addItem("Todos")
        window.search_category_input.addItems(categories_list)

    @staticmethod
    def getBrands(window):
        brands = getBrands()
        
        brand_list = [t[0] for t in brands]

        window.brand_input.addItems(brand_list)

    @staticmethod
    def remove(window, id):
        removeProduct(id)

        ProductController.get(window, window.search_input.text(), type="search")
