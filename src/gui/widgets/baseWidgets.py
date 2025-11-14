from PySide6.QtWidgets import *
from PySide6.QtGui import QPainter, Qt, QPixmap

from gui.colors import *

import os

class ButtonBase(QPushButton):
    def __init__(self, text="", icon_path="", is_active=False):
        super().__init__()
        self.icon_path = icon_path
        self.is_active = is_active

        self.setText(text)

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
            
        self.drawIcon(qp, self.icon_path, 45, color)
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
        icon_size = 16 # Tamanho fixo do ícone em pixels
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
