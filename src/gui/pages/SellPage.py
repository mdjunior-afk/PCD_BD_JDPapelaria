from PySide6.QtWidgets import *

from ..widgets import *

from .Dialogs import *

class SellPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 24)
        self.main_layout.setSpacing(12)

        self.search_widget = QWidget()
        
        self.search_layout = QHBoxLayout(self.search_widget)
        self.search_layout.setContentsMargins(0, 0, 0, 12)

        self.left_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.intial_date = DateEdit(icon_path="calendar.svg")
        self.date_label = QLabel(" Até ")
        self.date_label.setStyleSheet("color: #747474")
        self.final_date = DateEdit(icon_path="calendar.svg")
        self.right_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.search_layout.addItem(self.left_spacer)
        self.search_layout.addWidget(self.intial_date)
        self.search_layout.addWidget(self.date_label)
        self.search_layout.addWidget(self.final_date)
        self.search_layout.addItem(self.right_spacer)

        self.box_widget = QWidget()
        self.box_widget_layout = QHBoxLayout(self.box_widget)
        self.box_widget_layout.setContentsMargins(0, 0, 0, 6)

        self.add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.edit_btn = PageButton("Editar", icon_path="edit.svg")
        self.remove_btn = PageButton("Remover", icon_path="cross.svg")
        self.box_widget_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.add_btn.clicked.connect(self.addWindow)
        self.edit_btn.clicked.connect(self.editWindow)
        self.remove_btn.clicked.connect(self.removeWindow)

        self.box_widget_layout.addWidget(self.add_btn)
        self.box_widget_layout.addWidget(self.edit_btn)
        self.box_widget_layout.addWidget(self.remove_btn)
        self.box_widget_layout.addItem(self.box_widget_spacer)

        self.table = TableWidget(["ID", "Nome", "CPF/CNPJ", "Endereço"], "Venda")

        self.main_layout.addWidget(self.search_widget)
        self.main_layout.addWidget(self.box_widget)
        self.main_layout.addWidget(self.table)

    def addWindow(self):
        self.current_win = SellDialog()

        self.current_win.exec()

    def editWindow(self):
        self.current_win = BaseDialog()

        self.current_win.exec()
        pass

    def removeWindow(self):
        self.current_win = BaseDialog()

        self.current_win.exec()
        pass