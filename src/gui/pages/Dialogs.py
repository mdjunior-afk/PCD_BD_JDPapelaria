from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIcon

from ..widgets import *

class BaseDialog(QDialog):
    def __init__(self, maximum_width=800):
        super().__init__()

        self.setStyleSheet("background-color: #D9D9D9; color: #747474;")

        self.setMaximumWidth(maximum_width)

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

        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()

        self.category_label = QLabel("Categoria:")
        self.category_box = QComboBox()
        self.category_box.addItems(["CARREGADOR", "PENDRIVE", "CANETA"])

        self.barcode_label = QLabel("Cód.Barra:")
        self.barcode_input = QLineEdit()

        self.buy_price_label = QLabel("Preço de compra: R$")
        self.buy_price_input = QSpinBox(minimum=0, maximum=99999)

        self.adjust_label = QLabel("Reajuste: ")
        self.adjust_input = QSpinBox(minimum=0, maximum=99999)
        self.perc = QLabel("%")

        self.sell_price_label = QLabel("Preço de venda: R$")
        self.sell_price_input = QSpinBox(minimum=0, maximum=99999)

        self.input_layout.addWidget(self.name_label, 0, 0)
        self.input_layout.addWidget(self.name_input, 0, 1, 1, 6)

        self.input_layout.addWidget(self.category_label, 1, 0)
        self.input_layout.addWidget(self.category_box, 1, 1)
        
        self.input_layout.addWidget(self.barcode_label, 1, 2)
        self.input_layout.addWidget(self.barcode_input, 1, 3, 1, 4)

        self.input_layout.addWidget(self.buy_price_label, 2, 0)
        self.input_layout.addWidget(self.buy_price_input, 2, 1)
        self.input_layout.addWidget(self.adjust_label, 2, 2)
        self.input_layout.addWidget(self.adjust_input, 2, 3)
        self.input_layout.addWidget(self.perc, 2, 4)
        self.input_layout.addWidget(self.sell_price_label, 2, 5)
        self.input_layout.addWidget(self.sell_price_input, 2, 6)

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIcon

from ..widgets import *

class TransactionDialog(BaseDialog):
    def __init__(self, maximum_width=800, maximum_height=800, initial_window=0):
        super().__init__(maximum_width)

        self.initial_window = initial_window
        self.setMaximumSize(maximum_width, maximum_height)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Movimentação")

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
        self.total_info_layout.addWidget(QLabel("Total: R$"))
        self.total_info_layout.addWidget(self.total_input)
        self.total_info_widget.setLayout(self.total_info_layout)

        self.input_layout.addWidget(self.people_info_widget)
        self.input_layout.addWidget(self.tab)
        self.input_layout.addWidget(self.total_info_widget)
        self.tab.setCurrentIndex(self.initial_window)

        # --- ReturnData ---
        self.return_data = ReturnData(self)
        self.updateReturnDataTarget(self.initial_window)
        self.tab.currentChanged.connect(self.updateReturnDataTarget)

    # ----------------------
    # --- Funções Genéricas
    # ----------------------
    def clearFields(self, fields: list):
        for f in fields:
            if isinstance(f, (QLineEdit, QSpinBox, QDoubleSpinBox)):
                f.clear()
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
        search_input.setMaximumWidth(800)

        price_input = DoubleSpinBox()
        quantity_input = SpinBox()
        subtotal_input = DoubleSpinBox()
        subtotal_input.setReadOnly(True)
        subtotal_input.setButtonSymbols(QAbstractSpinBox.NoButtons)

        layout.addWidget(search_input, 0, 0, 1, 9)
        layout.addWidget(QLabel("Preço: R$"), 1, 0)
        layout.addWidget(price_input, 1, 1)
        layout.addWidget(QLabel("Quantidade:"), 1, 2)
        layout.addWidget(quantity_input, 1, 3)
        layout.addWidget(QLabel(" = "), 1, 4)
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
        search_input.setMaximumWidth(1200)

        price_input = DoubleSpinBox()
        quantity_input = SpinBox()
        subtotal_input = DoubleSpinBox()
        subtotal_input.setReadOnly(True)
        subtotal_input.setButtonSymbols(QAbstractSpinBox.NoButtons)

        layout.addWidget(search_input, 0, 0, 1, 9)
        layout.addWidget(QLabel("Preço: R$"), 1, 0)
        layout.addWidget(price_input, 1, 1)
        layout.addWidget(QLabel("Quantidade:"), 1, 2)
        layout.addWidget(quantity_input, 1, 3)
        layout.addWidget(QLabel(" = "), 1, 4)
        layout.addWidget(subtotal_input, 1, 5)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 6)
        layout.addWidget(PageButton("Adicionar", icon_path="plus.svg"), 1, 7)
        layout.addWidget(PageButton("Remover", icon_path="cross.svg"), 1, 8)

        return widget, search_input, (price_input, quantity_input, subtotal_input)
    
    def createPaymentInputs(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        document_input = QComboBox()
        document_input.addItems(["PIX", "Cartão de Crédito", "Cartão de Débito"])
        value_input = DoubleSpinBox()

        layout.addWidget(QLabel("Documento:"), 0, 0)
        layout.addWidget(document_input, 0, 1)
        layout.addWidget(QLabel("Valor: R$"), 0, 2)
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
