from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, Qt

from src.gui.colors import *
from src.gui.utils import createShadow

class InfoWidget(QFrame):
    def __init__(self, border_radius=10, title="", info=""):
        super().__init__()

        self.border_radius = border_radius

        self.primary_color = PRIMARY_COLOR
        self.secondary_color = SECONDARY_COLOR
        self.btn_text_color = BTN_TEXT_COLOR

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)

        # Label título
        self.title_label = QLabel(title)
        layout.addWidget(self.title_label, alignment=Qt.AlignLeft)

        # Label valor
        self.info_label = QLabel(info)
        layout.addWidget(self.info_label, alignment=Qt.AlignLeft)

        # Sombra
        shadow = createShadow()
        self.setGraphicsEffect(shadow)

    def setStyle(self, config):
        self.primary_color = config["PRIMARY_COLOR"]
        self.secondary_color = config["SECONDARY_COLOR"]
        self.btn_text_color = config["BTN_TEXT_COLOR"]

        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {self.btn_text_color}; font-size: 14px;")
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {self.btn_text_color}; font-size: 16px; font-weight: bold;")
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {self.primary_color}, stop: 1 {self.primary_color});
                border-radius: {self.border_radius}px;
            }}
        """)

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {self.secondary_color}, stop: 1 {self.secondary_color});
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {self.btn_text_color}; font-size: 14px;")
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {self.btn_text_color}; font-size: 16px; font-weight: bold;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {self.primary_color}, stop: 1 {self.primary_color});
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {self.btn_text_color}; font-size: 14px;")
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {self.btn_text_color}; font-size: 16px; font-weight: bold;")
        super().leaveEvent(event)