from src.models.personModel import *

from PySide6.QtWidgets import *

class PersonController:
    @staticmethod
    def get(window, data={}, type="edit"):
        persons = getPerson(data)

        if type == "edit":
            window.name_input.setText(persons[0]["nome"])
            # Adicionar os valores no edit
            
        elif type == "search":
            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for person in persons:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                for column in range(table.columnCount()):
                    table.setItem(row, column, QTableWidgetItem(str(person[column])))

    @staticmethod
    def remove(window, id):
        removePerson(id)

        PersonController.get(window, window.search_input.text(), type="search")
