from src.models.saleModel import *

from PySide6.QtWidgets import *

class SalesController:
    @staticmethod
    def save(data={}):
        print(f"add: {data}")

        addSale(data)

    @staticmethod
    def get(window, data={}, type="edit"):
        sales = getSale(data)

        if type == "edit":
            window.name_input.setText(sales[0]["nome"])
            # Adicionar os valores no edit

        elif type == "search":
            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for sales in sales:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                for column in range(table.columnCount()):
                    table.setItem(row, column, QTableWidgetItem(str(sales[column])))

    @staticmethod
    def remove(window, id):
        removeSale(id)

        SalesController.get(window, window.search_input.text(), type="search")