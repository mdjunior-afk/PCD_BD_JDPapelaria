from PySide6.QtWidgets import *

from ..widgets import *
from ..config import *

from .Dialogs import *

class PeoplePage(QWidget):
    def __init__(self):
        super().__init__()

        self.document_input = None
        self.addressWindow = None
        self.contactWindow = None

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
        inputs_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
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

        edit_tab_layout.addWidget(edit_widget)

        edit_tab.setLayout(edit_tab_layout)

        tab = Tab()
        tab.addTab(search_tab, "Consulta de pessoas")
        tab.addTab(filter_tab, "Consulta com filtros")
        tab.addTab(edit_tab, "Adicionar/Editar pessoas")

        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(tab)

        self.setLayout(layout)

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
        self.document_label = Label("CPF:")
        sex_label = Label("Sexo:")
        birth_date_label = Label("Nascimento:")

        name_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        person_type_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.document_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sex_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        birth_date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        name_input = SearchInput(placeholder="", max_width=1200)
        person_type_input = ComboBox(["Pessoa Física", "Pessoa Jurídica"])
        self.document_input = SearchInput(max_width=1200);
        sex_input = ComboBox(["Masculino", "Feminino", "Outro"])
        birth_date_input = DateEdit()

        self.document_input.setInputMask("000.000.000-00;_")

        person_type_input.currentIndexChanged.connect(self.onIndexChanged)

        info_layout.addWidget(name_label, 0, 0)
        info_layout.addWidget(name_input, 0, 1, 1, 3)
        info_layout.addWidget(person_type_label, 1, 0)
        info_layout.addWidget(person_type_input, 1, 1)
        info_layout.addWidget(self.document_label, 1, 2)
        info_layout.addWidget(self.document_input, 1, 3)
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

        address_table = TableWidget(["ID", "CEP", "Rua", "Número", "Complemento", "Bairro", "Cidade", "Estado"])

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

    def onIndexChanged(self, index):
        if index == 0:
            self.document_input.setInputMask("000.000.000-00;_")
            self.document_label.setText("CPF")
            self.document_input.clear()
        elif index == 1:
            self.document_input.setInputMask("00.000.000/0000-00;_")
            self.document_label.setText("CNPJ")
            self.document_input.clear()

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

        buttons_widget = create_add_buttons()

        layout.addWidget(main_group)
        layout.addWidget(buttons_widget)

    def editContactWindow(self):
        pass

    def removeContactWindow(self):
        pass

    def addAddressWindow(self):
        self.addressWindow = AddressWindow()
        self.addressWindow.show()

    def editAddressWindow(self):
        pass

    def removeAddressWindow(self):
        pass

class AddressWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; color: {TEXT_COLOR}")

        main_layout = QVBoxLayout()

        widget = GroupBox("Informações de endereço")
        layout = QGridLayout()

        widget.setLayout(layout)

        cep_label = Label("CEP:")
        estate_label = Label("Estado:")
        city_label = Label("Cidade:")
        neighborhood_label = Label("Bairro:")
        street_label = Label("Rua:")
        number_label = Label("Número:")
        complement_label = Label("Complemento:")

        self.cep_input = SearchInput()
        self.cep_input.setInputMask("00000-000;_")
        search_input = Button("Procurar", icon_path="search.svg")
        self.estate_input = ComboBox()
        self.city_input = ComboBox()
        self.neighborhood_input = SearchInput()
        self.street_input = SearchInput()
        number_input = SearchInput()
        self.complement_input = SearchInput()

        search_input.clicked.connect(self.searchCEP)

        layout.addWidget(cep_label, 0, 0)
        layout.addWidget(self.cep_input, 0, 1)
        layout.addWidget(search_input, 0, 2)
        layout.addWidget(estate_label, 1, 0)
        layout.addWidget(self.estate_input, 1, 1)
        layout.addWidget(city_label, 1, 2)
        layout.addWidget(self.city_input, 1, 3)
        layout.addWidget(neighborhood_label, 2, 0)
        layout.addWidget(self.neighborhood_input, 2, 1, 1, 3)
        layout.addWidget(street_label, 3, 0)
        layout.addWidget(self.street_input, 3, 1)
        layout.addWidget(number_label, 3, 2)
        layout.addWidget(number_input, 3, 3)
        layout.addWidget(complement_label, 4, 0)
        layout.addWidget(self.complement_input, 4, 1, 1, 3)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 5, 0)

        buttons = create_add_buttons()

        main_layout.addWidget(widget)
        main_layout.addWidget(buttons)

        self.setLayout(main_layout)

    def searchCEP(self):
        cep = self.cep_input.text()
        #self.warning_label.setText("Consultando...")

        cep = ''.join(filter(str.isdigit, cep))

        if len(cep) != 8:
            print("ERRO")
            return

        url = f"https://viacep.com.br/ws/{cep}/json/"

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'erro' in data and data['erro']:
                print(f"CEP não encontrado!")
                return

            uf_do_cep = data['uf']
            estate_index = self.estate_input.findData(uf_do_cep)

            if estate_index >= 0:
                self.estate_input.setCurrentIndex(estate_index)

                city = data['localidade']

                city_index = self.city_input.findText(city, Qt.MatchFlag.MatchExactly)
                if city_index >= 0:
                    self.city_input.setCurrentIndex(city_index)
                else:
                    self.city_input.lineEdit().setText(city)

            self.neighborhood_input.setText(data["bairro"])
            self.street_input.setText(data["logradouro"])

        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar o ViaCEP: {e}")
            return None
        except json.JSONDecodeError:
            print("Erro ao decodificar a resposta JSON.")
            return None
        finally:
            #self.warning_label.setText("")
            QApplication.restoreOverrideCursor()
