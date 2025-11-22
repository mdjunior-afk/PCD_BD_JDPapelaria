from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from src.gui.pageManager import *
from src.gui.widgets import *
from src.gui.colors import *

import os, json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.content = None

        self.applyStyle()

        # Menu Buttons
        self.home_button = None
        self.product_button = None
        self.people_button = None
        self.sell_button = None
        self.services_button = None
        self.invoice_entry_button = None
        self.settings_button = None
        self.menu_buttons = []

        # Configurações da janela
        self.setWindowTitle("JD Papelaria")    
        self.resize(1280, 720)
        self.setMinimumSize(800, 600)

        widget = QWidget()
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.side_menu = self.createSideMenu()

        self.content, self.page_manager = self.createContent()

        layout.addWidget(self.side_menu)
        layout.addWidget(self.content)

        widget.setLayout(layout)

        self.home_page()

        self.setCentralWidget(widget)

        self.applyStyle()

    def createContent(self):
        widget = QWidget()

        layout = QVBoxLayout()

        page_manager = PageManager(self)

        layout.addWidget(page_manager)

        widget.setLayout(layout)

        return widget, page_manager

    def createSideMenu(self):
        widget = QWidget()
        widget.setObjectName("SideMenu")
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
        self.product_button = SideMenuButton("Produtos", icon_path="box-open-full.svg")
        self.people_button = SideMenuButton("Pessoas", icon_path="users-alt.svg")
        self.sell_button = SideMenuButton("Vendas", icon_path="shopping-basket.svg")
        self.services_button = SideMenuButton("Serviços", icon_path="print.svg")
        #self.invoice_entry_button = SideMenuButton("Notas de Entrada", icon_path="document.svg")

        # Buttons Connections
        menu_button.clicked.connect(self.toggle_side_menu)
        self.home_button.clicked.connect(self.home_page)
        self.product_button.clicked.connect(self.product_page)
        self.people_button.clicked.connect(self.people_page)
        self.sell_button.clicked.connect(self.sell_page)
        self.services_button.clicked.connect(self.service_page)
        #self.invoice_entry_button.clicked.connect(self.invoice_page)

        # Add Top Inputs
        top_layout.addWidget(menu_button)
        top_layout.addWidget(self.home_button)
        top_layout.addWidget(self.product_button)
        top_layout.addWidget(self.people_button)
        top_layout.addWidget(self.sell_button)
        top_layout.addWidget(self.services_button)
        #top_layout.addWidget(self.invoice_entry_button)

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
        self.settings_button = SideMenuButton("Configurações", icon_path="monitor-sun.svg")

        self.settings_button.clicked.connect(self.settings_page)

        # Add Bottom Inputs
        bottom_layout.addWidget(self.settings_button)

        # Add Layout Inputs
        layout.addWidget(top_widget)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(bottom_widget)

        widget.setLayout(layout)

        self.menu_buttons = [self.home_button, self.product_button, self.people_button, self.sell_button, self.services_button, self.settings_button]

        return widget
    
    def applyStyle(self):
        qss_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        
        with open("src/configuration.json", "r") as f:
            config = json.load(f)

        theme = config["THEME"]

        if theme == "dark":
            content_color = config["DARK_CONTENT_COLOR"]
            text_color = config["DARK_TEXT_COLOR"]
            subtitle_color = config["DARK_SUBTITLE_COLOR"]
            background_color = config["DARK_BACKGROUND_COLOR"]
            content_color = config["DARK_CONTENT_COLOR"]
        else:
            content_color = config["LIGHT_CONTENT_COLOR"]
            text_color = config["LIGHT_TEXT_COLOR"]
            subtitle_color = config["LIGHT_SUBTITLE_COLOR"]
            background_color = config["LIGHT_BACKGROUND_COLOR"]
            content_color = config["LIGHT_CONTENT_COLOR"]
        
        with open(qss_path, "r") as f:
            _style = f.read()
            _style = _style.format(
                SIDE_MENU_LABEL_SIZE=config["SIDE_MENU_LABEL_SIZE"],
                NORMAL_LABEL_SIZE=config["NORMAL_LABEL_SIZE"],
                INPUT_LABEL_SIZE=config["INPUT_LABEL_SIZE"],
                TITLE_LABEL_SIZE=config["TITLE_LABEL_SIZE"],
                SUBTITLE_LABEL_SIZE=config["SUBTITLE_LABEL_SIZE"],
                
                PRIMARY_COLOR=config["PRIMARY_COLOR"],
                PRIMARY_COLOR_HOVER=config["PRIMARY_COLOR_HOVER"],

                SECONDARY_COLOR=config["SECONDARY_COLOR"],
                SECONDARY_COLOR_HOVER=config["SECONDARY_COLOR_HOVER"],
                
                BTN_BACKGROUND_COLOR=config["BTN_BACKGROUND_COLOR"],
                BTN_TEXT_COLOR=config["BTN_TEXT_COLOR"],
                BTN_HOVER_BACKGROUND_COLOR=config["BTN_HOVER_BACKGROUND_COLOR"],
                BTN_HOVER_TEXT_COLOR=config["BTN_HOVER_TEXT_COLOR"],

                CONTENT_COLOR=content_color,
                TEXT_COLOR=text_color,
                SUBTITLE_COLOR=subtitle_color,
                BACKGROUND_COLOR=background_color,

                LINE_EDIT_BACKGROUND_COLOR=config["LINE_EDIT_BACKGROUND_COLOR"],
                GROUP_BOX_BACKGROUND_COLOR=config["GROUP_BOX_BACKGROUND_COLOR"],
                SHADOW_BACKGROUND_COLOR=config["SHADOW_BACKGROUND_COLOR"],

                ICON_COLOR=config["ICON_COLOR"],
                ICON_HOVER_COLOR=config["ICON_HOVER_COLOR"]
            )

            resolved_config = config.copy()
            resolved_config["CONTENT_COLOR"] = content_color
            resolved_config["TEXT_COLOR"] = text_color
            resolved_config["SUBTITLE_COLOR"] = subtitle_color
            resolved_config["BACKGROUND_COLOR"] = background_color            

            if self.content:
                self.content.setStyleSheet(f"background-color: {content_color}; color: {text_color};")

            for widget in self.findChildren(QPushButton):
                if widget.objectName() == "SideMenuButton":
                    widget.setStyle(resolved_config)
                if widget.objectName() == "Button":
                    widget.setStyle(resolved_config)

            for widget in self.findChildren(QTableWidget):
                widget.setStyle(resolved_config)

            for widget in self.findChildren(InfoWidget):
                widget.setStyle(resolved_config)

            for widget in self.findChildren(QTabWidget):
                widget.setStyle(resolved_config)

            QApplication.instance().setStyleSheet(_style)

            self.setCursor(Qt.ArrowCursor)

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

        self.page_manager.setCurrentIndex(8)

    def settings_page(self):
        for button in self.menu_buttons:
            button.setActive(button is self.settings_button)

        self.page_manager.setCurrentIndex(5)        

    def toggle_side_menu(self):
        current_width = self.side_menu.width()

        new_width = 50

        if current_width == 50:
            new_width = 250

        self.side_menu.setFixedWidth(new_width)
