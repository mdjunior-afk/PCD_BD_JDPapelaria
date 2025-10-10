from PySide6.QtWidgets import *

from ..config import *

class StockInput(QSpinBox):
    def __init__(self):
        super().__init__()

    def setStyle(self):
        style = f"""
        QDoubleSpinBox {{
        background-color: {BTN_TEXT_COLOR};
        border-radius: 8px;
        padding: 8px 20px 8px 8px;
        font-size: 14px;
        }}

        QDoubleSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
        }}

        QDoubleSpinBox::up-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QDoubleSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
        }}

        QDoubleSpinBox::down-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QDoubleSpinBox::up-arrow {{
        image: url(src/gui/icons/caret-up.svg);
        width: 10px;
        height: 10px;
        }}

        QDoubleSpinBox::down-arrow {{
        image: url(src/gui/icons/caret-down.svg);
        width: 10px;
        height: 10px;
        }}
        """

        self.setStyleSheet(style)