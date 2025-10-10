from PySide6.QtWidgets import *
from PySide6.QtGui import QColor

from ..config import *

class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        self.setMaximum(99999)

        self.setStyle()

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

    def setStyle(self):
        style = f"""
        QSpinBox {{
            background-color: {BTN_TEXT_COLOR};
            border-radius: 8px;
            padding: 8px 20px 8px 8px;
            font-size: 14px;
        }}

        QSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_COLOR2});
        }}

        QSpinBox::up-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR2}, stop: 1 {PRIMARY_COLOR});
        }}

        QSpinBox::down-button:hover {{
            background-color: {PRIMARY_COLOR2};
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

        self.setMaximum(99999)

        self.setStyle()

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

    def setStyle(self):
        style = f"""
        QDoubleSpinBox {{
        background-color: {LINE_EDIT_BACKGROUND_COLOR};
        border-radius: 8px;
        padding: 8px 20px 8px 8px;
        font-size: 14px;
        }}

        QDoubleSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_COLOR2});
        }}

        QDoubleSpinBox::up-button:hover {{
            background-color: {PRIMARY_COLOR2};
        }}

        QDoubleSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR2}, stop: 1 {PRIMARY_COLOR});
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
