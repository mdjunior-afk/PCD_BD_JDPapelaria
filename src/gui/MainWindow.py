from PySide6.QtWidgets import * 

from gui.pages.PageManager import PageManager
from gui.widgets import SideMenuButton

from .config import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Menu Buttons
        self.home_button = None
        self.product_button = None
        self.people_button = None
        self.sell_button = None
        self.services_button = None
        self.invoice_entry_button = None
        self.menu_buttons = []

        self.setWindowTitle("JD Papelaria")
        
        self.resize(1280, 720)
        self.setMinimumSize(800, 600)

        widget = QWidget()
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.side_menu = self.create_side_menu()

        content, self.page_manager = self.create_content()

        layout.addWidget(self.side_menu)
        layout.addWidget(content)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def create_content(self):
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {CONTENT_COLOR}; color: {TEXT_COLOR};")

        layout = QVBoxLayout()

        page_manager = PageManager()

        layout.addWidget(page_manager)

        widget.setLayout(layout)

        return widget, page_manager

    def create_side_menu(self):
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {PRIMARY_COLOR};")
        widget.setMaximumWidth(50)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top Widget
        top_widget = QWidget()
        top_widget.setStyleSheet("background-color: none;")
        top_widget.setMinimumHeight(50)

        # Top Layout
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        top_widget.setLayout(top_layout)

        # Top Inputs
        menu_button = SideMenuButton("Menu", icon_path="menu-burger.svg")
        self.home_button = SideMenuButton("Home", icon_path="home.svg", is_active=True)
        self.product_button = SideMenuButton("Produtos", icon_path="boxes.svg")
        self.people_button = SideMenuButton("Pessoas", icon_path="users-alt.svg")
        self.sell_button = SideMenuButton("Vendas", icon_path="shopping-cart.svg")
        self.services_button = SideMenuButton("Serviços", icon_path="print.svg")
        self.invoice_entry_button = SideMenuButton("Notas de Entrada", icon_path="document.svg")

        self.menu_buttons = [self.home_button, self.product_button, self.people_button, self.sell_button, self.services_button, self.invoice_entry_button]

        # Buttons Connections
        menu_button.clicked.connect(self.toggle_side_menu)
        self.home_button.clicked.connect(self.home_page)
        self.product_button.clicked.connect(self.product_page)
        self.people_button.clicked.connect(self.people_page)
        self.sell_button.clicked.connect(self.sell_page)
        self.services_button.clicked.connect(self.service_page)
        self.invoice_entry_button.clicked.connect(self.invoice_page)

        # Add Top Inputs
        top_layout.addWidget(menu_button)
        top_layout.addWidget(self.home_button)
        top_layout.addWidget(self.product_button)
        top_layout.addWidget(self.people_button)
        top_layout.addWidget(self.sell_button)
        top_layout.addWidget(self.services_button)
        top_layout.addWidget(self.invoice_entry_button)

        # Bottom Widget
        bottom_widget = QWidget()
        bottom_widget.setStyleSheet("background-color: none;")
        bottom_widget.setMinimumHeight(50)

        # Bottom Layout
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)

        bottom_widget.setLayout(bottom_layout)

        # Bottom Inputs
        settings_button = SideMenuButton("Configurações", icon_path="settings.svg")

        # Add Bottom Inputs
        bottom_layout.addWidget(settings_button)

        # Add Layout Inputs
        layout.addWidget(top_widget)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(bottom_widget)

        widget.setLayout(layout)

        return widget

    def home_page(self):
        for button in self.menu_buttons:
            button.setActive(button is self.home_button)
                
        self.page_manager.setCurrentIndex(0)

    def product_page(self):
        for button in self.menu_buttons:
            button.setActive(button is self.product_button)
                
        self.page_manager.setCurrentIndex(1)

    def people_page(self):
        for button in self.menu_buttons:
            button.setActive(button is self.people_button)
        
        self.page_manager.setCurrentIndex(2)

    def sell_page(self):
        for button in self.menu_buttons:
            button.setActive(button is self.sell_button)
        
        self.page_manager.setCurrentIndex(3)

    def service_page(self):
        for button in self.menu_buttons:
            button.setActive(button is self.services_button)

        self.page_manager.setCurrentIndex(4)

    def invoice_page(self):
        for button in self.menu_buttons:
            button.setActive(button is self.invoice_entry_button)

        self.page_manager.setCurrentIndex(5)

    def toggle_side_menu(self):
        current_width = self.side_menu.width()

        new_width = 50

        if current_width == 50:
            new_width = 250

        self.side_menu.setFixedWidth(new_width)
