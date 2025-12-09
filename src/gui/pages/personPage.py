from PySide6.QtWidgets import *
from PySide6.QtCore import QDate, Qt

from src.gui.widgets import *
from src.gui.utils import *
from src.utils import cepAPI, locations, CNPJApi

from src.gui.widgets.removeWindow import *

from src.controllers.personController import PersonController

import json

class PersonPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Labels
        labels_widget = QWidget()
        labels_layout = QVBoxLayout()
        labels_widget.setLayout(labels_layout)

        title_label = Label(text="Painel de Pessoas", type="Title")
        subtitle_label = Label(text="Gerencie todas as pessoas cadastradas", type="Subtitle")

        labels_layout.addWidget(title_label)
        labels_layout.addWidget(subtitle_label)

        self.tab = Tab()
        
        search_tab, self.search_table = self.createSearchTab()
        edition_tab = self.createEditionTab()

        self.search_table.add_action.triggered.connect(self.addPerson)
        self.search_table.edit_action.triggered.connect(lambda: self.editPerson(self.search_table))
        self.search_table.remove_action.triggered.connect(lambda: self.removePerson(self.search_table))

        self.tab.addTab(search_tab, "Pesquisar", )
        self.tab.addTab(edition_tab, "Adicionar/Editar")

        layout.addWidget(labels_widget)
        layout.addWidget(self.tab)

    def createSearchTab(self):
        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        search_layout = QGridLayout()

        search_label = Label("Pesquisar", type="InputLabel")
        type_label = Label("Tipo de pessoa", type="InputLabel")

        self.search_input = LineEdit("Pesquise por uma pessoa")
        self.search_type_input = ComboBox()
        self.search_type_input.addItems(["Todos", "Pessoa física", "Pessoa jurídica"])
        search_button = PushButton("Pesquisar", icon_path="search.svg", type="WithoutBackground")
        export_button = PushButton("Exportar", icon_path="download.svg", type="WithBackground")

        search_button.clicked.connect(lambda: PersonController.get(self, {"procura": self.search_input.text(), "tipo": self.search_type_input.currentText()}, "search"))

        search_layout.addWidget(search_label, 0, 0)
        search_layout.addWidget(type_label, 0, 1)

        search_layout.addWidget(self.search_input, 1, 0)
        search_layout.addWidget(self.search_type_input, 1, 1)
        search_layout.addWidget(search_button, 1, 2)

        search_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 3)

        search_layout.addWidget(export_button, 1, 4)

        table = Table(["ID", "Nome", "CPF/CNPJ", "Contato", "Endereço"])

        search_layout.addWidget(table, 2, 0, 1, 4)
        
        layout.addLayout(search_layout)
        layout.addWidget(table)

        return widget, table
    
    def createEditionTab(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent !important;")

        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        buttons_widget, buttons = createWindowButtons()

        person_type_box = GroupBox("Tipo da pessoa")
        person_type_layout = QHBoxLayout()
        person_type_box.setLayout(person_type_layout)

        self.client_box = QCheckBox("Cliente")
        self.client_box.setChecked(True)
        self.supplier_box = QCheckBox("Fornecedor")

        self.client_box.setFocusPolicy(Qt.NoFocus)
        self.supplier_box.setFocusPolicy(Qt.NoFocus)

        person_type_layout.addWidget(self.client_box)
        person_type_layout.addWidget(self.supplier_box)
        person_type_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        info_box = GroupBox("Informações de pessoa")
        info_layout = QGridLayout()
        info_box.setLayout(info_layout)

        name_label = Label("Nome", type="InputLabel")
        type_label = Label("Tipo de pessoa", type="InputLabel")
        document_label = Label("CPF", type="InputLabel")
        sex_label = Label("Sexo", type="InputLabel")
        birthday_label = Label("Data de nascimento", type="InputLabel")
        fantasy_name_label = Label("Nome fantasia", type="InputLabel")

        self.id_input = SpinBox()
        self.id_input.setValue(0)
        self.name_input = LineEdit()
        self.type_input = ComboBox()
        self.type_input.addItems(["Pessoa física", "Pessoa jurídica"])
        self.type_input.updateSize()
        self.document_input = LineEdit()
        self.sex_input = ComboBox()
        self.sex_input.addItems(["Masculino", "Feminino", "Outro"])
        self.sex_input.updateSize()
        self.birthday_input = DateEdit(QDate.currentDate())
        self.fantasy_name_input = LineEdit()
        get_cnpj_button = PushButton("Pesquisar", icon_path="search.svg")

        fantasy_name_label.setVisible(False)
        self.fantasy_name_input.setVisible(False)
        get_cnpj_button.setVisible(False)

        self.document_input.setInputMask("000.000.000-00;_")
        self.document_input.textChanged.connect(lambda x: print(x))

        info_layout.addWidget(name_label, 0, 0)
        info_layout.addWidget(type_label, 2, 0)
        info_layout.addWidget(document_label, 2, 1)
        info_layout.addWidget(sex_label, 2, 2)
        info_layout.addWidget(birthday_label, 2, 3)
        info_layout.addWidget(fantasy_name_label, 2, 3)
        
        info_layout.addWidget(self.name_input, 1, 0, 1, 4)
        info_layout.addWidget(self.type_input, 3, 0)
        info_layout.addWidget(self.document_input, 3, 1)
        info_layout.addWidget(get_cnpj_button, 3, 2)
        info_layout.addWidget(self.sex_input, 3, 2)
        info_layout.addWidget(self.birthday_input, 3, 3)
        info_layout.addWidget(self.fantasy_name_input, 3, 3)
        
        info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        contact_box = GroupBox("Informações de contato")
        contact_layout = QVBoxLayout()
        contact_box.setLayout(contact_layout)

        contact_buttons_widget, contact_buttons, = createTableButtons()
        self.contact_table = Table(["ID", "Tipo", "Contato"]) # Use self.contact_table
        
        contact_buttons[0].clicked.connect(self.addContactWindow)
        # CONEXÃO PARA REMOVER CONTATO
        # TODO: Implementar a lógica de edição para contact_buttons[1]
        contact_buttons[1].clicked.connect(self.editContactWindow)
        
        contact_buttons[2].clicked.connect(self.removeSelectedContact)
        
        contact_layout.addWidget(contact_buttons_widget)
        contact_layout.addWidget(self.contact_table)

        address_box = GroupBox("Informações de endereço")
        address_layout = QVBoxLayout()
        address_box.setLayout(address_layout)

        address_buttons_widget, address_buttons = createTableButtons()
        self.address_table = Table(["ID", "CEP", "Logradouro", "Número", "Bairro", "Cidade", "Estado", "Complemento"]) # Use self.address_table

        address_buttons[0].clicked.connect(self.addAddressWindow)
        # CONEXÃO PARA REMOVER ENDEREÇO
        address_buttons[2].clicked.connect(self.removeSelectedAddress)
        # TODO: Implementar a lógica de edição para address_buttons[1]
        address_buttons[1].clicked.connect(self.editAddressWindow)
        
        address_layout.addWidget(address_buttons_widget)
        address_layout.addWidget(self.address_table)

        layout.addWidget(person_type_box)
        layout.addWidget(info_box)
        layout.addWidget(contact_box)
        layout.addWidget(address_box)
        layout.addWidget(buttons_widget)

        self.type_input.currentIndexChanged.connect(lambda index: self.onIndexChanged(index, name_label, document_label, self.document_input, (self.sex_input, self.birthday_input, sex_label, birthday_label), (self.fantasy_name_input, fantasy_name_label, get_cnpj_button)))
        get_cnpj_button.clicked.connect(lambda x: self.getCNPJ(
            self.document_input, {"razao_social": self.name_input, "nome_fantasia": self.fantasy_name_input}, self.contact_table, self.address_table
        ))

        buttons[0].clicked.connect(self.addPerson)
        buttons[1].clicked.connect(self.resetInputs)

        scroll_area.setWidget(widget)

        return scroll_area
    
    def addContactToTable(self, contact_type: str, value: str, row_to_edit=None):
        """Adiciona ou edita um contato na tabela."""
        table = self.contact_table
        
        # Se row_to_edit for um índice válido, estamos editando
        if row_to_edit is not None and 0 <= row_to_edit < table.rowCount():
            row = row_to_edit
            # O ID deve ser mantido se for uma edição. Assumindo que o ID está na coluna 0.
            # Se não for uma edição, o ID será atribuído abaixo.
            item_id = table.item(row, 0).text()
        else:
            # Adicionar nova linha
            row = table.rowCount()
            table.setRowCount(row + 1)
            # Atribuir um ID temporário (pode ser o índice da linha ou um contador)
            # Para este exemplo, usaremos o índice da linha como um ID temporário se não houver ID real do banco de dados
            item_id = str(row + 1) # ID base 1 para melhor visualização
            table.setItem(row, 0, QTableWidgetItem(item_id))

        table.setItem(row, 1, QTableWidgetItem(contact_type))
        table.setItem(row, 2, QTableWidgetItem(value))

    def removeSelectedContact(self):
        """Remove a linha selecionada da tabela de contatos."""
        table = self.contact_table
        selected_rows = table.selectionModel().selectedRows()
        
        # As linhas devem ser removidas em ordem decrescente para não bagunçar os índices
        for index in sorted(selected_rows, reverse=True):
            table.removeRow(index.row())

    def addAddressToTable(self, cep: str, logradouro: str, numero: str, bairro: str, cidade: str, estado: str, complemento: str, row_to_edit=None):
        """Adiciona ou edita um endereço na tabela."""
        table = self.address_table
        
        # Se row_to_edit for um índice válido, estamos editando
        if row_to_edit is not None and 0 <= row_to_edit < table.rowCount():
            row = row_to_edit
            item_id = table.item(row, 0).text()
        else:
            # Adicionar nova linha
            row = table.rowCount()
            table.setRowCount(row + 1)
            item_id = str(row + 1)
            table.setItem(row, 0, QTableWidgetItem(item_id))

        table.setItem(row, 1, QTableWidgetItem(cep))
        table.setItem(row, 2, QTableWidgetItem(logradouro))
        table.setItem(row, 3, QTableWidgetItem(numero))
        table.setItem(row, 4, QTableWidgetItem(bairro))
        table.setItem(row, 5, QTableWidgetItem(cidade))
        table.setItem(row, 6, QTableWidgetItem(estado))
        table.setItem(row, 7, QTableWidgetItem(complemento))
        
    def removeSelectedAddress(self):
        """Remove a linha selecionada da tabela de endereços."""
        table = self.address_table
        selected_rows = table.selectionModel().selectedRows()
        
        # As linhas devem ser removidas em ordem decrescente para não bagunçar os índices
        for index in sorted(selected_rows, reverse=True):
            table.removeRow(index.row())


    def addPerson(self):
        # Converte birthday para formato SQLite (yyyy-MM-dd)
        birthday_date = self.birthday_input.date()
        birthday_str = birthday_date.toString('yyyy-MM-dd')

        data = {
            "nome": self.name_input.text(),
            "type": self.type_input.currentText(),
            "document": self.document_input.text(),
            "sex": self.sex_input.currentText(),
            "birthday": birthday_str,
            "address": self.getAllAddress(),
            "contact": self.getAllContacts(),
            "fantasy_name": self.fantasy_name_input.text(),
            "is_client": int(self.client_box.isChecked()),
            "is_supplier": int(self.supplier_box.isChecked())
        }

        if self.id_input.value() == 0:
            PersonController.add(data, "add")
        else:
            PersonController.edit(self.id_input.value(), data)

        message = MessageDialog(self, "Sucesso", message="Pessoa salva com sucesso!", msg_type=MessageDialog.SUCCESS)
        message.exec()
        
        self.resetInputs()

    def editPerson(self, table: Table):
        selectedItems = table.selectedItems()

        PersonController.get(self, {"id_pessoa": selectedItems[0].text()}, "edit")

        self.tab.setCurrentIndex(1)

    def removePerson(self, table: Table):
        selectedItems = table.selectedItems()
    
        print(selectedItems)

        dialog = RemoveDialog(
            parent=self,
            title="Remover Pessoa",
            item_name=f"Pessoa: {selectedItems[1].text()}"
        )

        if dialog.exec() == QDialog.Accepted:
            if (selectedItems[0].text() != "1"):
                PersonController.remove(self, selectedItems[0].text())

                PersonController.get(self, {}, "search")
            else:
                message = MessageDialog(self, "Erro ao remover", message=f"Não é possivel remover a pessoa {selectedItems[1].text()}", msg_type=MessageDialog.ERROR)
                message.exec()

    def getAllAddress(self):     
        if not hasattr(self, 'address_table') or not isinstance(self.address_table, QTableWidget):
            return []

        addresses = []
        table = self.address_table
        
        column_names = ["ID", "cep", "logradouro", "numero", "bairro", "cidade", "estado", "complemento"]

        for row in range(table.rowCount()):
            address_data = {}
            for col, name in enumerate(column_names):
                item = table.item(row, col)
                address_data[name] = item.text() if item is not None else ""
            
            address_data.pop("ID", None) 
            addresses.append(address_data)
            
        return addresses
    
    def getAllContacts(self):     
        if not hasattr(self, 'contact_table') or not isinstance(self.contact_table, QTableWidget):
            return []

        contacts = []
        table = self.contact_table
        
        column_names = ["ID", "tipo", "valor"]

        for row in range(table.rowCount()):
            contact_data = {}
            for col, name in enumerate(column_names):
                item = table.item(row, col)
                contact_data[name] = item.text() if item is not None else ""
            
            contact_data.pop("ID", None) 
            contacts.append(contact_data)
            
        return contacts
    
    def getCNPJ(self, cnpj_input, inputs, contact_table: QTableWidget, address_table: QTableWidget):
        data = CNPJApi.searchCNPJ(cnpj_input)

        contact_table.setRowCount(0)
        address_table.setRowCount(0)

        inputs["razao_social"].setText(data["razao_social"])
        inputs["nome_fantasia"].setText(data["estabelecimento"]["nome_fantasia"])

        # Email data
        row = 0

        if data["estabelecimento"]["email"] != None:
            contact_table.setRowCount(contact_table.rowCount() + 1)
            contact_table.setItem(0, 0, QTableWidgetItem(str(row)))
            contact_table.setItem(row, 1, QTableWidgetItem("Email"))
            contact_table.setItem(row, 2, QTableWidgetItem(data["estabelecimento"]["email"]))
            row += 1
            
        if data["estabelecimento"]["telefone1"] != None:
            contact_table.setRowCount(contact_table.rowCount() + 1)
            contact_table.setItem(row, 0, QTableWidgetItem(str(row)))
            contact_table.setItem(row, 1, QTableWidgetItem("Telefone fixo"))
            contact_table.setItem(row, 2, QTableWidgetItem(f"({data['estabelecimento']['ddd1']}) {data['estabelecimento']['telefone1']}"))
            row += 1
        
        if data["estabelecimento"]["telefone2"] != None:
            contact_table.setRowCount(contact_table.rowCount() + 1)
            contact_table.setItem(row, 0, QTableWidgetItem(str(row)))
            contact_table.setItem(row, 1, QTableWidgetItem("Telefone fixo"))
            contact_table.setItem(row, 2, QTableWidgetItem(f"({data['estabelecimento']['ddd2']}) {data['estabelecimento']['telefone2']}"))
            row += 1

        row = 0

        address_table.setRowCount(address_table.rowCount() + 1)
        address_table.setItem(row, 0, QTableWidgetItem(str(row)))
        address_table.setItem(row, 1, QTableWidgetItem(data["estabelecimento"]["cep"]))
        address_table.setItem(row, 2, QTableWidgetItem(data["estabelecimento"]["logradouro"]))
        address_table.setItem(row, 3, QTableWidgetItem(data["estabelecimento"]["numero"]))
        address_table.setItem(row, 4, QTableWidgetItem(data["estabelecimento"]["bairro"]))
        address_table.setItem(row, 5, QTableWidgetItem(data["estabelecimento"]["cidade"]["nome"]))
        address_table.setItem(row, 6, QTableWidgetItem(data["estabelecimento"]["estado"]["sigla"]))
        address_table.setItem(row, 7, QTableWidgetItem(data["estabelecimento"]["complemento"] if data["estabelecimento"]["complemento"] != None else ""))
    
    def resetInputs(self):
        self.id_input.setValue(0)
        self.name_input.clear()
        self.type_input.setCurrentIndex(0)
        self.document_input.setText('')
        self.sex_input.setCurrentIndex(0)
        self.birthday_input.setDate(QDate.currentDate())
        self.fantasy_name_input.setText('')

        self.address_table.setRowCount(0)
        self.contact_table.setRowCount(0)

    def applyStyleToDialog(self, dialog: QDialog):
        """Aplica o estilo global e o estilo local dos botões a uma QDialog."""
        
        # 1. Obtém o config atual
        with open("src/configuration.json", "r") as f:
            config = json.load(f)

        # 2. Aplica Estilo Local a Botões Customizados DENTRO do diálogo
        for widget in dialog.findChildren(QPushButton):
            # Apenas se tiver o método setStyle (se for seu PushButton)
            if hasattr(widget, 'setStyle'):
                widget.setStyle(config)

    def onIndexChanged(self, index, name, label, input, cpf_inputs: tuple, cnpj_inputs: tuple):
            if index == 0:
                name.setText("Nome")
                input.setInputMask("000.000.000-00;_")
                label.setText("CPF")
                input.clear()
                
                for i in cpf_inputs:
                    i.setVisible(True)

                for i in cnpj_inputs:
                    i.setVisible(False)

            elif index == 1:
                name.setText("Razão Social")
                input.setInputMask("00.000.000/0000-00;_")
                label.setText("CNPJ")
                input.clear()

                for i in cpf_inputs:
                    i.setVisible(False)

                for i in cnpj_inputs:
                    i.setVisible(True)

    def addContactWindow(self):
        # A janela de contato precisa saber qual tabela atualizar (self.contact_table)
        self.contact_window = ContactWindow(parent=self, parent_page=self, is_editing=False)
        self.applyStyleToDialog(self.contact_window)
        self.contact_window.exec()
    
    def editContactWindow(self):
        # Implementação de edição simplificada: tenta pegar os dados da linha selecionada
        selected_rows = self.contact_table.selectionModel().selectedRows()
        if not selected_rows:
            # Poderia ser um QMessageBox, mas por simplicidade, apenas retorna
            return 
        
        row_index = selected_rows[0].row()
        
        data = {
            "row_index": row_index,
            "type": self.contact_table.item(row_index, 1).text(),
            "value": self.contact_table.item(row_index, 2).text()
        }
        
        self.contact_window = ContactWindow(parent=self, parent_page=self, data=data, is_editing=True)
        self.applyStyleToDialog(self.contact_window)
        self.contact_window.exec()

    def addAddressWindow(self):
        # A janela de endereço precisa saber qual tabela atualizar (self.address_table)
        self.address_window = AddressWindow(parent=self, parent_page=self, is_editing=False)
        self.applyStyleToDialog(self.address_window)
        self.address_window.exec()

    def editAddressWindow(self):
        # Implementação de edição simplificada: tenta pegar os dados da linha selecionada
        selected_rows = self.address_table.selectionModel().selectedRows()
        if not selected_rows:
            # Poderia ser um QMessageBox, mas por simplicidade, apenas retorna
            return 
        
        row_index = selected_rows[0].row()
        
        data = {
            "row_index": row_index,
            "cep": self.address_table.item(row_index, 1).text(),
            "street": self.address_table.item(row_index, 2).text(),
            "number": self.address_table.item(row_index, 3).text(),
            "neighborhood": self.address_table.item(row_index, 4).text(),
            "city": self.address_table.item(row_index, 5).text(),
            "estate": self.address_table.item(row_index, 6).text(),
            "complement": self.address_table.item(row_index, 7).text(),
        }

        self.address_window = AddressWindow(parent=self, parent_page=self, data=data, is_editing=True)
        self.applyStyleToDialog(self.address_window)
        self.address_window.exec()

# --- ContactWindow Modificada ---
class ContactWindow(QDialog):
    def __init__(self, parent=None, parent_page=None, data={}, is_editing=False):
        super().__init__(parent=parent)

        self.parent_page = parent_page
        self.is_editing = is_editing
        self.row_index = data.get("row_index") # Armazena o índice se for edição

        self.setWindowFlag(Qt.Window)
        self.setWindowTitle("Editar Contato" if is_editing else "Adicionar Contato")

        self.setMaximumHeight(200)
        self.setMinimumWidth(500)

        self.setStyleSheet("background-color: #F3F3F3 !important;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        box = GroupBox("Cadastro de contato") # Corrigido o título
        box_layout = QGridLayout()
        box.setLayout(box_layout)

        buttons_widget, buttons = createWindowButtons()
        
        # Conexões dos botões para adicionar/editar
        buttons[0].setText("Salvar" if is_editing else "Adicionar")
        buttons[0].clicked.connect(self.save_contact)
        buttons[1].clicked.connect(self.clearInputs)
        buttons[2].clicked.connect(self.reject)

        type_label = Label("Tipo", "InputLabel")
        value_label = Label("Contato", "InputLabel")

        self.type_input = ComboBox() # Removido argumento posicional
        self.type_input.addItems(["Email", "Celular", "Telefone fixo"])
        self.type_input.updateSize()
        
        self.type_input.currentIndexChanged.connect(self.updateInputMask)
        
        self.value_input = LineEdit()

        box_layout.addWidget(type_label, 0, 0)
        box_layout.addWidget(value_label, 0, 1)

        box_layout.addWidget(self.type_input, 1, 0)
        box_layout.addWidget(self.value_input, 1, 1)

        layout.addWidget(box)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(buttons_widget)

        if data and is_editing:
            self.type_input.setCurrentText(data.get("type", ""))
            self.value_input.setText(data.get("value", ""))

    def updateInputMask(self):
        self.value_input.clear()

        if self.type_input.currentText() == "Celular":
            self.value_input.setInputMask("(00) 00000-0000;_")
        elif self.type_input.currentText() == "Telefone fixo":
            self.value_input.setInputMask("(00) 0000-0000;_")

    def save_contact(self):
        contact_type = self.type_input.currentText()
        value = self.value_input.text()
        
        if self.parent_page:
            # Chama a função na PersonPage para adicionar/editar o item
            self.parent_page.addContactToTable(contact_type, value, self.row_index if self.is_editing else None)
        
        self.accept() # Fecha o diálogo

    def clearInputs(self):
        self.type_input.setCurrentIndex(0)
        self.value_input.clear()

# --- AddressWindow Modificada ---
class AddressWindow(QDialog):
    def __init__(self, parent=None, parent_page=None, data={}, is_editing=False):
        super().__init__(parent=parent)

        self.parent_page = parent_page
        self.is_editing = is_editing
        self.row_index = data.get("row_index") # Armazena o índice se for edição

        self.setWindowFlag(Qt.Window)
        self.setWindowTitle("Editar Endereço" if is_editing else "Adicionar Endereço")
        
        self.setFixedHeight(300)

        self.setMinimumWidth(500)
        self.setMaximumWidth(600)

        self.setStyleSheet("background: #F3F3F3 !important;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        box = GroupBox("Cadastro de endereço")
        box_layout = QGridLayout()
        box.setLayout(box_layout)

        buttons_widget, buttons = createWindowButtons()
        
        # Conexões dos botões para adicionar/editar
        buttons[0].setText("Salvar" if is_editing else "Adicionar")
        buttons[0].clicked.connect(self.save_address)
        buttons[1].clicked.connect(self.clearInputs)
        buttons[2].clicked.connect(self.reject)

        cep_label = Label("CEP", "InputLabel")
        estate_label = Label("Estado", "InputLabel")
        city_label = Label("Cidade", "InputLabel")
        neighborhood_label = Label("Bairro", "InputLabel")
        street_label = Label("Logradouro", "InputLabel")
        number_label = Label("Nº", "InputLabel")
        complement_label = Label("Complemento", "InputLabel")

        self.cep_input = LineEdit()
        search_input = PushButton("Procurar", icon_path="search.svg")
        self.estate_input = ComboBox()
        self.city_input = ComboBox()
        self.neighborhood_input = LineEdit()
        self.street_input = LineEdit()
        self.number_input = LineEdit()
        self.complement_input = LineEdit()

        search_input.clicked.connect(lambda x: cepAPI.searchCEP(self.cep_input,
        {"estate_input": self.estate_input, "city_input": self.city_input,
         "neighborhood_input": self.neighborhood_input, "street_input": self.street_input,
         "complement_input": self.complement_input}))

        self.cep_input.setInputMask("00000-000;_")

        location = locations.Location(self.estate_input, self.city_input)
        location.loadData()
        location.fillEstates()

        self.estate_input.currentIndexChanged.connect(lambda x: location.filterCities())
        self.city_input.lineEdit().editingFinished.connect(location.validateCity)

        box_layout.addWidget(cep_label, 0, 0)
        box_layout.addWidget(estate_label, 2, 0)
        box_layout.addWidget(city_label, 2, 1)
        box_layout.addWidget(neighborhood_label, 2, 2)
        box_layout.addWidget(street_label, 4, 0)
        box_layout.addWidget(number_label, 4, 1)
        box_layout.addWidget(complement_label, 4, 2)

        box_layout.addWidget(self.cep_input, 1, 0)
        box_layout.addWidget(search_input, 1, 1)
        box_layout.addWidget(self.estate_input, 3, 0)
        box_layout.addWidget(self.city_input, 3, 1)
        box_layout.addWidget(self.neighborhood_input, 3, 2)
        box_layout.addWidget(self.street_input, 5, 0)
        box_layout.addWidget(self.number_input, 5, 1)
        box_layout.addWidget(self.complement_input, 5, 2)

        box_layout.setColumnStretch(0, 2)
        box_layout.setColumnStretch(1, 2)
        box_layout.setColumnStretch(2, 3)

        layout.addWidget(box)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(buttons_widget)

        if data and is_editing:
            self.cep_input.setText(data.get("cep", ""))
            self.estate_input.setCurrentText(data.get("estate", ""))
            self.city_input.setCurrentText(data.get("city", ""))
            self.neighborhood_input.setText(data.get("neighborhood", ""))
            self.street_input.setText(data.get("street", ""))
            self.number_input.setText(data.get("number", ""))
            self.complement_input.setText(data.get("complement", ""))
            
    def save_address(self):
        cep = self.cep_input.text()
        estate = self.estate_input.currentText()
        city = self.city_input.currentText()
        neighborhood = self.neighborhood_input.text()
        street = self.street_input.text()
        number = self.number_input.text()
        complement = self.complement_input.text()
        
        if self.parent_page:
            # Chama a função na PersonPage para adicionar/editar o endereço
            self.parent_page.addAddressToTable(
                cep, street, number, neighborhood, city, estate, complement, 
                self.row_index if self.is_editing else None
            )
            
        self.accept()

    def clearInputs(self):
        self.cep_input.clear()
        self.estate_input.setCurrentIndex(0)
        self.city_input.setCurrentIndex(0)
        self.neighborhood_input.clear()
        self.street_input.clear()
        self.number_input.clear()
        self.complement_input.clear()