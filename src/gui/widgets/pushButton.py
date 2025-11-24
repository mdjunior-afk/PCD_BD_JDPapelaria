from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from src.gui.widgets.baseWidgets import ButtonBase
from src.gui.colors import *

class PushButton(ButtonBase):
    def __init__(self, text="", icon_path="", is_active="", type="WithBackground"):
        super().__init__(text, icon_path, is_active)

        self.type = type

        self.setObjectName("Button")

        self.setFocusPolicy(Qt.NoFocus)

        self.setFixedHeight(36)

    def setStyle(self, config):
        _style = ""

        if "WithBackground" in self.type:
                _style = f"""
                QPushButton {{
                    background-color: {config["PRIMARY_COLOR"]};
                    border: 1px solid {config["PRIMARY_COLOR"]};
                    color: {config["BACKGROUND_COLOR"]};

                    padding-left: 40px;
                }}

                QPushButton:hover {{
                    background-color: {config["PRIMARY_COLOR_HOVER"]};
                    border-color: {config["PRIMARY_COLOR_HOVER"]};
                    color: {config["BACKGROUND_COLOR"]};
                }}
            """
        elif "WithoutBackground" in self.type:
            _style = f"""
                QPushButton {{
                    background-color: transparent !important;
                    border: 1px solid {config["PRIMARY_COLOR"]};
                    color: {config["PRIMARY_COLOR"]};

                    padding-left: 40px;
                }}

                QPushButton:hover {{
                    background-color: {config["PRIMARY_COLOR_HOVER"]};
                    border-color: {config["PRIMARY_COLOR_HOVER"]};
                    color: {config["BACKGROUND_COLOR"]};
                }}
            """

        self.setStyleSheet(_style)