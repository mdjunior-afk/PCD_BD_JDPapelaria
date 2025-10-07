from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIcon
import requests, json

from utils.LocationInput import Location

from ..widgets import *

class BaseDialog(QDialog):
    def __init__(self, maximum_width=600):
        super().__init__()

        self.setStyleSheet("background-color: #D9D9D9; color: #747474;")

        self.maximum_width = maximum_width
        
        self.setFixedHeight(700)

        self.setMinimumWidth(self.maximum_width + 100)
        self.setMaximumWidth(self.maximum_width + 200)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.input_layout = QGridLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        self.buttons_layout = QHBoxLayout()

        self.button_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.save_btn = PageButton("Salvar", icon_path="disk.svg")
        self.new_btn = PageButton("Novo", icon_path="plus.svg")
        self.cancel_btn = PageButton("Cancelar", icon_path="cross.svg")

        self.buttons_layout.addItem(self.button_spacer)
        self.buttons_layout.addWidget(self.save_btn)
        self.buttons_layout.addWidget(self.new_btn)
        self.buttons_layout.addWidget(self.cancel_btn)

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.buttons_layout)

    def save(self):
        pass

class ProductDialog(BaseDialog):
    def __init__(self):
        super().__init__()

        self.tab = QTabWidget()
        self.product_info_tab = self.createTabs()
        self.tab.addTab(self.product_info_tab, "Informações do produto")

        self.input_layout.addWidget(self.tab)

    def createTabs(self):
        product_info_tab = QWidget()
        supplier_info_tab = QWidget()

        product_info_layout = QVBoxLayout()
        product_widget, product_inputs = self.productInfoInputs()

        product_info_layout.addWidget(product_widget)
        product_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        product_info_tab.setLayout(product_info_layout)

        return product_info_tab
    
    def productInfoInputs(self):
        widget = QWidget()
        layout = QGridLayout()

        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(6)
        layout.setContentsMargins(5, 5, 5, 5)

        widget.setLayout(layout)

        product_info_widget = GroupBox("Informações gerais")
        product_info_layout = QGridLayout()

        name_label = Label("Nome:")
        barcode_label = Label("Cód. Barra:")
        category_label = Label("Categoria:")

        name_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        barcode_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        category_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        name_input = DefaultLineEdit()
        barcode_input = DefaultLineEdit()
        category_input = ComboBox(["Pen-Drives", "Carregadores", "Canetas", "Cadernos"], True)

        product_info_layout.addWidget(name_label, 0, 0)
        product_info_layout.addWidget(name_input, 0, 1, 1, 3)
        product_info_layout.addWidget(category_label, 1, 0)
        product_info_layout.addWidget(category_input, 1, 1)
        product_info_layout.addWidget(barcode_label, 1, 2)
        product_info_layout.addWidget(barcode_input, 1, 3)

        product_info_widget.setLayout(product_info_layout)

        product_price_widget = GroupBox("Informações de preço")
        product_price_layout = QGridLayout()

        purchase_price_label = Label("Compra: R$")
        adjust_price_label = Label("Reajuste:")
        sell_price_label = Label("Venda: R$")
        
        purchase_price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        adjust_price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sell_price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        purchase_price_input = DoubleSpinBox()
        adjust_price_input = DoubleSpinBox()
        sell_price_input = DoubleSpinBox()

        product_price_layout.addWidget(purchase_price_label, 0, 0)
        product_price_layout.addWidget(purchase_price_input, 0, 1)
        product_price_layout.addWidget(adjust_price_label, 0, 2)
        product_price_layout.addWidget(adjust_price_input, 0, 3)
        product_price_layout.addWidget(sell_price_label, 0, 4)
        product_price_layout.addWidget(sell_price_input, 0, 5)

        product_price_widget.setLayout(product_price_layout)

        # Stock widget
        product_stock_widget = GroupBox("Informações de estoque")
        product_stock_layout = QGridLayout()

        minimum_stock_label = Label("Estoque mínimo:")
        current_stock_label = Label("Estoque atual:")

        minimum_stock_input = SpinBox()
        current_stock_input = SpinBox()

        product_stock_layout.addWidget(minimum_stock_label, 0, 0)
        product_stock_layout.addWidget(minimum_stock_input, 0, 1)
        product_stock_layout.addWidget(current_stock_label, 0, 4)
        product_stock_layout.addWidget(current_stock_input, 0, 5)
        product_stock_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2, 1, 2)

        product_stock_widget.setLayout(product_stock_layout)

        # Supplier widget
        supplier_info_widget = GroupBox("Informações do fornecedor")
        supplier_info_layout = QGridLayout()

        supplier_validate_date_label = Label("Data de validade:")

        supplier_search_input = LineEdit()
        supplier_search_input.setMaximumWidth(1000)
        supplier_search_input.setPlaceholderText("Procure por um fornecedor")

        supplier_validate_date_input = DateEdit()
        add_btn = PageButton("Adicionar", icon_path="plus.svg")
        remove_btn = PageButton("Remover", icon_path="cross.svg")

        supplier_table = TableWidget(["Data", "CNPJ", "Razão Social", "Data de validade"])
        supplier_table.setMinimumHeight(100)

        supplier_info_layout.addWidget(supplier_search_input, 0, 0, 1, 5)
        supplier_info_layout.addWidget(supplier_validate_date_label, 1, 0)
        supplier_info_layout.addWidget(supplier_validate_date_input, 1, 1)
        supplier_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2)
        supplier_info_layout.addWidget(add_btn, 1, 3)
        supplier_info_layout.addWidget(remove_btn, 1, 4)
        supplier_info_layout.addWidget(supplier_table, 2, 0, 1, 5)

        supplier_info_widget.setLayout(supplier_info_layout)

        layout.addWidget(product_info_widget)
        layout.addWidget(product_price_widget)
        layout.addWidget(product_stock_widget)
        layout.addWidget(supplier_info_widget)

        return widget, ()

