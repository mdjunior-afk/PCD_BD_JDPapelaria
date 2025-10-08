from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from ..widgets import *

class InvoicePage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.supplier_info_group = GroupBox("Informações do fornecedor")
        self.supplier_info_layout = QGridLayout()

        self.search_supplier_input = LineEdit()
        self.search_supplier_input.setMaximumWidth(1200)
        self.search_supplier_input.setPlaceholderText("Procure por um fornecedor")

        self.company_name_label = Label("Razão Social:")
        self.cnpj_label = Label("CNPJ:")
        self.address_label = Label("Endereço:")
        self.cellphone_label = Label("Telefone:")
        self.email_label = Label("Email:")

        self.company_name_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.cnpj_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.cellphone_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.company_name_input = Label("")
        self.cnpj_input = Label("")
        self.address_input = Label("")
        self.cellphone_input = Label("")
        self.email_input = Label("")

        self.supplier_info_layout.addWidget(self.search_supplier_input, 0, 0, 1, 2)
        self.supplier_info_layout.addWidget(self.company_name_label, 1, 0)
        self.supplier_info_layout.addWidget(self.company_name_input, 1, 1)
        self.supplier_info_layout.addWidget(self.cnpj_label, 2, 0)
        self.supplier_info_layout.addWidget(self.cnpj_input, 2, 1)
        self.supplier_info_layout.addWidget(self.address_label, 3, 0)
        self.supplier_info_layout.addWidget(self.address_input, 3, 1)
        self.supplier_info_layout.addWidget(self.cellphone_label, 4, 0)
        self.supplier_info_layout.addWidget(self.cellphone_input, 4, 1)
        self.supplier_info_layout.addWidget(self.email_label, 5, 0)
        self.supplier_info_layout.addWidget(self.email_input, 5, 1)

        self.supplier_info_layout.setColumnStretch(1, 2)

        self.supplier_info_group.setLayout(self.supplier_info_layout)

        self.product_info_group = GroupBox("Informações do produto")
        self.product_info_layout = QGridLayout()

        self.purchase_price_label = Label("Compra: R$")
        self.quantity_label = Label("Quantidade:")

        self.search_product_input = LineEdit()
        self.search_product_input.setMaximumWidth(1200)
        self.search_product_input.setPlaceholderText("Procure por um produto")
        self.purchase_price_input = DoubleSpinBox()
        self.quantity_input = SpinBox()

        self.add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.edit_btn = PageButton("Editar", icon_path="edit.svg")
        self.remove_btn = PageButton("Remover", icon_path="cross.svg")

        self.table_input = TableWidget(["Produto", "Preço de compra", "Quantidade", "Novo estoque"])

        self.product_info_layout.addWidget(self.search_product_input, 0, 0, 1, 9)
        self.product_info_layout.addWidget(self.purchase_price_label, 1, 0)
        self.product_info_layout.addWidget(self.purchase_price_input, 1, 1)
        self.product_info_layout.addWidget(self.quantity_label, 1, 2)
        self.product_info_layout.addWidget(self.quantity_input, 1, 3)
        self.product_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 4)
        self.product_info_layout.addWidget(self.add_btn, 1, 5)
        self.product_info_layout.addWidget(self.edit_btn, 1, 6)
        self.product_info_layout.addWidget(self.remove_btn, 1, 7)
        self.product_info_layout.addWidget(self.table_input, 2, 0, 1, 8)

        self.product_info_group.setLayout(self.product_info_layout)

        self.main_layout.addWidget(self.supplier_info_group)
        self.main_layout.addWidget(self.product_info_group)

        #self.main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.options_widget = QWidget()
        self.options_layout = QHBoxLayout()

        self.save_btn = PageButton("Salvar", icon_path="disk.svg")
        self.new_btn = PageButton("Novo", icon_path="plus.svg")
        self.cancel_btn = PageButton("Cancelar", icon_path="cross.svg")

        self.options_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.options_layout.addWidget(self.save_btn)
        self.options_layout.addWidget(self.new_btn)
        self.options_layout.addWidget(self.cancel_btn)

        self.options_widget.setLayout(self.options_layout)

        self.main_layout.addWidget(self.options_widget)

        self.setLayout(self.main_layout)


