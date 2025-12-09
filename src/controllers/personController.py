from src.models.personModel import *
from PySide6.QtCore import QDate

from PySide6.QtWidgets import *

class PersonController:
    @staticmethod
    def get(window, data={}, type="edit"):

        persons = getPerson(data)

        if type == "search_item":
            data = []

            for person in persons:
                data.append({"nome": person[1]})

            return data

        elif type == "edit":
            persons = persons[0]

            window.id_input.setValue(persons[0])
            window.name_input.setText(persons[1])
            if (persons[3] != None):
                window.type_input.setCurrentText("Pessoa física")
                window.document_input.setText(persons[3])
                window.sex_input.setCurrentText(persons[6])
                window.birthday_input.setDate(QDate.fromString(persons[7]))
            else:
                window.type_input.setCurrentText("Pessoa jurídica")
                window.document_input.setText(persons[4])
                window.fantasy_name_input.setText(persons[8])

            address_list = getAllAddress(persons[0])
            contacts_list = getAllContacts(persons[0])

            window.address_table.setRowCount(0)
            window.contact_table.setRowCount(0)

            for contact in contacts_list:
                table = window.contact_table
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                table.setItem(row, 0, QTableWidgetItem(str(contact[0] if contact[0] != None else '')))
                table.setItem(row, 1, QTableWidgetItem(str(contact[2] if contact[2] != None else '')))
                table.setItem(row, 2, QTableWidgetItem(str(contact[3] if contact[3] != None else '')))

            for address in address_list:
                table = window.address_table
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                table.setItem(row, 0, QTableWidgetItem(str(address[0] if address[0] != None else '')))
                table.setItem(row, 1, QTableWidgetItem(str(address[8] if address[8] != None else '')))
                table.setItem(row, 2, QTableWidgetItem(str(address[2] if address[2] != None else '')))
                table.setItem(row, 3, QTableWidgetItem(str(address[3] if address[3] != None else '')))
                table.setItem(row, 4, QTableWidgetItem(str(address[5] if address[5] != None else '')))
                table.setItem(row, 5, QTableWidgetItem(str(address[6] if address[6] != None else '')))
                table.setItem(row, 6, QTableWidgetItem(str(address[7] if address[7] != None else '')))
                table.setItem(row, 7, QTableWidgetItem(str(address[4] if address[4] != None else '')))
            
        elif type == "search":
            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for person in persons:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                table.setItem(row, 0, QTableWidgetItem(str(person[0] if person[0] != None else '')))
                table.setItem(row, 1, QTableWidgetItem(str(person[1] if person[1] != None else '')))
                if (person[3] != None):
                    table.setItem(row, 2, QTableWidgetItem(str(person[3] if person[3] != None else '')))
                else:
                    table.setItem(row, 2, QTableWidgetItem(str(person[4] if person[4] != None else '')))

                table.setItem(row, 3, QTableWidgetItem(str(person[9] if person[9] != None else '')))
                table.setItem(row, 4, QTableWidgetItem(str(person[10] if person[10] != None else '')))

    @staticmethod
    def add(data, type):
        addPerson(data)

    @staticmethod
    def edit(id, data):
        editPerson(id, data)

    @staticmethod
    def remove(window, id):
        removePerson(id)

        PersonController.get(window, {"pesquisa": window.search_input.text()}, type="search")

    @staticmethod
    def getSuppliers(data):
        return getSuppliers(data)