class PeopleDialog(BaseDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cadastro de Pessoa")

        self.tab = QTabWidget()
        self.people_info_tab = self.createTabs()
        self.tab.addTab(self.people_info_tab, "Informações da pessoa")

        self.input_layout.addWidget(self.tab)

    def createTabs(self):
        people_info_tab = QWidget()

        people_info_layout = QVBoxLayout()
        people_widget, people_inputs = self.peopleInfoInputs()

        people_info_layout.addWidget(people_widget)
        people_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        people_info_tab.setLayout(people_info_layout)

        return people_info_tab
    
    def peopleInfoInputs(self):
        widget = QWidget()
        layout = QGridLayout()

        widget.setLayout(layout)

        person_info_widget = GroupBox("Informações Gerais")
        person_info_layout = QGridLayout()

        name_label = Label("Nome:")
        person_type_label = Label("Tipo de pessoa:")
        self.document_label = Label("CPF:")
        sex_label = Label("Sexo:")
        birthday_label = Label("Nascimento:")
        cellphone_label = Label("Celular:")
        email_label = Label("Email:")
        
        name_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        person_type_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.document_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sex_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        birthday_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cellphone_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        email_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        name_input = DefaultLineEdit()
        person_type_input = ComboBox(["PF", "PJ"])
        person_type_input.currentIndexChanged.connect(self.onIndexChanged)
        self.document_input = DefaultLineEdit()
        self.document_input.setInputMask("000.000.000-00;_")
        sex_input = ComboBox(["Masculino", "Feminino", "Outro"])
        birthday_input = DateEdit()
        
        # Contact inputs
        cellphone_input = DefaultLineEdit()
        cellphone_input.setInputMask("(00) 00000-0000;_")
        email_input = DefaultLineEdit()

        person_info_layout.addWidget(name_label, 0, 0)
        person_info_layout.addWidget(name_input, 0, 1, 1, 3)
        person_info_layout.addWidget(person_type_label, 1, 0)
        person_info_layout.addWidget(person_type_input, 1, 1)
        person_info_layout.addWidget(self.document_label, 1, 2)
        person_info_layout.addWidget(self.document_input, 1, 3)
        person_info_layout.addWidget(sex_label, 2, 0)
        person_info_layout.addWidget(sex_input, 2, 1)
        person_info_layout.addWidget(birthday_label, 2, 2)
        person_info_layout.addWidget(birthday_input, 2, 3)
        person_info_layout.addWidget(email_label, 3, 0)
        person_info_layout.addWidget(email_input, 3, 1)
        person_info_layout.addWidget(cellphone_label, 3, 2)
        person_info_layout.addWidget(cellphone_input, 3, 3)

        person_info_widget.setLayout(person_info_layout)
        
        # Address inputs
        address_widget = GroupBox("Informações de Endereço:")
        address_layout = QGridLayout()

        cep_label = Label("CEP:")
        self.warning_label = Label("")
        estate_label = Label("Estado:")
        city_label = Label("Cidade:")
        neighborhood_label = Label("Bairro:")
        number_label =  Label("Número:")
        street_label = Label("Rua:")
        complement_label = Label("Complemento:")

        cep_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        estate_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        city_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        neighborhood_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        number_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        street_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        complement_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.cep_input = DefaultLineEdit()
        self.cep_input.setInputMask("00000-000")
        search_btn = PageButton("Procurar", icon_path="search.svg")
        search_btn.clicked.connect(self.searchCEP)
        self.estate_input = ComboBox()
        self.city_input = ComboBox()
        self.neighborhood_input = DefaultLineEdit()
        self.number_input =  DefaultLineEdit()
        self.street_input = DefaultLineEdit()
        self.complement_input = DefaultLineEdit()

        self.add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.remove_btn = PageButton("Remover", icon_path="cross.svg")
        self.add_btn.clicked.connect(self.addAddress)

        self.address_table = TableWidget(["CEP", "Rua", "Nº", "Complemento", "Bairro", "Cidade", "Estado" ])
        self.address_table.setFixedHeight(150)
        self.address_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.address_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

        self.location = Location(self.estate_input, self.city_input)
        self.location.loadData()
        self.location.fillEstates()

        self.estate_input.currentIndexChanged.connect(lambda i: self.location.filterCities())
        self.city_input.lineEdit().editingFinished.connect(self.location.validateCity)

        address_layout.addWidget(cep_label, 0, 0)
        address_layout.addWidget(self.cep_input, 0, 1)
        address_layout.addWidget(search_btn, 0, 2)
        address_layout.addWidget(self.warning_label, 0, 3)
        address_layout.addWidget(estate_label, 1, 0)
        address_layout.addWidget(self.estate_input, 1, 1)
        address_layout.addWidget(city_label, 1, 2)
        address_layout.addWidget(self.city_input, 1, 3, 1, 2)
        address_layout.addWidget(number_label, 2, 0)
        address_layout.addWidget(self.number_input, 2, 1)
        address_layout.addWidget(neighborhood_label, 2, 2)
        address_layout.addWidget(self.neighborhood_input, 2, 3, 1, 2)
        address_layout.addWidget(street_label, 3, 0)
        address_layout.addWidget(self.street_input, 3, 1, 1, 4)
        address_layout.addWidget(complement_label, 4, 0)
        address_layout.addWidget(self.complement_input, 4, 1, 1, 4)
        address_layout.addWidget(self.add_btn, 5, 3)
        address_layout.addWidget(self.remove_btn, 5, 4)
        address_layout.addWidget(self.address_table, 6, 0, 1, address_layout.columnCount())

        address_layout.setColumnStretch(3, 2)

        address_widget.setLayout(address_layout)

        layout.addWidget(person_info_widget, 0, 0)
        layout.addWidget(address_widget, 1, 0)

        return widget, ()
    
    def addAddress(self):
        row_index = self.address_table.rowCount()
        self.address_table.insertRow(row_index)

        self.address_table.setItem(row_index, 0, QTableWidgetItem(self.cep_input.text()))
        self.address_table.setItem(row_index, 1, QTableWidgetItem(self.street_input.text()))
        self.address_table.setItem(row_index, 2, QTableWidgetItem(self.number_input.text()))
        self.address_table.setItem(row_index, 3, QTableWidgetItem(self.complement_input.text()))
        self.address_table.setItem(row_index, 4, QTableWidgetItem(self.neighborhood_input.text()))
        self.address_table.setItem(row_index, 5, QTableWidgetItem(self.city_input.currentText()))
        self.address_table.setItem(row_index, 6, QTableWidgetItem(self.estate_input.currentText()))
    
    def onIndexChanged(self, index):
        if index == 0:
            self.document_input.setInputMask("000.000.000-00;_")
            self.document_label.setText("CPF")
            self.document_input.clear()
        elif index == 1:
            self.document_input.setInputMask("00.000.000/0000-00;_")
            self.document_label.setText("CNPJ")
            self.document_input.clear()

    def searchCEP(self):
        cep = self.cep_input.text()
        self.warning_label.setText("Consultando...")

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
            self.warning_label.setText("")
            QApplication.restoreOverrideCursor()

class TransactionDialog(BaseDialog):
    def __init__(self, maximum_width=800, maximum_height=800, initial_window=0):
        super().__init__(maximum_width)

        self.initial_window = initial_window
        self.setMaximumSize(maximum_width, maximum_height)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Movimentação")

        # --- Data ---
        self.date_widget = QWidget()
        self.date_layout = QHBoxLayout()
        self.date_layout.setContentsMargins(0, 0, 0, 6)

        self.date = DateEdit()
        self.date_layout.addWidget(Label("Data da venda:"))
        self.date_layout.addWidget(self.date)
        self.date_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.date_widget.setLayout(self.date_layout)

        # --- Cliente ---
        self.people_info_widget = QWidget()
        self.people_info_layout = QVBoxLayout()

        self.search_people = LineEdit("Procure por um cliente")
        self.search_people.setMaximumWidth(800)
        self.people_info_layout.addWidget(self.search_people)
        self.people_info_widget.setLayout(self.people_info_layout)

        # --- Tabs ---
        self.tab = QTabWidget()
        self.product_tab, self.service_tab, self.payment_tab = self.createTabs()
        self.tab.addTab(self.product_tab, "Produtos")
        self.tab.addTab(self.service_tab, "Serviços")
        self.tab.addTab(self.payment_tab, "Pagamentos")

        # -- Total --
        self.total_info_widget = QWidget()
        self.total_info_layout = QHBoxLayout()

        self.total_input = DoubleSpinBox()
        self.total_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.total_input.setReadOnly(True)

        self.total_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.total_info_layout.addWidget(Label("Total: R$"))
        self.total_info_layout.addWidget(self.total_input)
        self.total_info_widget.setLayout(self.total_info_layout)

        self.input_layout.addWidget(self.date_widget)
        self.input_layout.addWidget(self.people_info_widget)
        self.input_layout.addWidget(self.tab)
        self.input_layout.addWidget(self.total_info_widget)
        self.tab.setCurrentIndex(self.initial_window)

        # --- ReturnData ---
        self.return_data = ReturnData(self)
        self.updateReturnDataTarget(self.initial_window)
        self.tab.currentChanged.connect(self.updateReturnDataTarget)

    def clearFields(self, fields: list):
        for f in fields:
            if isinstance(f, QLineEdit):
                if f.isReadOnly():
                    f.setReadOnly(False)
                    f.clear()
            elif isinstance(f, (QSpinBox, QDoubleSpinBox)):
                f.setValue(0)

        self.return_data.hide()

    def searchItems(self, data: list, targets: dict, search_widget: QLineEdit):
        if not search_widget.text():
            self.return_data.hide()
            return
        self.return_data.setTarget(targets)
        self.return_data.showData(data)

        # Posiciona o dropdown
        pos_global = search_widget.mapToGlobal(QPoint(0, search_widget.height()))
        pos_local = self.mapFromGlobal(pos_global)
        self.return_data.move(pos_local)
        self.return_data.setFixedWidth(search_widget.width())

    def updateReturnDataTarget(self, index):
        if index == 0:  # Produtos
            targets = {
                "nome": self.product_search_input,
                "quantidade": self.product_quantity_input,
                "valor": self.product_price_input,
                "subtotal": self.product_subtotal_input
            }
        elif index == 1:  # Serviços
            targets = {
                "nome": self.service_search_input,
                "quantidade": self.service_quantity_input,
                "valor": self.service_price_input,
                "subtotal": self.service_subtotal_input
            }
        else:
            targets = {}
        
        self.return_data.setTarget(targets)

    # ----------------------
    # --- Criar Tabs
    # ----------------------
    def createTabs(self):
        product_tab = QWidget()
        service_tab = QWidget()
        payment_tab = QWidget()

        # --- Produtos ---
        product_layout = QVBoxLayout()
        product_info_widget, product_search, product_inputs = self.createProductInputs()
        self.product_search_input = product_search
        self.product_price_input, self.product_quantity_input, self.product_subtotal_input = product_inputs

        product_layout.addWidget(product_info_widget)
        product_layout.addWidget(TableWidget(["Nome", "Quantidade", "Preço", "Total"]))
        product_tab.setLayout(product_layout)

        # Conecta search e clear
        self.setupSearch(product_search, product_inputs, data=[
            {"nome": "PENDRIVE SAMSUNG 8G", "quantidade": 1, "valor": 39.90},
            {"nome": "PENDRIVE SANDISK 16GB", "quantidade": 1, "valor": 59.90}
        ])

        # --- Serviços ---
        service_layout = QVBoxLayout()
        service_info_widget, service_search, service_inputs = self.createServiceInputs()
        self.service_search_input = service_search
        self.service_price_input, self.service_quantity_input, self.service_subtotal_input = service_inputs

        service_layout.addWidget(service_info_widget)
        service_layout.addWidget(TableWidget(["Tipo", "Quantidade", "Preço", "Total"]))
        service_tab.setLayout(service_layout)

        # Conecta search e clear
        self.setupSearch(service_search, service_inputs, data=[
            {"nome": "XEROX", "quantidade": 1, "valor": 0.50},
            {"nome": "CURRÍCULO", "quantidade": 10, "valor": 10}
        ])

        payment_layout = QVBoxLayout()
        payment_info_widget, document_input = self.createPaymentInputs()

        payment_layout.addWidget(payment_info_widget)
        payment_layout.addWidget(TableWidget(["Data", "Documento", "Valor"]))
        payment_tab.setLayout(payment_layout)

        return product_tab, service_tab, payment_tab

    # ----------------------
    # --- Helpers Inputs
    # ----------------------
    def createProductInputs(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        search_input = LineEdit("Procure por um produto...")
        search_input.setMaximumWidth(self.maximum_width)

        price_input = DoubleSpinBox()
        quantity_input = SpinBox()
        subtotal_input = DoubleSpinBox()
        subtotal_input.setReadOnly(True)
        subtotal_input.setButtonSymbols(QAbstractSpinBox.NoButtons)

        layout.addWidget(search_input, 0, 0, 1, 9)
        layout.addWidget(Label("Preço: R$"), 1, 0)
        layout.addWidget(price_input, 1, 1)
        layout.addWidget(Label("Quantidade:"), 1, 2)
        layout.addWidget(quantity_input, 1, 3)
        layout.addWidget(Label(" = "), 1, 4)
        layout.addWidget(subtotal_input, 1, 5)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 6)
        layout.addWidget(PageButton("Adicionar", icon_path="plus.svg"), 1, 7)
        layout.addWidget(PageButton("Remover", icon_path="cross.svg"), 1, 8)

        return widget, search_input, (price_input, quantity_input, subtotal_input)

    def createServiceInputs(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        search_input = LineEdit("Procure por um serviço...")
        search_input.setMaximumWidth(self.maximum_width)

        price_input = DoubleSpinBox()
        quantity_input = SpinBox()
        subtotal_input = DoubleSpinBox()
        subtotal_input.setReadOnly(True)
        subtotal_input.setButtonSymbols(QAbstractSpinBox.NoButtons)

        layout.addWidget(search_input, 0, 0, 1, 9)
        layout.addWidget(Label("Preço: R$"), 1, 0)
        layout.addWidget(price_input, 1, 1)
        layout.addWidget(Label("Quantidade:"), 1, 2)
        layout.addWidget(quantity_input, 1, 3)
        layout.addWidget(Label(" = "), 1, 4)
        layout.addWidget(subtotal_input, 1, 5)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 6)
        layout.addWidget(PageButton("Adicionar", icon_path="plus.svg"), 1, 7)
        layout.addWidget(PageButton("Remover", icon_path="cross.svg"), 1, 8)

        return widget, search_input, (price_input, quantity_input, subtotal_input)
    
    def createPaymentInputs(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        document_input = ComboBox(["PIX", "Cartão de Crédito", "Cartão de Débito"], True)
        value_input = DoubleSpinBox()

        layout.addWidget(Label("Documento:"), 0, 0)
        layout.addWidget(document_input, 0, 1)
        layout.addWidget(Label("Valor: R$"), 0, 2)
        layout.addWidget(value_input, 0, 3)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 4)
        layout.addWidget(PageButton("Adicionar", icon_path="plus.svg"), 0, 5)
        layout.addWidget(PageButton("Remover", icon_path="cross.svg"), 0, 6)

        return widget, (document_input, value_input)

    # ----------------------
    # --- Configura Search
    # ----------------------
    def setupSearch(self, search_widget, inputs, data):
        # Botão de limpar
        clear_action = search_widget.addAction(QIcon.fromTheme("window-close"), QLineEdit.TrailingPosition)
        clear_action.triggered.connect(lambda: self.clearFields([search_widget, *inputs]))

        # Conecta textChanged
        search_widget.textChanged.connect(
            lambda text: self.searchItems(data,
                                          {"nome": search_widget,
                                           "quantidade": inputs[1],
                                           "valor": inputs[0],
                                           "subtotal": inputs[2]},
                                          search_widget)
        )
