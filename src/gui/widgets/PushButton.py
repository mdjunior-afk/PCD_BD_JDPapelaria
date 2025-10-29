from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, Qt, QPixmap

from ..config import *

import os

class PushButton(QPushButton):
    def __init__(self, text="", minimum_width=50, height=40, text_padding=55, icon_path="", is_active=False):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setCursor(Qt.PointingHandCursor)  # Adiciona cursor de mão ao passar o mouse

        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.icon_path = icon_path
        self.is_active = is_active

        self.first = False

        self.setStyle()

    def setStyle(self):
        base_style = f"""
        QPushButton {{
            font-size: 12px;
            color: {BTN_TEXT_COLOR};
            background-color: transparent !important;
            padding-left: {self.text_padding}px;
            text-align: left;
            border: none;
        }}
        QPushButton:hover {{
            background: {SECONDARY_COLOR};
            color: {BTN_HOVER_TEXT_COLOR}; /* O texto também muda de cor ao hover */
        }}
        """

        active_style = f"""
        QPushButton[active="true"] {{
            background: {SECONDARY_COLOR};
            color: {BTN_HOVER_TEXT_COLOR};
            border-right: 5px solid {CONTENT_COLOR};
        }}
        """
        
        self.setProperty("active", "true" if self.is_active else "false")
        
        # Junte os estilos
        full_style = base_style + active_style
        self.setStyleSheet(full_style)

    def setActive(self, value):
        self.is_active = value

        self.setStyle()

    def paintEvent(self, event):
        # A forma mais simples é deixar o QPushButton desenhar tudo e depois adicionar o ícone.
        super().paintEvent(event)
        
        # Cria o QPainter para desenhar o ícone
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        
        # Define a cor do ícone
        if self.underMouse() or self.is_active:
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
        icon_size = 15 # Tamanho fixo do ícone em pixels
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