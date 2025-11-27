from PySide6.QtWidgets import *

from src.gui.colors import *
from src.gui.utils import *


class Tab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.shadow = createShadow()
        self.setGraphicsEffect(self.shadow)

    def setStyle(self, config):

        _style = f"""
        QTabWidget::pane {{
            background-color: {config["BACKGROUND_COLOR"]};
            border-top-right-radius: 8px;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;

            padding: 24px 0;
        }}

        QTabWidget > QWidget {{
            background: transparent;
        }}
        """

        self.setStyleSheet(_style)

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: transparent !important")