from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *

from src.gui.utils import createWindowButtons

class EntryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QGridLayout(self)

        self.supplier_search_input = LineEdit(placeholder="Procure por um fornecedor...")
        
        self.product_search_input = LineEdit(placeholder="Procure por um produto...")
        self.product_price_input = DoubleSpinBox()
        self.product_quantity_input = SpinBox()
        self.expiry_date_input = DateEdit(date=QDate.currentDate())

        self.buttons_widget, self.buttons = createWindowButtons()

        self.table = Table(["ID", "Nome", "Preço de compra", "Quantidade", "Data de validade"])

        self.main_layout.addWidget(self.supplier_search_input, 0, 0, 1, 3)
        self.main_layout.addWidget(self.product_search_input, 1, 0, 1, 4)
        self.main_layout.addWidget(self.product_price_input, 2, 0)
        self.main_layout.addWidget(self.product_quantity_input, 2, 1)
        self.main_layout.addWidget(self.expiry_date_input, 2, 2)
        self.main_layout.addWidget(self.buttons_widget, 2, 3, 1, 2)
        self.main_layout.addWidget(self.table, 3, 0, 1, 4)