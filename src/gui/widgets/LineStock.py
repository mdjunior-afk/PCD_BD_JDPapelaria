from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QAction, QIcon

from ..config import *

class LineStock(QWidget):
    def __init__(self, placeholder=""):
        super().__init__()

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(6, 6, 6, 6)

        self.search_input = SearchInput(placeholder)
        self.search_input.setMaximumWidth(1200)
        self.stock_input = StockInput()
        self.stock_input.setReadOnly(True)
        self.stock_input.setMaximumWidth(50)

        layout.addWidget(self.search_input)
        layout.addWidget(self.stock_input)

        self.setLayout(layout)

class SearchInput(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()

        self.setPlaceholderText(placeholder)

        search_icon_path = 'src/gui/icons/search.svg'
        search_action = QAction(QIcon(search_icon_path), '', self)
        
        self.addAction(search_action, QLineEdit.LeadingPosition)

        self.applyShadow()
        self.setStyle()

    def applyShadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

    def setStyle(self):
        style = f"""
        QLineEdit {{
            color: {TEXT_COLOR};
            background-color: {LINE_BACKGROUND_COLOR};
            font-size: 14px;
            padding: 8px;
            border-top-left-radius: 16px;
            border-top-right-radius: 0;
            border-bottom-left-radius: 16px;
            border-bottom-right-radius: 0;
        }}
        """

        self.setStyleSheet(style)

class StockInput(QLineEdit):
    def __init__(self):
        super().__init__()

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

        self.setStyle()

    def setStyle(self):
        style = f"""
        QLineEdit {{
            color: {LINE_BACKGROUND_COLOR};
            background-color: {SIDEMENU_COLOR};
            font-size: 14px;
            padding: 8px;
            border-top-left-radius: 0;
            border-top-right-radius: 16px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 16px;
        }}
        """

        self.setStyleSheet(style)