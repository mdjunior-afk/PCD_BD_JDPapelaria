from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, Qt

from src.gui.colors import *
from src.gui.utils import createShadow

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
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 14px;")
        layout.addWidget(self.title_label, alignment=Qt.AlignLeft)

        # Label valor
        self.info_label = QLabel(info)
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.info_label, alignment=Qt.AlignLeft)

        # Estilo inicial
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_COLOR});
                border-radius: {self.border_radius}px;
            }}
        """)

        # Sombra
        shadow = createShadow()
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {SECONDARY_COLOR}, stop: 1 {SECONDARY_COLOR});
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 14px;")
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_COLOR});
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 14px;")
        self.info_label.setStyleSheet(f"background-color: transparent !important; color: {BTN_TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        super().leaveEvent(event)