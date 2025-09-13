from PySide6.QtWidgets import *
from PySide6.QtGui import QColor

class LineEdit(QLineEdit):
    def __init__(self, placeholder="", maximum_width=600, font_size=14, text_color="#747474", background_color="#EFEFEF", text_padding=8, border_radius=16):
        super().__init__()

        self.setPlaceholderText(placeholder)
        self.setMaximumWidth(maximum_width)

        self.font_size = font_size
        self.text_color = text_color
        self.background_color = background_color
        self.text_padding = text_padding
        self.border_radius = border_radius

        self.setStyle()

    def setStyle(self):
        style = f"""
        QLineEdit {{
            color: {self.text_color};
            background-color: {self.background_color};
            font-size: {self.font_size}px;
            padding: {self.text_padding}px;
            border-radius: {self.border_radius}px;
        }}
        """

        self.setStyleSheet(style)