from PySide6.QtWidgets import QLabel

from ..config import *

class Label(QLabel):
    def __init__(self, text):
        super().__init__(text)

        style = f"""
        QLabel {{
            color: {TEXT_COLOR} !important;
            background-color: transparent;
        }}
        """

        self.setStyleSheet(style)