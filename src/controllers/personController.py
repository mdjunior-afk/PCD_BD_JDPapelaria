from src.models.personModel import *

class PersonController:
    @staticmethod
    def get(window, data={}, type="edit"):
        persons = getPerson(data)

        if type == "edit":
            window.name_input.setText(persons[0]["nome"])
            # Adicionar os valores no edit
            
        elif type == "search":
            for person in persons:
                window.search_table.setRowCount(window.search_table.rowCount() + 1)

                row = window.search_table.rowCount() - 1

                # Adicionar os valores na tabela

    @staticmethod
    def remove(window, id):
        removePerson(id)

        PersonController.get(window, window.search_input.text(), type="search")
