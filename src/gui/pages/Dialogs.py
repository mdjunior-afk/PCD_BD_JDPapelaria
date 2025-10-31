from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIcon
import requests, json

from utils.LocationInput import Location

from ..widgets import *

class BaseDialog(QDialog):
    def __init__(self, maximum_width=800):
        super().__init__()

        self.setStyleSheet("background-color: #D9D9D9; color: #747474;")

        self.maximum_width = maximum_width
        
        self.setFixedHeight(700)

        self.setMinimumWidth(self.maximum_width + 100)
        self.setMaximumWidth(self.maximum_width + 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

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

        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.buttons_layout)

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

        self.purchase_price_input = DoubleSpinBox()
        self.adjust_price_input = DoubleSpinBox()
        self.sell_price_input = DoubleSpinBox()

        self.purchase_price_input.editingFinished.connect(self.updateSellPrice)
        self.adjust_price_input.editingFinished.connect(self.updateSellPrice)
        self.sell_price_input.editingFinished.connect(self.updateAdjustPrice)

        product_price_layout.addWidget(purchase_price_label, 0, 0)
        product_price_layout.addWidget(self.purchase_price_input, 0, 1)
        product_price_layout.addWidget(adjust_price_label, 0, 2)
        product_price_layout.addWidget(self.adjust_price_input, 0, 3)
        product_price_layout.addWidget(sell_price_label, 0, 4)
        product_price_layout.addWidget(self.sell_price_input, 0, 5)

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

    def updateSellPrice(self):
        purchase = self.purchase_price_input.value()
        adjust = self.adjust_price_input.value()

        self.sell_price_input.setValue(purchase + (purchase * (adjust / 100)))
    
    def updateAdjustPrice(self):
        sell = self.sell_price_input.value()
        purchase = self.purchase_price_input.value()

        self.adjust_price_input.setValue(((sell/purchase) - 1) * 100)

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
        #people_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
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
        person_type_input = ComboBox(["Pessoa Física", "Pessoa Jurídica"])
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

