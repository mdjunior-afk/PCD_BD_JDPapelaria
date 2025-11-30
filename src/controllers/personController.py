from src.models.personModel import *
from PySide6.QtCore import QDate

from PySide6.QtWidgets import *

class PersonController:
    @staticmethod
    def get(window, data={}, type="edit"):

        persons = getPerson(data)

        if type == "edit":
            if not data:
                # Tratar o caso de não encontrar a pessoa (pode ser um QMessageBox)
                print("Erro: Dados da pessoa não encontrados ou vazios.")
                return

            # Armazenar o ID para uso na função de salvar (editPerson)
            window.current_person_id = data.get("id_pessoa") 

            # --- 1. Dados Básicos e Tipo ---
            
            # O tipo de pessoa é determinado pela presença de CPF ou CNPJ no resultado
            is_pf = data.get("CPF") is not None and data.get("CPF") != ""
            
            # Seta o tipo no ComboBox e dispara o onIndexChanged
            window.type_input.setCurrentIndex(0 if is_pf else 1)
            
            # window os campos que dependem do tipo
            window.name_input.setText(data.get("Nome", ""))
            window.document_input.setText(data.get("CPF") if is_pf else data.get("CNPJ", ""))
            
            if is_pf:
                # Campos específicos de Pessoa Física
                window.sex_input.setCurrentText(data.get("Sexo", "Outro"))
                window.birthday_input.setDate(QDate.fromString(data.get("DataNascimento", "01/01/2000"), "dd/MM/yyyy")) # Ajuste o formato da data conforme seu DB
            else:
                # Campos específicos de Pessoa Jurídica
                window.fantasy_name_input.setText(data.get("NomeFantasia", ""))

            # Flags Cliente/Fornecedor
            window.client_box.setChecked(data.get("Cliente") == 1)
            window.supplier_box.setChecked(data.get("Fornecedor") == 1)

            # --- 2. Contatos (Limpa e Preenche) ---
            window.contact_table.setRowCount(0) # Limpa a tabela
            
            # Assume que "Contatos" é uma lista de dicionários no objeto de dados
            # Ex: [{"ID": 1, "Tipo": "Email", "Valor": "a@b.com"}, ...]
            contacts = data.get("Contatos", []) 
            for i, contact in enumerate(contacts):
                # Você precisa de um método que adicione os itens no formato QTableWidgetItem, 
                # similar ao que você faz no getCNPJ ou addContactToTable.
                window.contact_table.setRowCount(window.contact_table.rowCount() + 1)
                window.contact_table.setItem(i, 0, QTableWidgetItem(str(contact.get("ID", i+1)))) # ID Real ou temporário
                window.contact_table.setItem(i, 1, QTableWidgetItem(contact.get("Tipo", "")))
                window.contact_table.setItem(i, 2, QTableWidgetItem(contact.get("Valor", "")))
            
            window.contact_table.resizeColumnsToContents()

            # --- 3. Endereços (Limpa e Preenche) ---
            window.address_table.setRowCount(0) # Limpa a tabela
            
            # Assume que "Enderecos" é uma lista de dicionários no objeto de dados
            # Ex: [{"ID": 1, "CEP": "...", "Logradouro": "...", ...}, ...]
            addresses = data.get("Enderecos", [])
            for i, address in enumerate(addresses):
                window.address_table.setRowCount(window.address_table.rowCount() + 1)
                window.address_table.setItem(i, 0, QTableWidgetItem(str(address.get("ID", i+1)))) # ID Real ou temporário
                window.address_table.setItem(i, 1, QTableWidgetItem(address.get("CEP", "")))
                window.address_table.setItem(i, 2, QTableWidgetItem(address.get("Logradouro", "")))
                window.address_table.setItem(i, 3, QTableWidgetItem(address.get("Numero", "")))
                window.address_table.setItem(i, 4, QTableWidgetItem(address.get("Bairro", "")))
                window.address_table.setItem(i, 5, QTableWidgetItem(address.get("Cidade", "")))
                window.address_table.setItem(i, 6, QTableWidgetItem(address.get("Estado", "")))
                window.address_table.setItem(i, 7, QTableWidgetItem(address.get("Complemento", "")))
            
        elif type == "search":
            table = window.search_table
            table.clearContents()
            table.setRowCount(0)

            for person in persons:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                table.setItem(row, 0, QTableWidgetItem(str(person[0])))
                table.setItem(row, 1, QTableWidgetItem(str(person[2])))
                if (person[1] == 1):
                    table.setItem(row, 2, QTableWidgetItem(str(person[4])))
                else:
                    table.setItem(row, 2, QTableWidgetItem(str(person[3])))

                table.setItem(row, 3, QTableWidgetItem(str(person[5])))
                table.setItem(row, 4, QTableWidgetItem(str(person[6] + person[7] + person[8])))

    @staticmethod
    def add(data, type):
        addPerson(data)

    @staticmethod
    def remove(window, id):
        removePerson(id)

        PersonController.get(window, window.search_input.text(), type="search")
