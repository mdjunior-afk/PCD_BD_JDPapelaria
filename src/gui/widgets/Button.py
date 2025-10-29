from PySide6.QtWidgets import *

from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt

import os

from ..config import *

class Button(QPushButton):
    def __init__(self, text, property="WithBackground", icon_path=""):
        super().__init__(text)

        self.setFixedHeight(36)

        self.property_text = property
        self.icon_path = icon_path

        _style = ""

        if "WithBackground" in property:
                _style = f"""
                QPushButton {{
                    background-color: {PRIMARY_COLOR};
                    border: 1px solid {PRIMARY_COLOR};
                    color: {BACKGROUND_COLOR};

                    padding-left: 40px;
                }}

                QPushButton:hover {{
                    background-color: {PRIMARY_COLOR2};
                    border-color: {PRIMARY_COLOR2};
                    color: {BACKGROUND_COLOR};
                }}
            """
        elif "WithoutBackground" in property:
            _style = f"""
                QPushButton {{
                    background-color: transparent !important;
                    border: 1px solid {PRIMARY_COLOR};
                    color: {PRIMARY_COLOR};
                }}

                QPushButton:hover {{
                    background-color: {PRIMARY_COLOR2};
                    border-color: {PRIMARY_COLOR2};
                    color: {BACKGROUND_COLOR};
                }}
            """

        self.setStyleSheet(_style)

    def paintEvent(self, event):
        super().paintEvent(event)
        
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        
        if self.underMouse():
            color = ICON_HOVER_COLOR
        else:
            color = ICON_COLOR
            
        self.drawIcon(qp, self.icon_path, 50, color)
        qp.end()

    def drawIcon(self, qp: QPainter, image_path: str, width: int, color: str):
        if not image_path:
            return

        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.normpath(os.path.join(current_dir, "..", "icons"))
        icon_path = os.path.normpath(os.path.join(path, image_path))
        
        if not os.path.exists(icon_path):
            return

        original_icon = QPixmap(icon_path)
        
        icon_size = 15
        icon_to_draw = original_icon.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        colored_icon = QPixmap(icon_to_draw.size())
        colored_icon.fill(Qt.transparent)

        painter = QPainter(colored_icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, icon_to_draw)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_icon.rect(), color)
        painter.end()

        x = (width - icon_size) / 2
        y = (self.height() - icon_size) / 2
        
        qp.drawPixmap(int(x), int(y), colored_icon)
