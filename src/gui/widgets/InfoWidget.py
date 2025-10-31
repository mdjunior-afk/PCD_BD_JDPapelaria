from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, Qt

from ..config import *

class InfoWidget(QFrame):
    def __init__(self, title="", info=""):
        super().__init__()

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)

        # Title Label
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 14px;")
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Info Label
        self.info_label = QLabel(info)
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.info_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Style
        self.setStyleSheet(f"""
            QFrame {{
                background: {PRIMARY_COLOR2};
                border-radius: 8px;
            }}
        """)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setOffset(4, 4)
        shadow.setColor(QColor(0, 0, 0, 25))
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background: {SECONDARY_COLOR};
                border-radius: 8px;
            }}
        """)
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 14px;")
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background: {PRIMARY_COLOR2};
                border-radius: 8px;
            }}
        """)
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 14px;")
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        super().leaveEvent(event)
