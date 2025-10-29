from PySide6.QtWidgets import *
from PySide6.QtGui import QColor

from ..config import *

class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        self.setMaximum(99999)

        self.setStyle()

    def setStyle(self):
        style = f"""
        QSpinBox {{
            background-color: transparent !important;
            border-radius: 8px;
            padding: 8px 20px 8px 8px;
            font-size: 12px;
            border: 1px solid lightgray;
        }}

        QSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background: transparent !important;
        }}

        QSpinBox::up-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background: transparent !important;
        }}

        QSpinBox::down-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QSpinBox::up-arrow {{
        image: url(gui/icons/angle-small-up.svg);
        width: 10px;
        height: 10px;
        }}

        QSpinBox::down-arrow {{
        image: url(gui/icons/angle-small-down.svg);
        width: 10px;
        height: 10px;
        }}
        """

        self.setStyleSheet(style)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()

        self.setMaximum(99999)

        self.setStyle()

    def setStyle(self):
        style = f"""
        QDoubleSpinBox {{
        background-color: transparent !important;
        border-radius: 8px;
        padding: 8px 20px 8px 8px;
        font-size: 12px;
        border: 1px solid lightgray;
        }}

        QDoubleSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background: transparent !important;
        }}

        QDoubleSpinBox::up-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QDoubleSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background: transparent !important;
        }}

        QDoubleSpinBox::down-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QDoubleSpinBox::up-arrow {{
        image: url(gui/icons/angle-small-up.svg);
        width: 10px;
        height: 10px;
        }}

        QDoubleSpinBox::down-arrow {{
        image: url(gui/icons/angle-small-down.svg);
        width: 10px;
        height: 10px;
        }}
        """

        self.setStyleSheet(style)
