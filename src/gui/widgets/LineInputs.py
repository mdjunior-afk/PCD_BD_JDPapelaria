from PySide6.QtWidgets import *

from ..config import *

class SearchInput(QLineEdit):
    def __init__(self, placeholder="Digite aqui", max_width=300):
        super().__init__()

        self.setMinimumHeight(36)

        self.setMaximumWidth(max_width)
        self.setPlaceholderText(placeholder)

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