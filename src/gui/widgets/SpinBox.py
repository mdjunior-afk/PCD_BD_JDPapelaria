from PySide6.QtWidgets import *

from ..config import *

class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        self.setStyle()

    def setStyle(self):
        style = f"""
        QSpinBox {{
        background-color: {BTN_TEXT_COLOR};
        border-radius: 8px;
        padding: 4px 20px 4px 4px;
        font-size: 14px;
        }}

        QSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
        }}

        QSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
        }}

        QSpinBox::up-arrow {{
        image: url(src/gui/icons/caret-up.svg);
        width: 10px;
        height: 10px;
        }}

        QSpinBox::down-arrow {{
        image: url(src/gui/icons/caret-down.svg);
        width: 10px;
        height: 10px;
        }}
        """

        self.setStyleSheet(style)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()

        self.setStyle()

    def setStyle(self):
        style = f"""
        QDoubleSpinBox {{
        background-color: {BTN_TEXT_COLOR};
        border-radius: 8px;
        padding: 4px 20px 4px 4px;
        font-size: 14px;
        }}

        QDoubleSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
        }}

        QDoubleSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
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
