from PySide6.QtWidgets import *

from src.gui.widgets.baseWidgets import ButtonBase
from src.gui.colors import *

class PushButton(ButtonBase):
    def __init__(self, text="", icon_path="", is_active="", type="WithBackground"):
        super().__init__(text, icon_path, is_active)

        self.setObjectName("Button")

        self.setFixedHeight(36)

        _style = ""

        if "WithBackground" in type:
                _style = f"""
                QPushButton {{
                    background-color: {PRIMARY_COLOR};
                    border: 1px solid {PRIMARY_COLOR};
                    color: {BACKGROUND_COLOR};

                    padding-left: 40px;
                }}

                QPushButton:hover {{
                    background-color: {PRIMARY_COLOR_HOVER};
                    border-color: {PRIMARY_COLOR_HOVER};
                    color: {BACKGROUND_COLOR};
                }}
            """
        elif "WithoutBackground" in type:
            _style = f"""
                QPushButton {{
                    background-color: transparent !important;
                    border: 1px solid {PRIMARY_COLOR};
                    color: {PRIMARY_COLOR};

                    padding-left: 40px;
                }}

                QPushButton:hover {{
                    background-color: {PRIMARY_COLOR_HOVER};
                    border-color: {PRIMARY_COLOR_HOVER};
                    color: {BACKGROUND_COLOR};
                }}
            """

        self.setStyleSheet(_style)