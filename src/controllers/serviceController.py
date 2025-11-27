from src.models.serviceModel import *

from PySide6.QtWidgets import *

class ServiceController:
    @staticmethod
    def save(data={}):
        print(f"add: {data}")

        addService(data)

    @staticmethod
    def get(window, data={}, type="edit"):
        services = getService(data)

        if type == "edit":
            window.name_input.setText(services[0]["nome"])
            # Adicionar os valores no edit

        elif type == "search":
            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for services in services:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                for column in range(table.columnCount()):
                    table.setItem(row, column, QTableWidgetItem(str(services[column])))

    @staticmethod
    def remove(window, id):
        removeService(id)

        ServiceController.get(window, window.search_input.text(), type="search")