class TransactionDialog(BaseDialog):
    def __init__(self, maximum_width=1000, maximum_height=800, initial_window=0):
        super().__init__(maximum_width)

        self.total = 0

        self.initial_window = initial_window
        self.setMaximumSize(maximum_width, maximum_height)
        self.setMinimumSize(900, 600)
        self.setWindowTitle("Movimentação")

        self.date_widget = QWidget()
        self.date_layout = QHBoxLayout()
        self.date_layout.setContentsMargins(0, 0, 0, 6)

        self.date = DateEdit()
        self.date_layout.addWidget(Label("Data da venda:"))
        self.date_layout.addWidget(self.date)
        self.date_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.date_widget.setLayout(self.date_layout)

        self.people_info_widget = QWidget()
        self.people_info_layout = QVBoxLayout()

        self.search_people = LineEdit("Procure por um cliente")
        self.search_people.setMaximumWidth(800)
        self.people_info_layout.addWidget(self.search_people)
        self.people_info_widget.setLayout(self.people_info_layout)

        self.tab = QTabWidget()
        self.product_tab, self.service_tab, self.payment_tab = self.createTabs()
        self.tab.addTab(self.product_tab.widget, "Produtos")
        self.tab.addTab(self.service_tab.widget, "Serviços")
        self.tab.addTab(self.payment_tab.widget, "Pagamentos")

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

        self.return_data = ReturnData(self)
        self.updateReturnDataTarget(self.initial_window)
        self.tab.currentChanged.connect(self.updateReturnDataTarget)

    def createTabs(self):
        return self.ProductTab(self), self.ServiceTab(self), self.PaymentTab(self)

    class ProductTab():
        def __init__(self, parent):
            self.widget = QWidget()
            self.parent = parent

            product_layout = QVBoxLayout()
            product_info_widget, product_search, product_inputs = self.createProductInputs()
            self.product_search_input = product_search
            self.product_stock_input, self.product_price_input, self.product_quantity_input, self.product_subtotal_input = product_inputs
            self.table_widget = TableWidget(["Nome", "Preço", "Quantidade", "Total"])

            self.product_price_input.editingFinished.connect(self.updateSellPrice)
            self.product_quantity_input.editingFinished.connect(self.updateSellPrice)

            product_layout.addWidget(product_info_widget)
            product_layout.addWidget(self.table_widget)
            
            self.widget.setLayout(product_layout)

            self.parent.setupSearch(product_search, product_inputs, data=[
                {"nome": "PENDRIVE SAMSUNG 8G", "estoque": 3, "quantidade": 1, "valor": 39.90},
                {"nome": "PENDRIVE SANDISK 16GB", "estoque": 5, "quantidade": 1, "valor": 59.90}
            ])

        def createProductInputs(self):
            widget = QWidget()
            layout = QGridLayout()
            layout.setSpacing(6)
            layout.setContentsMargins(0, 0, 0, 0)

            widget.setLayout(layout)

            search_input = LineComplement("Procure por um produto")

            price_input = DoubleSpinBox()
            quantity_input = SpinBox()
            subtotal_input = DoubleSpinBox()
            subtotal_input.setReadOnly(True)
            subtotal_input.setButtonSymbols(QAbstractSpinBox.NoButtons)

            optionsButtons, buttons = self.parent.createOptionsButtons()
            add_button, edit_button, remove_button = buttons

            add_button.clicked.connect(self.addProduct)
            edit_button.clicked.connect(self.editProduct)
            remove_button.clicked.connect(self.removeProduct)

            layout.addWidget(search_input, 0, 0, 1, 12)
            layout.addWidget(Label("Preço: R$"), 1, 0)
            layout.addWidget(price_input, 1, 1)
            layout.addWidget(Label("Quantidade:"), 1, 2)
            layout.addWidget(quantity_input, 1, 3)
            layout.addWidget(Label(" = "), 1, 4)
            layout.addWidget(subtotal_input, 1, 5)
            layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 6)
            layout.addWidget(optionsButtons, 1, 7, 1, 5)

            return widget, search_input.search_input, (search_input.complement_input, price_input, quantity_input, subtotal_input)
        
        def updateSellPrice(self):
            price = self.product_price_input.value()
            quantity = self.product_quantity_input.value()

            self.product_subtotal_input.setValue(price * quantity)
        
        def addProduct(self):
            row_count = self.table_widget.rowCount()

            self.table_widget.insertRow(row_count)

            search = self.product_search_input.text()
            price = self.product_price_input.value()
            quantity = self.product_quantity_input.value()
            subtotal = self.product_subtotal_input.value()
            total_input = self.parent.total_input
            
            self.table_widget.setItem(row_count, 0, QTableWidgetItem(search))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(price)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(subtotal)))

            self.parent.total += subtotal
            self.parent.payment_tab.value_input.setValue(self.parent.total)
            total_input.setValue(self.parent.total)

            self.parent.clearFields([self.product_search_input, *(self.product_price_input, self.product_quantity_input, self.product_subtotal_input)])

        def editProduct(self):
            pass

        def removeProduct(self):
            pass

    class ServiceTab():
        def __init__(self, parent):
            self.widget = QWidget()
            self.parent = parent

            service_layout = QVBoxLayout()
            service_info_widget, service_search, service_inputs = self.createServiceInputs()
            self.service_search_input = service_search
            self.service_price_input, self.service_quantity_input, self.service_subtotal_input = service_inputs

            self.table_widget = TableWidget(["Tipo", "Quantidade", "Preço", "Total"])

            self.service_price_input.editingFinished.connect(self.updateSellPrice)
            self.service_quantity_input.editingFinished.connect(self.updateSellPrice)

            service_layout.addWidget(service_info_widget)
            service_layout.addWidget(self.table_widget)
            
            self.widget.setLayout(service_layout)

            # Conecta search e clear
            self.parent.setupSearch(service_search, service_inputs, data=[
                {"nome": "XEROX", "quantidade": 1, "valor": 0.50},
                {"nome": "CURRÍCULO", "quantidade": 10, "valor": 10}
            ])
    
        def createServiceInputs(self):
            widget = QWidget()
            layout = QGridLayout()
            widget.setLayout(layout)

            search_input = LineComplement("Procure por um serviço...", property="WithoutComplement")

            price_input = DoubleSpinBox()
            quantity_input = SpinBox()
            subtotal_input = DoubleSpinBox()
            subtotal_input.setReadOnly(True)
            subtotal_input.setButtonSymbols(QAbstractSpinBox.NoButtons)

            optionsButtons, buttons = self.parent.createOptionsButtons()
            add_button, edit_button, remove_button = buttons

            add_button.clicked.connect(self.addService)
            edit_button.clicked.connect(self.editService)
            remove_button.clicked.connect(self.removeService)

            layout.addWidget(search_input, 0, 0, 1, 9)
            layout.addWidget(Label("Preço: R$"), 1, 0)
            layout.addWidget(price_input, 1, 1)
            layout.addWidget(Label("Quantidade:"), 1, 2)
            layout.addWidget(quantity_input, 1, 3)
            layout.addWidget(Label(" = "), 1, 4)
            layout.addWidget(subtotal_input, 1, 5)
            layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 6)
            layout.addWidget(optionsButtons, 1, 7, 1, 5)

            return widget, search_input.search_input, (price_input, quantity_input, subtotal_input)
        
        def updateSellPrice(self):
            price = self.service_price_input.value()
            quantity = self.service_quantity_input.value()

            self.service_subtotal_input.setValue(price * quantity)
        
        def addService(self):
            row_count = self.table_widget.rowCount()

            self.table_widget.insertRow(row_count)

            search = self.service_search_input.text()
            price = self.service_price_input.value()
            quantity = self.service_quantity_input.value()
            subtotal = self.service_subtotal_input.value()
            total_input = self.parent.total_input
            
            self.table_widget.setItem(row_count, 0, QTableWidgetItem(search))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(price)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(subtotal)))

            self.parent.total += subtotal
            self.parent.payment_tab.value_input.setValue(self.parent.total)
            total_input.setValue(self.parent.total)

            self.parent.clearFields([self.service_search_input, *(self.service_price_input, self.service_quantity_input, self.service_subtotal_input)])
            pass

        def editService(self):
            pass

        def removeService(self):
            pass

    class PaymentTab():
        def __init__(self, parent):
            self.widget = QWidget()
            self.parent = parent

            payment_layout = QVBoxLayout()
            payment_info_widget, inputs = self.createPaymentInputs()
            self.document_input, self.value_input = inputs

            payment_layout.addWidget(payment_info_widget)
            payment_layout.addWidget(TableWidget(["Data", "Documento", "Valor"]))
            
            self.widget.setLayout(payment_layout)

        def createPaymentInputs(self):
            widget = QWidget()
            layout = QGridLayout()
            widget.setLayout(layout)

            document_input = ComboBox(["PIX", "Cartão de Crédito", "Cartão de Débito"], True)
            value_input = DoubleSpinBox()

            optionsButtons, buttons = self.parent.createOptionsButtons()
            add_button, edit_button, remove_button = buttons

            add_button.clicked.connect(self.addPayment)
            edit_button.clicked.connect(self.editPayment)
            remove_button.clicked.connect(self.removePayment)

            layout.addWidget(Label("Documento:"), 0, 0)
            layout.addWidget(document_input, 0, 1)
            layout.addWidget(Label("Valor: R$"), 0, 2)
            layout.addWidget(value_input, 0, 3)
            layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 6)
            layout.addWidget(optionsButtons, 1, 7, 1, 5)

            return widget, (document_input, value_input)
    
        def addPayment(self):
            pass

        def editPayment(self):
            pass

        def removePayment(self):
            pass

    def clearFields(self, fields: list):
        for f in fields:
            if isinstance(f, QLineEdit):
                if f.isReadOnly():
                    f.setReadOnly(False if "SearchInput" in f.__class__.__name__ else True)
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

        pos_global = search_widget.mapToGlobal(QPoint(0, search_widget.height()))
        pos_local = self.mapFromGlobal(pos_global)
        self.return_data.move(pos_local)
        self.return_data.setFixedWidth(search_widget.width())

    def updateReturnDataTarget(self, index):
        if index == 0:  # Produtos
            targets = {
                "nome": self.product_tab.product_search_input,
                "estoque": self.product_tab.product_stock_input,
                "quantidade": self.product_tab.product_quantity_input,
                "valor": self.product_tab.product_price_input,
                "subtotal": self.product_tab.product_subtotal_input
            }
        elif index == 1:  # Serviços
            targets = {
                "nome": self.service_tab.service_search_input,
                "quantidade": self.service_tab.service_quantity_input,
                "valor": self.service_tab.service_price_input,
                "subtotal": self.service_tab.service_subtotal_input
            }
        else:
            targets = {}
        
        self.return_data.setTarget(targets)

    def createOptionsButtons(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 6, 6, 6)

        add_button = PageButton("Adicionar", icon_path="plus.svg")
        edit_button = PageButton("Editar", icon_path="edit.svg")
        remove_button = PageButton("Remover", icon_path="cross.svg")

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(remove_button)

        widget.setLayout(layout)

        return widget, (add_button, edit_button, remove_button)

    # ----------------------
    # --- Configura Search
    # ----------------------
    def setupSearch(self, search_widget, inputs, data):
        clear_action = search_widget.addAction(QIcon.fromTheme("window-close"), QLineEdit.TrailingPosition)
        clear_action.triggered.connect(lambda: self.clearFields([search_widget, *inputs]))

        if len(inputs) == 3:
            search_widget.textChanged.connect(
                lambda text: self.searchItems(data,
                                            {"nome": search_widget,
                                            "valor": inputs[0],
                                            "quantidade": inputs[1],
                                            "subtotal": inputs[2]},
                                            search_widget)
        )
        else:
            search_widget.textChanged.connect(
                lambda text: self.searchItems(data,
                                {"nome": search_widget,
                                "estoque": inputs[0],
                                "valor": inputs[1],
                                "quantidade": inputs[2],
                                "subtotal": inputs[3]},
                                search_widget)
        )
    
    def updateServiceSellPrice(self):
        price = self.service_price_input.value()
        quantity = self.service_quantity_input.value()

        self.service_subtotal_input.setValue(price * quantity)

