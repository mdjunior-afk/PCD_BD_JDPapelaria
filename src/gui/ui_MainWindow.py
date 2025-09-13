from PySide6.QtWidgets import *
from PySide6.QtGui import QColor
from PySide6.QtCore import QPropertyAnimation

from gui.widgets.PushButton import PushButton
from gui.widgets.PageButton import PageButton
from gui.widgets.LineEdit import LineEdit

#from gui.pages.ui_PageApplication import PageManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JD Papelaria")
        
        self.resize(1280, 720)
        self.setMinimumSize(800, 600)

        # Shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 200))
        shadow_effect.setOffset(5, 5)

        shadow_effect2 = QGraphicsDropShadowEffect()
        shadow_effect2.setBlurRadius(20)
        shadow_effect2.setColor(QColor(0, 0, 0, 200))
        shadow_effect2.setOffset(5, 5)

        self.central_widget = QWidget()
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # START: side_menu
        self.side_menu = QWidget()
        self.side_menu.setStyleSheet("background-color: #EFEFEF")
        self.side_menu.setGraphicsEffect(shadow_effect)
        self.side_menu.setMaximumWidth(50)

        self.side_menu_layout = QVBoxLayout(self.side_menu)
        self.side_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_layout.setSpacing(0)

        self.side_menu_top_widget = QWidget()
        self.side_menu_top_widget.setMinimumHeight(50)

        self.side_menu_top_layout = QVBoxLayout(self.side_menu_top_widget)
        self.side_menu_top_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_btn = PushButton("Toggle")
        self.product_btn = PushButton("Produtos")
        self.people_btn = PushButton("Pessoas")
        self.sell_btn = PushButton("Vendas")
        self.services_btn = PushButton("Serviços")

        self.menu_btn.clicked.connect(self.toggleSideMenu)

        self.side_menu_top_layout.addWidget(self.menu_btn)
        self.side_menu_top_layout.addWidget(self.product_btn)
        self.side_menu_top_layout.addWidget(self.people_btn)
        self.side_menu_top_layout.addWidget(self.sell_btn)
        self.side_menu_top_layout.addWidget(self.services_btn)

        self.side_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.side_menu_bottom_widget = QWidget()
        self.side_menu_bottom_widget.setMinimumHeight(50)

        self.side_menu_bottom_layout = QVBoxLayout(self.side_menu_bottom_widget)
        self.side_menu_bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.settings_btn = PushButton("Configurações")

        self.side_menu_bottom_layout.addWidget(self.settings_btn)

        self.side_menu_layout.addWidget(self.side_menu_top_widget)
        self.side_menu_layout.addItem(self.side_menu_spacer)
        self.side_menu_layout.addWidget(self.side_menu_bottom_widget)

        # END: side_menu

        self.content = QWidget()
        self.content.setStyleSheet("background-color: #D9D9D9")

        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.product_page = QWidget()

        self.product_page_layout = QVBoxLayout(self.product_page)

        self.product_search_widget = QWidget()
        self.setMaximumHeight(50)

        self.product_search_layout = QHBoxLayout(self.product_search_widget)
        self.product_search_layout.setContentsMargins(0, 0, 0, 0)
        self.product_search_layout.setSpacing(0)

        self.product_search_input = LineEdit("Procure por um produto...")

        self.product_search_layout.addWidget(self.product_search_input)

        self.product_buttons_widget = QWidget()

        self.product_buttons_layout = QHBoxLayout(self.product_buttons_widget)
        self.product_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.product_buttons_layout.setSpacing(12)

        self.product_add_btn = PageButton("Adicionar")
        self.product_edit_btn = PageButton("Editar")
        self.product_remove_btn = PageButton("Remover")

        self.product_buttons_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.product_buttons_layout.addWidget(self.product_add_btn)
        self.product_buttons_layout.addWidget(self.product_edit_btn)
        self.product_buttons_layout.addWidget(self.product_remove_btn)
        self.product_buttons_layout.addItem(self.product_buttons_spacer)

        self.product_table = QTableWidget()

        self.product_page_layout.addWidget(self.product_search_widget)
        self.product_page_layout.addWidget(self.product_buttons_widget)
        self.product_page_layout.addWidget(self.product_table)

        self.content_layout.addWidget(self.product_page)

        self.main_layout.addWidget(self.side_menu)
        self.main_layout.addWidget(self.content)

        self.setCentralWidget(self.central_widget)

    def toggleSideMenu(self, checked):
        current_width = self.side_menu.width()

        new_width = 50
        if current_width == 50:
            new_width = 250

        self.animation = QPropertyAnimation(self.side_menu, b"minimumWidth")
        self.animation.setStartValue(self.side_menu.width())
        self.animation.setEndValue(new_width)
        self.animation.setDuration(100)
        self.animation.start()