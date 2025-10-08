from PySide6.QtWidgets import QGroupBox

from ..config import *

class GroupBox(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

        style = f"""
        QGroupBox {{
            margin-top: 1ex;
            padding: 1ex;

            background-color: {GROUP_BOX_BG_COLOR};
            color: {TEXT_COLOR};

            border: 2px solid lightgray;
            border-radius: 8px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;

            padding: 0 3px;

            font-weight: bold;
        }}
        """

        self.setStyleSheet(style)