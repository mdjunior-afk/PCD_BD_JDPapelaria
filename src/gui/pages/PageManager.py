from PySide6.QtWidgets import *

from gui.widgets.LineEdit import LineEdit
from gui.widgets.PageButton import PageButton
from gui.widgets.TableWidget import TableWidget

class PageManager(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.product_page = QWidget()

        self.product_page_layout = QVBoxLayout(self.product_page)
        self.product_page_layout.setContentsMargins(12, 12, 12, 24)
        self.product_page_layout.setSpacing(12)

        self.product_search_widget = QWidget()
        
        self.product_search_layout = QHBoxLayout(self.product_search_widget)
        self.product_search_layout.setContentsMargins(0, 0, 0, 12)

        self.product_search_input = LineEdit("Procure por um produto...")

        self.product_search_layout.addWidget(self.product_search_input)

        self.product_buttons_box = QWidget()
        self.product_buttons_box_layout = QHBoxLayout(self.product_buttons_box)
        self.product_buttons_box_layout.setContentsMargins(0, 0, 0, 6)

        self.add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.edit_btn = PageButton("Editar", icon_path="edit.svg")
        self.remove_btn = PageButton("Remover", icon_path="cross.svg")
        self.procuct_buttons_box_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.product_buttons_box_layout.addWidget(self.add_btn)
        self.product_buttons_box_layout.addWidget(self.edit_btn)
        self.product_buttons_box_layout.addWidget(self.remove_btn)
        self.product_buttons_box_layout.addItem(self.procuct_buttons_box_spacer)

        self.product_table = TableWidget(["ID", "Nome", "Estoque", "Preço", "Categoria"])

        self.product_page_layout.addWidget(self.product_search_widget)
        self.product_page_layout.addWidget(self.product_buttons_box)
        self.product_page_layout.addWidget(self.product_table)

        self.insertWidget(0, self.product_page)

        # People page
        self.people_page = QWidget()

        self.people_page_layout = QVBoxLayout(self.people_page)
        self.people_page_layout.setContentsMargins(12, 12, 12, 24)
        self.people_page_layout.setSpacing(12)

        self.people_search_widget = QWidget()
        
        self.people_search_layout = QHBoxLayout(self.people_search_widget)
        self.people_search_layout.setContentsMargins(0, 0, 0, 12)

        self.people_search_input = LineEdit("Procure por uma pessoa...")

        self.people_search_layout.addWidget(self.people_search_input)

        self.people_buttons_box = QWidget()
        self.people_buttons_box_layout = QHBoxLayout(self.people_buttons_box)
        self.people_buttons_box_layout.setContentsMargins(0, 0, 0, 6)

        self.people_add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.people_edit_btn = PageButton("Editar", icon_path="edit.svg")
        self.people_remove_btn = PageButton("Remover", icon_path="cross.svg")
        self.people_buttons_box_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.people_buttons_box_layout.addWidget(self.people_add_btn)
        self.people_buttons_box_layout.addWidget(self.people_edit_btn)
        self.people_buttons_box_layout.addWidget(self.people_remove_btn)
        self.people_buttons_box_layout.addItem(self.people_buttons_box_spacer)

        self.people_table = TableWidget(["ID", "Nome", "CPF/CNPJ", "Endereço"], "Pessoa")

        self.people_page_layout.addWidget(self.people_search_widget)
        self.people_page_layout.addWidget(self.people_buttons_box)
        self.people_page_layout.addWidget(self.people_table)

        self.insertWidget(1, self.people_page)