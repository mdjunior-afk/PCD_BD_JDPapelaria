from PySide6.QtWidgets import *

from gui.widgets.LineEdit import LineEdit
from gui.widgets.PageButton import PageButton
from gui.widgets.TableWidget import TableWidget
from gui.widgets.InfoWidget import InfoWidget
from gui.widgets.DateEdit import DateEdit

class PageManager(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.home_page = QWidget()

        self.home_page_layout = QVBoxLayout(self.home_page)
        self.home_page_layout.setContentsMargins(12, 12, 12, 12)
        self.home_page_layout.setSpacing(6)

        self.home_search_widget = QWidget()
        
        self.home_search_layout = QHBoxLayout(self.home_search_widget)
        self.home_search_layout.setContentsMargins(0, 0, 0, 12)

        self.home_search_input = LineEdit("Procure por algo...")

        self.home_search_layout.addWidget(self.home_search_input)

        self.box = QWidget()

        self.box_layout = QHBoxLayout(self.box)
        self.box_layout.setContentsMargins(0, 0, 0, 12)
        self.box_layout.setSpacing(6)

        self.left_home_box_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.right_home_box_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.stock_info = InfoWidget(title="Estoques baixos", info="10")
        self.birthday_qtd = InfoWidget(title="Aniversáriantes do mês", info="3")
        self.daily_sell = InfoWidget(title="Vendas de hoje", info="5")

        self.box_layout.addItem(self.left_home_box_spacer)
        self.box_layout.addWidget(self.stock_info)
        self.box_layout.addWidget(self.daily_sell)
        self.box_layout.addWidget(self.birthday_qtd)
        self.box_layout.addItem(self.right_home_box_spacer)

        self.home_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.home_page_layout.addWidget(self.home_search_widget)
        self.home_page_layout.addWidget(self.box)
        self.home_page_layout.addItem(self.home_spacer)

        self.insertWidget(0, self.home_page)

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

        self.insertWidget(1, self.product_page)

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

        self.insertWidget(2, self.people_page)

        #Sell Page
        self.sell_page = QWidget()

        self.sell_page_layout = QVBoxLayout(self.sell_page)
        self.sell_page_layout.setContentsMargins(12, 12, 12, 24)
        self.sell_page_layout.setSpacing(12)

        self.sell_search_widget = QWidget()
        
        self.sell_search_layout = QHBoxLayout(self.sell_search_widget)
        self.sell_search_layout.setContentsMargins(0, 0, 0, 12)

        self.sell_left_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.sell_intial_date = DateEdit(icon_path="calendar.svg")
        self.date_label = QLabel(" Até ")
        self.date_label.setStyleSheet("color: #747474")
        self.sell_final_date = DateEdit(icon_path="calendar.svg")
        self.sell_right_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.sell_search_layout.addItem(self.sell_left_spacer)
        self.sell_search_layout.addWidget(self.sell_intial_date)
        self.sell_search_layout.addWidget(self.date_label)
        self.sell_search_layout.addWidget(self.sell_final_date)
        self.sell_search_layout.addItem(self.sell_right_spacer)

        self.sell_buttons_box = QWidget()
        self.sell_buttons_box_layout = QHBoxLayout(self.sell_buttons_box)
        self.sell_buttons_box_layout.setContentsMargins(0, 0, 0, 6)

        self.sell_add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.sell_edit_btn = PageButton("Editar", icon_path="edit.svg")
        self.sell_remove_btn = PageButton("Remover", icon_path="cross.svg")
        self.sell_buttons_box_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.sell_buttons_box_layout.addWidget(self.sell_add_btn)
        self.sell_buttons_box_layout.addWidget(self.sell_edit_btn)
        self.sell_buttons_box_layout.addWidget(self.sell_remove_btn)
        self.sell_buttons_box_layout.addItem(self.sell_buttons_box_spacer)

        self.sell_table = TableWidget(["ID", "Nome", "CPF/CNPJ", "Endereço"], "Venda")

        self.sell_page_layout.addWidget(self.sell_search_widget)
        self.sell_page_layout.addWidget(self.sell_buttons_box)
        self.sell_page_layout.addWidget(self.sell_table)

        self.insertWidget(3, self.sell_page)