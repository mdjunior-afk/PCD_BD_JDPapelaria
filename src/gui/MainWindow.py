from PySide6.QtWidgets import *
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import QPixmap

from gui.widgets import PushButton

from gui.pages.PageManager import PageManager

from .config import *

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
        self.side_menu.setStyleSheet(f"""
            background-color: {PRIMARY_COLOR};
        """)
        self.side_menu.setMaximumWidth(50)

        self.animation = QPropertyAnimation(self.side_menu, b"minimumWidth")
        self.animation.setDuration(200)

        self.side_menu_layout = QVBoxLayout(self.side_menu)
        self.side_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_layout.setSpacing(0)

        self.side_menu_top_widget = QWidget()
        self.side_menu_top_widget.setStyleSheet("background-color: none;")
        self.side_menu_top_widget.setMinimumHeight(50)

        self.side_menu_top_layout = QVBoxLayout(self.side_menu_top_widget)
        self.side_menu_top_layout.setContentsMargins(0, 0, 0, 0)
        self.side_menu_top_layout.setSpacing(0)

        self.logo_label = QLabel()
        self.logo_label.setFixedSize(233, 67)

        self.logo_label.setStyleSheet("padding: 8px;")

        self.logo_pixmap = QPixmap("src/gui/images/logo.png")
        self.logo_label.setScaledContents(True)

        self.logo_label.hide()

        self.menu_btn = PushButton("Menu", icon_path="menu-burger.svg")
        self.home_btn = PushButton("Home", icon_path="home.svg", is_active=True)
        self.product_btn = PushButton("Produtos", icon_path="boxes.svg")
        self.people_btn = PushButton("Pessoas", icon_path="users-alt.svg")
        self.sell_btn = PushButton("Vendas", icon_path="shopping-cart.svg")
        self.services_btn = PushButton("Serviços", icon_path="print.svg")
        self.invoice_entry_btn = PushButton("Notas de Entrada", icon_path="document.svg")

        self._all_btns = [self.home_btn, self.product_btn, self.people_btn, self.sell_btn, self.services_btn, self.invoice_entry_btn]

        self.menu_btn.clicked.connect(self.toggleSideMenu)
        self.home_btn.clicked.connect(self.homePage)
        self.product_btn.clicked.connect(self.productPage)
        self.people_btn.clicked.connect(self.peoplePage)
        self.sell_btn.clicked.connect(self.sellPage)
        self.services_btn.clicked.connect(self.servicePage)
        self.invoice_entry_btn.clicked.connect(self.invoicePage)

        self.side_menu_top_layout.addWidget(self.logo_label)
        self.side_menu_top_layout.addWidget(self.menu_btn)
        self.side_menu_top_layout.addWidget(self.home_btn)
        self.side_menu_top_layout.addWidget(self.product_btn)
        self.side_menu_top_layout.addWidget(self.people_btn)
        self.side_menu_top_layout.addWidget(self.sell_btn)
        self.side_menu_top_layout.addWidget(self.services_btn)
        self.side_menu_top_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.side_menu_top_layout.addWidget(self.invoice_entry_btn)

        self.side_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.side_menu_bottom_widget = QWidget()
        self.side_menu_bottom_widget.setStyleSheet("background-color: none;")
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
        self.content.setStyleSheet(f"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {CONTENT_COLOR}, stop: 1 {CONTENT_COLOR2}); color: {TEXT_COLOR}")

        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        self.content_layout.setSpacing(0)

        self.page_manager = PageManager()

        self.content_layout.addWidget(self.page_manager)

        self.main_layout.addWidget(self.side_menu)
        self.main_layout.addWidget(self.content)

        self.setCentralWidget(self.central_widget)

    def homePage(self):
        for btn in self._all_btns:
            btn.setActive(btn is self.home_btn)
                
        self.page_manager.setCurrentIndex(0)

    def productPage(self):
        for btn in self._all_btns:
            btn.setActive(btn is self.product_btn)
                
        self.page_manager.setCurrentIndex(1)

    def peoplePage(self):
        for btn in self._all_btns:
            btn.setActive(btn is self.people_btn)
        
        self.page_manager.setCurrentIndex(2)

    def sellPage(self):
        for btn in self._all_btns:
            btn.setActive(btn is self.sell_btn)
        
        self.page_manager.setCurrentIndex(3)

    def servicePage(self):
        for btn in self._all_btns:
            btn.setActive(btn is self.services_btn)

        self.page_manager.setCurrentIndex(4)

    def invoicePage(self):
        for btn in self._all_btns:
            btn.setActive(btn is self.invoice_entry_btn)

        self.page_manager.setCurrentIndex(5)

    def toggleSideMenu(self):
        current_width = self.side_menu.width()

        new_width = 50
        self.logo_label.clear()

        if current_width == 50:
            new_width = 250

            self.logo_label.setPixmap(self.logo_pixmap)

        self.side_menu.setFixedWidth(new_width)