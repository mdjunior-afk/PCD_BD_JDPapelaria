from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..config import *

class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyle()

    def setStyle(self):
        style = f"""
        QComboBox {{
            background-color: {BTN_TEXT_COLOR};
            padding: 4px;
            border-radius: 8px;
            outline: none;
            box-shadow: none;
        }}

        QComboBox::drop-down {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
        }}

        QComboBox:down-arrow {{
            image: url(src/gui/icons/caret-down.svg);
            width: 10px;
            height: 10px;
        }}
        """

        self.setStyleSheet(style)