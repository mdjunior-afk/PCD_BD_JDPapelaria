from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QAction, QIcon, QFontMetrics

from ..config import *

class LineComplement(QWidget):
    def __init__(self, placeholder="", items=[], property="WithComplement"):
        super().__init__()

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 6, 6)

        self.search_input = SearchInput(placeholder, property)
        self.search_input.setMaximumWidth(1200)
        self.complement_input = None

        layout.addWidget(self.search_input)
        
        if "WithComplement" in property:
            if not items:
                self.complement_input = StockInput()
                self.complement_input.setReadOnly(True)
                self.complement_input.setMaximumWidth(75)
            else:
                self.complement_input = CategoryInput(items)

            layout.addWidget(self.complement_input)

        self.setLayout(layout)

class SearchInput(QLineEdit):
    def __init__(self, placeholder="", property="WithComplement"):
        super().__init__()
        self.setObjectName("SearchInput")

        self.setProperty("class", property)

        self.setFixedHeight(36)

        self.setPlaceholderText(placeholder)

        search_icon_path = 'src/gui/icons/search.svg'
        search_action = QAction(QIcon(search_icon_path), '', self)
        
        self.addAction(search_action, QLineEdit.LeadingPosition)

        self.applyShadow()
        self.setColor()

    def setColor(self):
        _style = f"""
        QLineEdit#SearchInput {{
            color: {TEXT_COLOR} !important;
            background-color: {LINE_EDIT_BACKGROUND_COLOR} !important;
        }}
        """

        self.setStyleSheet(_style)

    def applyShadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

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
            color: {LINE_EDIT_BACKGROUND_COLOR};
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_COLOR2});
            font-size: 14px;
            padding: 8px;
            border-top-left-radius: 0;
            border-top-right-radius: 8px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 8px;
        }}
        """

        self.setStyleSheet(style)

class CategoryInput(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.currentIndexChanged.connect(self.adjustWidth)

        self.addItems(items)

        self.setStyle()

        self.applyShadow()

    def adjustWidth(self):
        fm = QFontMetrics(self.font())
        text = self.currentText()
        width = fm.horizontalAdvance(text) + 40
        self.setFixedWidth(width)

    def applyShadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

    def setStyle(self):
        style = f"""
        QComboBox {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_COLOR2});
            color: {LINE_EDIT_BACKGROUND_COLOR};
            padding: 8px;
            
            border-top-left-radius: 0;
            border-top-right-radius: 8px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 8px;
            
            outline: none;
            box-shadow: none;
        }}

        QComboBox::drop-down {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_COLOR2});
        }}

        QComboBox:down-arrow {{
            image: url(src/gui/icons/caret-down.svg);
            width: 10px;
            height: 10px;
        }}
        """

        self.setStyleSheet(style)