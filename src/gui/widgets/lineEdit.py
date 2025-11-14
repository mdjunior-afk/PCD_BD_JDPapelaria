from PySide6.QtWidgets import *

from gui.colors import *

class LineEdit(QLineEdit):
    def __init__(self, placeholder="", type="WithoutComplement"):
        super().__init__(placeholderText=placeholder)

        self.setProperty("type", type)
        self.setStyle()

    def setStyle(self):
        _style = f"""
        QLineEdit {{
            background-color: transparent !important;
            border: 1px solid lightgray;
        }}

        QLineEdit:focus {{
            border-color: {PRIMARY_COLOR};
        }}
        """

        self.setStyleSheet(_style)