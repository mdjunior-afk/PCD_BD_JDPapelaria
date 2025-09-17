from PySide6.QtWidgets import *

from ..widgets import *

class BaseDialog(QDialog):
    def __init__(self, maximum_width=800):
        super().__init__()

        self.setStyleSheet("background-color: #D9D9D9; color: #747474;")

        self.setMaximumWidth(maximum_width)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.input_layout = QGridLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 12)

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

class TransactionDialog(BaseDialog):
    def __init__(self, maximum_width=800, maximum_height=800, initial_window=0):
        super().__init__(maximum_width)

        self.initial_window = initial_window

        self.setMaximumSize(maximum_width, maximum_height)
        self.setMinimumSize(800, 600)

        self.setWindowTitle("Movimentação")

        self.people_info_widget = QWidget()
        self.people_info_layout = QVBoxLayout()
        
        self.search_people = LineEdit("Procure por um cliente")
        self.search_people.setMaximumWidth(800)

        self.people_info_layout.addWidget(self.search_people)

        self.people_info_widget.setLayout(self.people_info_layout)

        self.tab = QTabWidget()

        self.product_tab = QWidget()
        self.product_layout = QVBoxLayout()

        self.product_info_widget = QWidget()
        self.product_info_layout = QGridLayout()
        self.product_info_layout.setSpacing(6)

        self.product_info_widget.setLayout(self.product_info_layout)

        self.product_search_input = LineEdit("Procure por um produto...")
        self.product_search_input.setMaximumWidth(800)

        self.product_price_label = QLabel("Preço: R$")
        self.product_price_input = DoubleSpinBox()
        self.product_quantity_label = QLabel("Quantidade:")
        self.product_quantity_input = SpinBox()
        self.product_table = TableWidget(["Nome", "Quantidade", "Preço", "Total"])
        self.add_product_btn = PageButton("Adicionar", icon_path="plus.svg")

        self.product_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.product_info_layout.addWidget(self.product_search_input, 0, 0, 1, 6)

        # Linha de baixo
        self.product_info_layout.addWidget(self.product_price_label, 1, 0)
        self.product_info_layout.addWidget(self.product_price_input, 1, 1)
        self.product_info_layout.addWidget(self.product_quantity_label, 1, 2)
        self.product_info_layout.addWidget(self.product_quantity_input, 1, 3)
        self.product_info_layout.addItem(self.product_spacer, 1, 4)
        self.product_info_layout.addWidget(self.add_product_btn, 1, 5)

        # Faz a coluna do input expandir
        self.product_info_layout.setColumnStretch(0, 0)  # cresce
        self.product_info_layout.setColumnStretch(1, 0)
        self.product_info_layout.setColumnStretch(2, 0)
        self.product_info_layout.setColumnStretch(3, 0)
        self.product_info_layout.setColumnStretch(4, 1)
        self.product_info_layout.setColumnStretch(5, 0)

        self.product_layout.addWidget(self.product_info_widget)
        self.product_layout.addWidget(self.product_table)

        self.product_tab.setLayout(self.product_layout)

        self.service_tab = QWidget()
        self.service_layout = QVBoxLayout()

        self.service_info_widget = QWidget()
        self.service_info_layout = QGridLayout()

        self.service_info_widget.setLayout(self.service_info_layout)

        self.service_search_input = LineEdit("Procure por um serviço...")
        self.service_search_input.setMaximumWidth(1200)
        self.service_price_label = QLabel("Preço: R$")
        self.service_price_input = DoubleSpinBox()
        self.service_quantity_label = QLabel("Quantidade:")
        self.service_quantity_input = SpinBox()
        self.service_table = TableWidget(["Tipo", "Quantidade", "Preço", "Total"])
        self.add_service_btn = PageButton("Adicionar", icon_path="plus.svg")

        self.service_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.service_info_layout.addWidget(self.service_search_input, 0, 0, 1, 6)
        self.service_info_layout.addWidget(self.service_price_label, 1, 0)
        self.service_info_layout.addWidget(self.service_price_input, 1, 1)
        self.service_info_layout.addWidget(self.service_quantity_label, 1, 2)
        self.service_info_layout.addWidget(self.service_quantity_input, 1, 3)
        self.service_info_layout.addItem(self.service_spacer, 1, 4)
        self.service_info_layout.addWidget(self.add_service_btn, 1, 5)

        self.service_info_layout.setColumnStretch(0, 0)  # cresce
        self.service_info_layout.setColumnStretch(1, 0)
        self.service_info_layout.setColumnStretch(2, 0)
        self.service_info_layout.setColumnStretch(3, 0)
        self.service_info_layout.setColumnStretch(4, 1)
        self.service_info_layout.setColumnStretch(5, 0)

        self.service_layout.addWidget(self.service_info_widget)
        self.service_layout.addWidget(self.service_table)

        self.service_tab.setLayout(self.service_layout)

        self.payment = QWidget()

        self.tab.addTab(self.product_tab, "Produtos")
        self.tab.addTab(self.service_tab, "Serviços")
        self.tab.addTab(self.payment, "Pagamentos")

        self.input_layout.addWidget(self.people_info_widget)
        self.input_layout.addWidget(self.tab)

        self.tab.setCurrentIndex(self.initial_window)