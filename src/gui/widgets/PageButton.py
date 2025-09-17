from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt

from ..config import *

import os

class PageButton(QPushButton):
    def __init__(self, text="", minimum_width=50, height=40, text_padding=45, icon_path=""):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setMaximumWidth(125)
        self.setCursor(Qt.PointingHandCursor)

        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.icon_path = icon_path

        self.is_hovered = False
        self.setStyle()

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

    def setStyle(self):
        style = f"""
        QPushButton {{
            color: {BTN_TEXT_COLOR};
            font-size: 12px;
            background-color: {BTN_BACKGROUND_COLOR};
            padding-right: 10px;
            padding-left: {self.text_padding}px;
            text-align: left;
            border: none;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            color: {BTN_HOVER_TEXT_COLOR};
            background-color: {BTN_HOVER_BACKGROUND_COLOR};
        }}
        """

        self.setStyleSheet(style)

    def paintEvent(self, event):
        # A forma mais simples é deixar o QPushButton desenhar tudo e depois adicionar o ícone.
        super().paintEvent(event)
        
        # Cria o QPainter para desenhar o ícone
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        
        # Define a cor do ícone
        if self.underMouse():
            color = ICON_HOVER_COLOR # Cor branca no hover
        else:
            color = ICON_COLOR # Cor padrão
            
        self.drawIcon(qp, self.icon_path, self.minimum_width, color)
        qp.end()

    def drawIcon(self, qp: QPainter, image_path: str, width: int, color: str):
        if not image_path:
            return

        # Caminho do arquivo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.normpath(os.path.join(current_dir, "..", "icons"))
        icon_path = os.path.normpath(os.path.join(path, image_path))
        
        if not os.path.exists(icon_path):
            return

        original_icon = QPixmap(icon_path)
        
        # Redimensiona o ícone para caber na área reservada (se precisar)
        icon_size = 20 # Tamanho fixo do ícone em pixels
        icon_to_draw = original_icon.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Cria uma nova QPixmap para colorir o ícone
        colored_icon = QPixmap(icon_to_draw.size())
        colored_icon.fill(Qt.transparent)

        painter = QPainter(colored_icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, icon_to_draw)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_icon.rect(), color)
        painter.end()

        # Calcula a posição central do ícone dentro da área reservada (que é width)
        x = (width - icon_size) / 2
        y = (self.height() - icon_size) / 2
        
        # Desenha o ícone na posição calculada
        qp.drawPixmap(int(x), int(y), colored_icon)