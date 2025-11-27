from src.models.productModel import *

class ProductController:
    @staticmethod
    def get(window, data={}, type="edit"):
        products = getProduct(data)

        if type == "edit":
            window.name_input.setText(products[0]["nome"])
            # Adicionar os valores no edit

        elif type == "search":
            for product in products:
                window.search_table.setRowCount(window.search_table.rowCount() + 1)

                row = window.search_table.rowCount() - 1

                # Adicionar os valores na tabela

    @staticmethod
    def remove(window, id):
        removeProduct(id)

        ProductController.get(window, window.search_input.text(), type="search")
