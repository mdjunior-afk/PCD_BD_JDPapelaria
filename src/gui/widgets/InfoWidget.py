from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, Qt

class InfoWidget(QFrame):
    def __init__(self, background_color="#EFEFEF", border_radius=10, title="", title_color="#747474", info="", info_color="#EA7712"):
        super().__init__()

        self.background_color = background_color
        self.title_color = title_color
        self.info_color = info_color
        self.border_radius = border_radius

        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)

        # Label título
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: {title_color}; font-size: 14px;")
        layout.addWidget(self.title_label, alignment=Qt.AlignLeft)

        # Label valor
        self.info_label = QLabel(info)
        self.info_label.setStyleSheet(f"color: {info_color}; font-size: 20px; font-weight: bold;")
        layout.addWidget(self.info_label, alignment=Qt.AlignLeft)

        # Estilo inicial
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.background_color};
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
                background-color: {self.info_color};
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet("color: white; font-size: 14px;")
        self.info_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.background_color};
                border-radius: {self.border_radius}px;
            }}
        """)
        self.title_label.setStyleSheet(f"color: {self.title_color}; font-size: 14px;")
        self.info_label.setStyleSheet(f"color: {self.info_color}; font-size: 20px; font-weight: bold;")
        super().leaveEvent(event)