from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, Qt

from ..config import *

class InfoWidget(QFrame):
    def __init__(self, border_radius=10, title="", info=""):
        super().__init__()

        self.border_radius = border_radius

        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)

        # Label título
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: {BTN_TEXT_COLOR}; font-size: 14px;")
        layout.addWidget(self.title_label, alignment=Qt.AlignLeft)

        # Label valor
        self.info_label = QLabel(info)
        self.info_label.setStyleSheet(f"color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.info_label, alignment=Qt.AlignLeft)

        # Estilo inicial
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BTN_BACKGROUND_COLOR};
                border-radius: {self.border_radius}px;
            }}
        """)

        # Sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setOffset(4, 4)
        shadow.setColor(QColor(0, 0, 0, 25))
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BTN_HOVER_BACKGROUND_COLOR};
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet(f"color: {BTN_TEXT_COLOR}; font-size: 14px;")
        self.info_label.setStyleSheet(f"color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BTN_BACKGROUND_COLOR};
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet(f"color: {BTN_TEXT_COLOR}; font-size: 14px;")
        self.info_label.setStyleSheet(f"color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        super().leaveEvent(event)