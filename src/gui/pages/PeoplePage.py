from PySide6.QtWidgets import *

from ..widgets import *

from .Dialogs import *

class PeoplePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        page_title = Label("Painel de Pessoas", property="Title", fixed=False)
        page_subtitle = Label("Gerencie todas as pessoas cadastradas", property="Subtitle", fixed=False)

        search_tab = QTabWidget()
        search_layout = QVBoxLayout()

        inputs_widget = QWidget()
        inputs_layout = QHBoxLayout()

        search_label = Label("Pesquise:", property="NormalBolder", fixed=False)
        type_label = Label("Tipo:", property="NormalBolder", fixed=False)

        search_input = SearchInput(placeholder="")
        type_input = ComboBox(["Todos", "Clientes", "Fornecedores"])
        search_button = Button("Pesquisar", property="WithoutBackground")
        export_button = Button("Exportar", icon_path="download.svg")

        inputs_layout.addWidget(search_label)
        inputs_layout.addWidget(search_input)
        inputs_layout.addWidget(type_label)
        inputs_layout.addWidget(type_input)
        inputs_layout.addWidget(search_button)
        inputs_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        inputs_layout.addWidget(export_button)

        inputs_widget.setLayout(inputs_layout)

        table = TableWidget(["ID", "CPF/CNPJ", "Nome", "Contato", "Endereço"])
        
        search_layout.addWidget(inputs_widget)
        search_layout.addWidget(table)

        search_tab.setLayout(search_layout)

        filter_tab = TabWidget()

        edit_tab = TabWidget()
        edit_tab_layout = QVBoxLayout()

        edit_widget = self.createEditInputs()
        add_buttons_widget = self.createAddButtons()

        edit_tab_layout.addWidget(edit_widget)
        edit_tab_layout.addWidget(add_buttons_widget)

        edit_tab.setLayout(edit_tab_layout)

        tab = Tab()
        tab.addTab(search_tab, "Consulta de pessoas")
        tab.addTab(filter_tab, "Consulta com filtros")
        tab.addTab(edit_tab, "Adicionar/Editar pessoas")

        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(tab)

        self.setLayout(layout)

    def createAddButtons(self):
        widget = QWidget()
        widget.setStyleSheet("background: none;")
        layout = QHBoxLayout()

        add_button = Button("Salvar", icon_path="disk.svg")
        edit_button = Button("Novo", icon_path="plus.svg")
        remove_button = Button("Cancelar", icon_path="cross.svg")

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(remove_button)

        widget.setLayout(layout)

        return widget

    def createEditInputs(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent !important;")

        widget = QWidget()
        widget.setStyleSheet("background: transparent !important;")
        layout = QVBoxLayout()

        info_box = GroupBox("Informações da pessoa")
        info_layout = QGridLayout()

        name_label = Label("Nome:")
        person_type_label = Label("Tipo:")
        document_label = Label("CPF:")
        sex_label = Label("Sexo:")
        birth_date_label = Label("Nascimento:")

        name_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        person_type_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        document_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sex_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        birth_date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        name_input = SearchInput(placeholder="", max_width=1200)
        person_type_input = ComboBox(["Pessoa Física", "Pessoa Jurídica"])
        document_input = SearchInput(max_width=1200);
        sex_input = ComboBox(["Masculino", "Feminino", "Outro"])
        birth_date_input = DateEdit()

        document_input.setInputMask("000.000.000-00;_")

        info_layout.addWidget(name_label, 0, 0)
        info_layout.addWidget(name_input, 0, 1, 1, 3)
        info_layout.addWidget(person_type_label, 1, 0)
        info_layout.addWidget(person_type_input, 1, 1)
        info_layout.addWidget(document_label, 1, 2)
        info_layout.addWidget(document_input, 1, 3)
        info_layout.addWidget(sex_label, 2, 0)
        info_layout.addWidget(sex_input, 2, 1)
        info_layout.addWidget(birth_date_label, 2, 2)
        info_layout.addWidget(birth_date_input, 2, 3)

        info_layout.setColumnStretch(1, 2)
        info_layout.setColumnStretch(3, 2)

        info_box.setLayout(info_layout)

        contact_box = GroupBox("Informações de contato")
        contact_layout = QGridLayout()

        # Contact Labels
        email_label = Label("Email:", property="NormalBolder")
        cellphone_label = Label("Telefone:", property="NormalBolder")

        email_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cellphone_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Contact Inputs
        contact_table = TableWidget(["ID", "Tipo", "Contato"])

        add_contact_button = Button("Adicionar", icon_path="plus.svg")
        edit_contact_button = Button("Editar", icon_path="edit.svg")
        remove_contact_button = Button("Remover", icon_path="cross.svg")

        add_contact_button.clicked.connect(self.addContactWindow)
        edit_contact_button.clicked.connect(self.editContactWindow)
        remove_contact_button.clicked.connect(self.removeContactWindow)

        contact_layout.addWidget(add_contact_button, 0, 0)
        contact_layout.addWidget(edit_contact_button, 0, 1)
        contact_layout.addWidget(remove_contact_button, 0, 2)
        contact_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 3)
        contact_layout.addWidget(contact_table, 1, 0, 1, 4)

        contact_box.setLayout(contact_layout)

        address_box = GroupBox("Informações de endereço")
        address_layout = QGridLayout()

        cep_label = Label("CEP:")
        estate_label = Label("Estado:")
        city_label = Label("Cidade:")
        neighborhood_label = Label("Bairro:")
        street_label = Label("Rua:")
        number_label = Label("Número:")
        complement_label = Label("Complemento:")

        cep_input = SearchInput()
        search_input = Button("Procurar", icon_path="search.svg")
        estate_input = ComboBox()
        city_input = ComboBox()
        neighborhood_input = SearchInput()
        street_input = SearchInput()
        number_input = SearchInput()
        complement_input = SearchInput()
        address_table = TableWidget(["ID", "CEP", "Rua", "Número", "Complemento", "Bairro", "Cidade", "Estado"])

        """address_layout.addWidget(cep_label, 0, 0)
        address_layout.addWidget(cep_input, 0, 1)
        address_layout.addWidget(search_input, 0, 2)
        address_layout.addWidget(estate_label, 1, 0)
        address_layout.addWidget(estate_input, 1, 1)
        address_layout.addWidget(city_label, 1, 2)
        address_layout.addWidget(city_input, 1, 3)
        address_layout.addWidget(neighborhood_label, 2, 0)
        address_layout.addWidget(neighborhood_input, 2, 1, 1, 3)
        address_layout.addWidget(street_label, 3, 0)
        address_layout.addWidget(street_input, 3, 1)
        address_layout.addWidget(number_label, 3, 2)
        address_layout.addWidget(number_input, 3, 3)
        address_layout.addWidget(complement_label, 4, 0)
        address_layout.addWidget(complement_input, 4, 1, 1, 3)
        address_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))"""

        add_address_button = Button("Adicionar", icon_path="plus.svg")
        edit_address_button = Button("Editar", icon_path="edit.svg")
        remove_address_button = Button("Remover", icon_path="cross.svg")

        add_address_button.clicked.connect(self.addAddressWindow)
        edit_address_button.clicked.connect(self.editAddressWindow)
        remove_address_button.clicked.connect(self.removeAddressWindow)

        address_layout.addWidget(add_address_button, 0, 0)
        address_layout.addWidget(edit_address_button, 0, 1)
        address_layout.addWidget(remove_address_button, 0, 2)
        address_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 3)
        address_layout.addWidget(address_table, 1, 0, 1, 4)

        address_box.setLayout(address_layout)

        layout.addWidget(info_box)
        layout.addWidget(contact_box)
        layout.addWidget(address_box)

        widget.setLayout(layout)

        scroll_area.setWidget(widget)

        return scroll_area

    def updateSellPrice(self):
        purchase = self.purchase_input.value()
        adjust = self.adjust_input.value()

        self.sell_input.setValue(purchase + (purchase * (adjust / 100)))

    def updateAdjustPrice(self):
        sell = self.sell_input.value()
        purchase = self.purchase_input.value()

        self.adjust_input.setValue(((sell/purchase) - 1) * 100)

    def addContactWindow(self):
        widget = QWidget()
        layout = QVBoxLayout()

        widget.setLayout(layout)

        main_group = GroupBox("Cadastrar contato")
        main_layout = QGridLayout()

        main_group.setLayout(main_layout)

        type_label = Label("Tipo:")
        value_label = Label("Celular:")

        type_input = ComboBox(["Celular", "Email"])
        value_input = SearchInput()

        layout.addWidget(type_label)

        main_layout.addWidget(type_label, 0, 0)
        main_layout.addWidget(type_input, 0, 1)
        main_layout.addWidget(value_label, 0, 2)
        main_layout.addWidget(value_input, 0, 3)

        buttons_widget = self.createAddButtons()

        layout.addWidget(main_group)
        layout.addWidget(buttons_widget)

    def editContactWindow(self):
        pass

    def removeContactWindow(self):
        pass

    def addAddressWindow(self):
        pass

    def editAddressWindow(self):
        pass

    def removeAddressWindow(self):
        pass