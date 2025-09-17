from PySide6.QtWidgets import *

class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        self.setStyle()

    def setStyle(self):
        style = """
        QSpinBox {
        background-color: #EFEFEF;
        border-radius: 8px;
        padding: 4px 20px 4px 4px;
        font-size: 14px;
        }

        QSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background-color: #EA7712;
        }

        QSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background-color: #EA7712;
        }

        QSpinBox::up-arrow {
        image: url(src/gui/icons/caret-up.svg);
        width: 10px;
        height: 10px;
        }

        QSpinBox::down-arrow {
        image: url(src/gui/icons/caret-down.svg);
        width: 10px;
        height: 10px;
        }
        """

        self.setStyleSheet(style)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()

        self.setStyle()

    def setStyle(self):
        style = """
        QDoubleSpinBox {
        background-color: #EFEFEF;
        border-radius: 8px;
        padding: 4px 20px 4px 4px;
        font-size: 14px;
        }

        QDoubleSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            background-color: #EA7712;
        }

        QDoubleSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-bottom-right-radius: 8px;
            background-color: #EA7712;
        }

        QDoubleSpinBox::up-arrow {
        image: url(src/gui/icons/caret-up.svg);
        width: 10px;
        height: 10px;
        }

        QDoubleSpinBox::down-arrow {
        image: url(src/gui/icons/caret-down.svg);
        width: 10px;
        height: 10px;
        }
        """

        self.setStyleSheet(style)
