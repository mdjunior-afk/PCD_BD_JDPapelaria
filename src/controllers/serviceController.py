from src.models.serviceModel import *

class ServiceController:
    @staticmethod
    def save(data={}):
        print(f"add: {data}")

        addService(data)

    @staticmethod
    def get(window, data={}, type="edit"):
        products = getService(data)

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
        removeService(id)

        ServiceController.get(window, window.search_input.text(), type="search")