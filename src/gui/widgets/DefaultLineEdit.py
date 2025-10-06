from PySide6.QtWidgets import *
from PySide6.QtGui import QColor

from ..config import *

class DefaultLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setStyle()

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

    def setStyle(self):
        style = f"""
        QLineEdit {{
            background-color: {LINE_BACKGROUND_COLOR};
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }}
        
        
        """

        self.setStyleSheet(style)