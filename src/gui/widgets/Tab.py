from PySide6.QtWidgets import *
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from ..config import *

class Tab(QTabWidget):
    def __init__(self):
        super().__init__()

        _style = f"""
        QTabWidget::pane {{
            background: {BACKGROUND_COLOR};
            border: none; 
            border-top-right-radius: 8px;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;

            padding: 24px 0;
        }}

        QTabWidget > QWidget {{
            background: transparent;
        }}
        """

        self.setStyleSheet(_style)
        self.createShadow()

    def createShadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()

