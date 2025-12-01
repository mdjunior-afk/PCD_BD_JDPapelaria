from src.models.saleModel import *
from src.models.serviceModel import *

from PySide6.QtWidgets import *

class ServiceController:
    @staticmethod
    def save(data={}):

        addService(data)

    @staticmethod
    def get(window, data={}, type="edit"):
        if type == "search_item":
            services = getServices(data)
            data = []

            for service in services:
                data.append({"nome": service[1], "valor": service[3], "quantidade": 1, "subtotal": service[3]})

            print(data)

            return data
        elif type == "edit":
            services = getEditService(data["id"])
            payments = getSalePayments(data["id"])

            print(data["id"], services)

            window.id_input.setValue(services[0][0])
            window.search_client_input.setText(services[0][2])
            window.search_client_input.setReadOnly(True)
            window.item_explorer.hide()

            for item in services:
                window.transaction_tab.updateServiceTable(item[4], item[5], item[6], item[7])
                window.total_input.setValue(item[3])

            for payment in payments:
                window.transaction_tab.updatePaymentTable(payment[0], payment[1])
        else:
            sales = getService(data)

            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for sales in sales:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                table.setItem(row, 0, QTableWidgetItem(str(sales[0])))
                table.setItem(row, 1, QTableWidgetItem(str(sales[1])))
                table.setItem(row, 2, QTableWidgetItem(str(sales[2])))
                table.setItem(row, 3, QTableWidgetItem(str(sales[3])))
                table.setItem(row, 4, QTableWidgetItem(str(sales[8])))

    @staticmethod
    def remove(id):
        removeService(id)

    def getPaymentMethods(document_input):
        methods = getAllPaymentMethods()
        
        methods_list = [t[0] for t in methods]

        document_input.addItems(methods_list)