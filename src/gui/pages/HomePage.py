from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ..widgets import *

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(6)

        self.search_widget = QWidget()
        
        self.search_layout = QHBoxLayout(self.search_widget)
        self.search_layout.setContentsMargins(0, 0, 0, 12)

        self.search_input = LineComplement(placeholder="Procure por algo", property="WithoutComplement")

        self.search_layout.addWidget(self.search_input)

        self.box_widget = self.createBoxInputs()

        self.home_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.logo_widget = QWidget()
        self.logo_layout = QHBoxLayout()
        
        self.logo_label = QLabel()
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(233, 67)
        self.logo_pixmap = QPixmap("src/gui/images/logo.png")
        self.logo_label.setPixmap(self.logo_pixmap)

        self.logo_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.logo_layout.addWidget(self.logo_label)
        self.logo_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.logo_widget.setLayout(self.logo_layout)

        self.main_layout.addWidget(self.search_widget)
        self.main_layout.addWidget(self.box_widget)
        self.main_layout.addItem(self.home_spacer)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.logo_widget)
        self.main_layout.addStretch(2)

        self.setStyleSheet("""
        QWidget {
            background-color: transparent !important;
        }

        """)
    def createBoxInputs(self):
        widget = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(6)

        widget.setLayout(layout)

        stock_info = InfoWidget(title="Estoques baixos", info="10")
        birthday_info = InfoWidget(title="Aniversáriantes do mês", info="3")
        sell_info = InfoWidget(title="Vendas de hoje", info="R$1200,00")

        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(stock_info)
        layout.addWidget(sell_info)
        layout.addWidget(birthday_info)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        return widget