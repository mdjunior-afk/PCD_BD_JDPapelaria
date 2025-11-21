from src.gui.widgets.baseWidgets import *
from PySide6.QtCore import Qt

from src.gui.colors import *

class SideMenuButton(ButtonBase):
    def __init__(self, text="", icon_path="", is_active=False):
        super().__init__(text, icon_path, is_active)
        self.is_active = is_active

        self.setObjectName("SideMenuButton")

        self.setFocusPolicy(Qt.NoFocus)

        # Button Size
        self.setMinimumWidth(50)
        self.setFixedHeight(40)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyle()

    def setStyle(self):
        base_style = f"""
        QPushButton {{
            color: {BTN_TEXT_COLOR};
            background-color: transparent !important;
        }}
        QPushButton:hover {{
            background: {SECONDARY_COLOR};
            color: {BTN_HOVER_TEXT_COLOR};
        }}
        """

        active_style = f"""
        QPushButton[active="true"] {{
            background: {SECONDARY_COLOR};
            color: {BTN_HOVER_TEXT_COLOR};
            border-right: 5px solid {CONTENT_COLOR};
        }}
        """
        
        self.setProperty("active", "true" if self.is_active else "false")

        full_style = base_style + active_style
        self.setStyleSheet(full_style)