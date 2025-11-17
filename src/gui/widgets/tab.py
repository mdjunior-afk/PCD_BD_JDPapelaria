from PySide6.QtWidgets import *

from src.gui.colors import *
from src.gui.utils import *


class Tab(QTabWidget):
    def __init__(self):
        super().__init__()

        _style = f"""
        QTabWidget::pane {{
            background: {BACKGROUND_COLOR};
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

        self.shadow = createShadow()
        self.setGraphicsEffect(self.shadow)

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: transparent !important")