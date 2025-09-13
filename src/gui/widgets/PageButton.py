from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import Qt

class PageButton(QPushButton):
    def __init__(self, text="", minimum_width=50, height=40, text_padding=10, text_color="#747474", icon_path="", icon_color="#747474", btn_color="#EFEFEF", btn_hover="#EA7712"):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)

        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover

        self.setStyle()

    def setStyle(self):
        style = f"""
        QPushButton {{
            color: {self.text_color};
            background-color: {self.btn_color};
            padding: {self.text_padding}px;
            text-align: left;
            border: none;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            color: {self.btn_color};
            background-color: {self.btn_hover};
        }}
        """

        self.setStyleSheet(style)