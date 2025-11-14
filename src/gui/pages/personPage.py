from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *
from src.utils import cepAPI, locations

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

        tab = Tab()
        
        search_tab = self.createSearchTab()
        edition_tab = self.createEditionTab()

        tab.addTab(search_tab, "Pesquisar", )
        tab.addTab(edition_tab, "Adicionar/Editar")

        layout.addWidget(labels_widget)
        layout.addWidget(tab)

    def createSearchTab(self):
        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        search_layout = QGridLayout()

        search_label = Label("Pesquisar", type="InputLabel")
        type_label = Label("Tipo de pessoa", type="InputLabel")

        search_input = LineEdit("Pesquise por uma pessoa")
        type_input = ComboBox(["Todos", "Cliente", "Fornecedor"])
        search_button = PushButton("Pesquisar", icon_path="search.svg", type="WithoutBackground")
        export_button = PushButton("Exportar", icon_path="download.svg", type="WithBackground")

        search_layout.addWidget(search_label, 0, 0)
        search_layout.addWidget(type_label, 0, 1)

        search_layout.addWidget(search_input, 1, 0)
        search_layout.addWidget(type_input, 1, 1)
        search_layout.addWidget(search_button, 1, 2)

        search_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 3)

        search_layout.addWidget(export_button, 1, 4)

        table = Table(["ID", "Nome", "CPF/CNPJ", "Preço"])

        search_layout.addWidget(table, 2, 0, 1, 4)
        
        layout.addLayout(search_layout)
        layout.addWidget(table)

        return widget
    
    def createEditionTab(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent !important;")

        widget = TabWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        buttons_widget, buttons = createWindowButtons()

        info_box = GroupBox("Informações de pessoa")
        info_layout = QGridLayout()
        info_box.setLayout(info_layout)

        name_label = Label("Nome", type="InputLabel")
        type_label = Label("Tipo de pessoa", type="InputLabel")
        document_label = Label("CPF", type="InputLabel")
        sex_label = Label("Sexo", type="InputLabel")
        birthday_label = Label("Data de nascimento", type="InputLabel")

        name_input = LineEdit()
        type_input = ComboBox(["Pessoa física", "Pessoa jurídica"])
        document_input = LineEdit()
        sex_input = ComboBox(["Masculino", "Feminino", "Outro"])
        birthday_input = QDateEdit(date=QDate.currentDate())
        birthday_input.setDisplayFormat("dd/MM/yyyy")

        document_input.setInputMask("000.000.000-00;_")

        info_layout.addWidget(name_label, 0, 0)
        info_layout.addWidget(type_label, 2, 0)
        info_layout.addWidget(document_label, 2, 1)
        info_layout.addWidget(sex_label, 2, 2)
        info_layout.addWidget(birthday_label, 2, 3)
        
        info_layout.addWidget(name_input, 1, 0, 1, 4)
        info_layout.addWidget(type_input, 3, 0)
        info_layout.addWidget(document_input, 3, 1)
        info_layout.addWidget(sex_input, 3, 2)
        info_layout.addWidget(birthday_input, 3, 3)
        info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        contact_box = GroupBox("Informações de contato")
        contact_layout = QVBoxLayout()
        contact_box.setLayout(contact_layout)

        contact_buttons_widget, contact_buttons, = createTableButtons()
        contact_table = Table(["ID", "Tipo", "Contato"])

        contact_buttons[0].clicked.connect(self.addContactWindow)
        contact_buttons[1].clicked.connect(self.editContactWindow)
        contact_buttons[2].clicked.connect(self.removeContactWindow)
        
        contact_layout.addWidget(contact_buttons_widget)
        contact_layout.addWidget(contact_table)

        address_box = GroupBox("Informações de endereço")
        address_layout = QVBoxLayout()
        address_box.setLayout(address_layout)

        address_buttons_widget, address_buttons = createTableButtons()
        address_table = Table(["ID", "Tipo", "Contato"])

        address_buttons[0].clicked.connect(self.addAddressWindow)
        address_buttons[1].clicked.connect(self.editAddressWindow)
        address_buttons[2].clicked.connect(self.removeAddressWindow)
        
        address_layout.addWidget(address_buttons_widget)
        address_layout.addWidget(address_table)

        layout.addWidget(info_box)
        layout.addWidget(contact_box)
        layout.addWidget(address_box)
        layout.addWidget(buttons_widget)

        scroll_area.setWidget(widget)

        return scroll_area
    
    def addContactWindow(self):
        self.contact_window = ContactWindow()
        self.contact_window.show()
    
    def editContactWindow(self):
        self.contact_window = ContactWindow(data={
            "type": "Celular",
            "value": "(31) 98914-3646"
        })
        self.contact_window.show()

    def removeContactWindow(self):
        pass

    def addAddressWindow(self):
        self.address_window = AddressWindow()
        self.address_window.show()

    def editAddressWindow(self):
        self.address_window = AddressWindow(data={
            "cep": "34012650",
            "estate": "MG",
            "city": "Nova Lima",
            "neighborhood": "Honório Bicalho",
            "street": "Rua da Máquina",
            "number": "60",
            "complement": ""    
        })
        self.address_window.show()

    def removeAddressWindow(self):
        pass

class ContactWindow(QWidget):
    def __init__(self, data={}):
        super().__init__()

        self.setMaximumHeight(200)

        self.setStyleSheet("background-color: #F3F3F3 !important;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        box = GroupBox("Cadastro de endereço")
        box_layout = QGridLayout()
        box.setLayout(box_layout)

        buttons_widget, buttons = createWindowButtons()

        type_label = Label("Tipo", "InputLabel")
        value_label = Label("Contato", "InputLabel")

        type_input = ComboBox(["Email", "Celular", "Telefone fixo"])
        value_input = LineEdit()

        box_layout.addWidget(type_label, 0, 0)
        box_layout.addWidget(value_label, 0, 1)

        box_layout.addWidget(type_input, 1, 0)
        box_layout.addWidget(value_input, 1, 1)

        layout.addWidget(box)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(buttons_widget)

        if data:
            type_input.setCurrentText(data["type"])
            value_input.setText(data["value"])

class AddressWindow(QWidget):
    def __init__(self, data={}):
        super().__init__()

        self.setMaximumHeight(300)

        self.setStyleSheet("background: #F3F3F3 !important;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        box = GroupBox("Cadastro de endereço")
        box_layout = QGridLayout()
        box.setLayout(box_layout)

        buttons_widget, buttons = createWindowButtons()

        cep_label = Label("CEP", "InputLabel")
        estate_label = Label("Estado", "InputLabel")
        city_label = Label("Cidade", "InputLabel")
        neighborhood_label = Label("Bairro", "InputLabel")
        street_label = Label("Logradouro", "InputLabel")
        number_label = Label("Nº", "InputLabel")
        complement_label = Label("Complemento", "InputLabel")

        cep_input = LineEdit()
        search_input = PushButton("Procurar", icon_path="search.svg")
        estate_input = ComboBox()
        city_input = ComboBox()
        neighborhood_input = LineEdit()
        street_input = LineEdit()
        number_input = LineEdit()
        complement_input = LineEdit()

        search_input.clicked.connect(lambda x: cepAPI.searchCEP(cep_input,
        {"estate_input": estate_input, "city_input": city_input,
         "neighborhood_input": neighborhood_input, "street_input": street_input,
         "complement_input": complement_input}))

        cep_input.setInputMask("00000-000;_")

        location = locations.Location(estate_input, city_input)
        location.loadData()
        location.fillEstates()

        estate_input.currentIndexChanged.connect(lambda x: location.filterCities())
        city_input.lineEdit().editingFinished.connect(location.validateCity)

        box_layout.addWidget(cep_label, 0, 0)
        box_layout.addWidget(estate_label, 2, 0)
        box_layout.addWidget(city_label, 2, 1)
        box_layout.addWidget(neighborhood_label, 2, 2)
        box_layout.addWidget(street_label, 4, 0)
        box_layout.addWidget(number_label, 4, 1)
        box_layout.addWidget(complement_label, 4, 2)

        box_layout.addWidget(cep_input, 1, 0)
        box_layout.addWidget(search_input, 1, 1)
        box_layout.addWidget(estate_input, 3, 0)
        box_layout.addWidget(city_input, 3, 1)
        box_layout.addWidget(neighborhood_input, 3, 2)
        box_layout.addWidget(street_input, 5, 0)
        box_layout.addWidget(number_input, 5, 1)
        box_layout.addWidget(complement_input, 5, 2)

        layout.addWidget(box)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(buttons_widget)

        if data:
            cep_input.setText(data["cep"])
            estate_input.setCurrentText(data["estate"])
            city_input.setCurrentText(data["city"])
            neighborhood_input.setText(data["neighborhood"])
            street_input.setText(data["street"])
            number_input.setText(data["number"])
            complement_input.setText(data["complement"])