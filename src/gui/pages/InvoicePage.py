from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from ..widgets import *

from .Dialogs import *

class InvoicePage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 24)
        self.main_layout.setSpacing(12)

        self.search_widget = QWidget()
        
        self.search_layout = QHBoxLayout(self.search_widget)
        self.search_layout.setSpacing(0)
        self.search_layout.setContentsMargins(0, 0, 0, 12)

        self.search_input = LineEdit("Procure por um fornecedor")

        self.search_layout.addWidget(self.search_input)

        self.buttons_box = QWidget()
        self.buttons_box_layout = QHBoxLayout(self.buttons_box)
        self.buttons_box_layout.setContentsMargins(0, 0, 0, 6)

        self.add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.edit_btn = PageButton("Editar", icon_path="edit.svg")
        self.remove_btn = PageButton("Remover", icon_path="cross.svg")
        self.procuct_buttons_box_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.add_btn.clicked.connect(self.addWindow)
        self.edit_btn.clicked.connect(self.editWindow)
        self.remove_btn.clicked.connect(self.removeWindow)

        self.buttons_box_layout.addWidget(self.add_btn)
        self.buttons_box_layout.addWidget(self.edit_btn)
        self.buttons_box_layout.addWidget(self.remove_btn)
        self.buttons_box_layout.addItem(self.procuct_buttons_box_spacer)

        self.table = TableWidget()

        self.main_layout.addWidget(self.search_widget)
        self.main_layout.addWidget(self.buttons_box)
        self.main_layout.addWidget(self.table)

    def addWindow(self):
        self.current_win = InvoiceDialog()

        self.current_win.exec()

    def editWindow(self):
        self.current_win = InvoiceDialog()

        self.current_win.exec()
        pass

    def removeWindow(self):
        self.current_win = BaseDialog()

        self.current_win.exec()
        pass

