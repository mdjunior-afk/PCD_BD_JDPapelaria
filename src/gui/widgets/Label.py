from PySide6.QtWidgets import QLabel

from ..config import *

class Label(QLabel):
    def __init__(self, text, property="Normal", fixed=True):
        super().__init__(text)

        if fixed:
            self.setMaximumWidth(100)

        self.setProperty("class", property)

        _style = ""

        if "Title" in property or "Normal" in property:
            _style = f"color: {TEXT_COLOR} !important;"
        elif "Subtitle" in property:
            _style = f"color: {SUBTITLE_COLOR} !important;"

        _style += "background: none;"

        self.setStyleSheet(_style)