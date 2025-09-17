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

        self.search_input = LineEdit("Procure por algo...")

        self.search_layout.addWidget(self.search_input)

        self.box_widget = QWidget()

        self.box_layout = QHBoxLayout(self.box_widget)
        self.box_layout.setContentsMargins(0, 0, 0, 12)
        self.box_layout.setSpacing(6)

        self.box_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.box_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.stock_info = InfoWidget(title="Estoques baixos", info="10")
        self.birthday_qtd = InfoWidget(title="Aniversáriantes do mês", info="3")
        self.daily_sell = InfoWidget(title="Vendas de hoje", info="R$1200,00")

        self.box_layout.addItem(self.box_left_spacer)
        self.box_layout.addWidget(self.stock_info)
        self.box_layout.addWidget(self.daily_sell)
        self.box_layout.addWidget(self.birthday_qtd)
        self.box_layout.addItem(self.box_right_spacer)

        self.home_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.logo_widget = QWidget()
        self.logo_layout = QHBoxLayout()
        
        self.logo_label = QLabel()
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(233, 67)
        self.logo_pixmap = QPixmap("src/gui1/images/logo.png")
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
        self.main_layout.addStretch(1)