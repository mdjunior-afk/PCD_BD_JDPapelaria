from PySide6.QtWidgets import QGroupBox
from PySide6.QtGui import QColor, QPalette

from ..config import *

class GroupBox(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

        self.setColor()

    def setColor(self):
        _style = f"""
        QGroupBox {{
            background-color: transparent !important;
        }}
        """

        self.setStyleSheet(_style)