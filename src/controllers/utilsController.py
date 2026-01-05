from PySide6.QtWidgets import *
from PySide6.QtCore import QDate    

from src.models import utilsModels

class UtilsController:
    @staticmethod
    def getLowerStocks(window):
        lower_stock = utilsModels.getLowerStocks()

        window.stock_info.info_label.setText(str(lower_stock[0] if lower_stock != None else "0"))

    def getAnniversaries(window):
        anniversaries = utilsModels.getAnniversaries()

        window.birthday_qtd.info_label.setText(str(anniversaries[0] if anniversaries != None else "0"))

    def getTodaySale(window):
        today_sale = utilsModels.getTodaySale()

        window.daily_sale.info_label.setText(str(today_sale[0] if today_sale != None else "0"))

    def getEntries(window, data):
        print(data)
        entries = utilsModels.getEntries(data)

        # Adicionar os items na tabela
        table = window.search_table
        table.clearContents()
        table.setRowCount(0)

        for row_data in entries:
            row_number = table.rowCount()
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 3:  # Formatar valor total como moeda
                    data = f"R$ {data:.2f}"
                elif column_number == 1:  # Formatar data
                    data = QDate.fromString(data, "yyyy-MM-dd").toString("dd/MM/yyyy")

                item = QTableWidgetItem(str(data))
                table.setItem(row_number, column_number, item)

    def getEntryByID(entry_id):
        return utilsModels.getEntryByID(entry_id)

    def addEntry(data):
        utilsModels.addEntry(data)
    
    def editEntry(entry_id, data):
        utilsModels.editEntry(entry_id, data)