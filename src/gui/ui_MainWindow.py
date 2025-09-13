from PySide6.QtWidgets import *
from PySide6.QtGui import QColor
from PySide6.QtCore import QPropertyAnimation

from gui.widgets.PushButton import PushButton
from gui.widgets.PageButton import PageButton
from gui.widgets.LineEdit import LineEdit

from gui.pages.PageManager import PageManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JD Papelaria")
        
        self.resize(1280, 720)
        self.setMinimumSize(800, 600)

        self.central_widget = QWidget()
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # START: side_menu
        self.side_menu = QWidget()
        self.side_menu.setStyleSheet("background-color: #EFEFEF")
        self.side_menu.setMaximumWidth(50)

        self.side_menu_layout = QVBoxLayout(self.side_menu)
        self.side_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_layout.setSpacing(0)

        self.side_menu_top_widget = QWidget()
        self.side_menu_top_widget.setMinimumHeight(50)

        self.side_menu_top_layout = QVBoxLayout(self.side_menu_top_widget)
        self.side_menu_top_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_top_layout.setSpacing(0)

        self.menu_btn = PushButton("Menu", icon_path="menu-burger.svg")
        self.home_btn = PushButton("Home", icon_path="home.svg")
        self.product_btn = PushButton("Produtos", icon_path="boxes.svg", is_active=True)
        self.people_btn = PushButton("Pessoas", icon_path="users-alt.svg")
        self.sell_btn = PushButton("Vendas", icon_path="shopping-cart.svg")
        self.services_btn = PushButton("Serviços", icon_path="print.svg")

        self._all_btns = [self.home_btn, self.product_btn, self.people_btn, self.sell_btn, self.services_btn]

        self.menu_btn.clicked.connect(self.toggleSideMenu)
        self.product_btn.clicked.connect(self.productPage)
        self.people_btn.clicked.connect(self.peoplePage)

        self.side_menu_top_layout.addWidget(self.menu_btn)
        self.side_menu_top_layout.addWidget(self.home_btn)
        self.side_menu_top_layout.addWidget(self.product_btn)
        self.side_menu_top_layout.addWidget(self.people_btn)
        self.side_menu_top_layout.addWidget(self.sell_btn)
        self.side_menu_top_layout.addWidget(self.services_btn)

        self.side_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.side_menu_bottom_widget = QWidget()
        self.side_menu_bottom_widget.setMinimumHeight(50)

        self.side_menu_bottom_layout = QVBoxLayout(self.side_menu_bottom_widget)
        self.side_menu_bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.settings_btn = PushButton("Configurações", icon_path="settings.svg")

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

        self.page_manager = PageManager()

        self.content_layout.addWidget(self.page_manager)

        self.main_layout.addWidget(self.side_menu)
        self.main_layout.addWidget(self.content)

        self.setCentralWidget(self.central_widget)

    def productPage(self):
        self.product_btn.setActive(True)

        for btn in self._all_btns:
            if btn is not self.product_btn:
                btn.setActive(False)
                
        self.page_manager.setCurrentIndex(0)

    def peoplePage(self):
        self.people_btn.setActive(True)
        
        for btn in self._all_btns:
            if btn is not self.people_btn:
                btn.setActive(False)
        
        self.page_manager.setCurrentIndex(1)

    def toggleSideMenu(self):
        current_width = self.side_menu.width()

        new_width = 50
        if current_width == 50:
            new_width = 250

        self.animation = QPropertyAnimation(self.side_menu, b"minimumWidth")
        self.animation.setStartValue(self.side_menu.width())
        self.animation.setEndValue(new_width)
        self.animation.setDuration(50)
        self.animation.start()