class InvoiceDialog(BaseDialog):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout()

        supplier_info_group = GroupBox("Informações do fornecedor")
        supplier_info_layout = QGridLayout()

        search_supplier_input = LineEdit()
        search_supplier_input.setMaximumWidth(1200)
        search_supplier_input.setPlaceholderText("Procure por um fornecedor")

        company_name_label = Label("Razão Social:")
        cnpj_label = Label("CNPJ:")
        address_label = Label("Endereço:")
        cellphone_label = Label("Telefone:")
        email_label = Label("Email:")

        company_name_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cnpj_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        address_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cellphone_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        email_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        company_name_input = Label("")
        cnpj_input = Label("")
        address_input = Label("")
        cellphone_input = Label("")
        email_input = Label("")

        supplier_info_layout.addWidget(search_supplier_input, 0, 0, 1, 2)
        supplier_info_layout.addWidget(company_name_label, 1, 0)
        supplier_info_layout.addWidget(company_name_input, 1, 1)
        supplier_info_layout.addWidget(cnpj_label, 2, 0)
        supplier_info_layout.addWidget(cnpj_input, 2, 1)
        supplier_info_layout.addWidget(address_label, 3, 0)
        supplier_info_layout.addWidget(address_input, 3, 1)
        supplier_info_layout.addWidget(cellphone_label, 4, 0)
        supplier_info_layout.addWidget(cellphone_input, 4, 1)
        supplier_info_layout.addWidget(email_label, 5, 0)
        supplier_info_layout.addWidget(email_input, 5, 1)

        supplier_info_layout.setColumnStretch(1, 2)

        supplier_info_group.setLayout(supplier_info_layout)

        product_info_group = GroupBox("Informações do produto")
        product_info_layout = QGridLayout()

        purchase_price_label = Label("Compra: R$")
        quantity_label = Label("Quantidade:")

        search_product_input = LineEdit()
        search_product_input.setMaximumWidth(1200)
        search_product_input.setPlaceholderText("Procure por um produto")
        purchase_price_input = DoubleSpinBox()
        quantity_input = SpinBox()

        add_btn = PageButton("Adicionar", icon_path="plus.svg")
        edit_btn = PageButton("Editar", icon_path="edit.svg")
        remove_btn = PageButton("Remover", icon_path="cross.svg")

        table_input = TableWidget(["Produto", "Preço de compra", "Quantidade", "Novo estoque"])

        product_info_layout.addWidget(search_product_input, 0, 0, 1, 9)
        product_info_layout.addWidget(purchase_price_label, 1, 0)
        product_info_layout.addWidget(purchase_price_input, 1, 1)
        product_info_layout.addWidget(quantity_label, 1, 2)
        product_info_layout.addWidget(quantity_input, 1, 3)
        product_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 4)
        product_info_layout.addWidget(add_btn, 1, 5)
        product_info_layout.addWidget(edit_btn, 1, 6)
        product_info_layout.addWidget(remove_btn, 1, 7)
        product_info_layout.addWidget(table_input, 2, 0, 1, 8)

        product_info_group.setLayout(product_info_layout)

        layout.addWidget(supplier_info_group)
        layout.addWidget(product_info_group)

        widget.setLayout(layout)

        self.input_layout.addWidget(widget)