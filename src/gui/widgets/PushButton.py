from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, Qt, QPixmap
from PySide6.QtCore import QRect, QPoint

import os

class PushButton(QPushButton):
    def __init__(self, text="", minimum_width=50, height=40, text_padding=55, text_color="#747474", icon_path="", icon_color="#747474", btn_color="#EFEFEF", btn_hover="#EA7712", is_active=False):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setCursor(Qt.PointingHandCursor)  # Adiciona cursor de mão ao passar o mouse

        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.is_active = is_active

        self.is_hovered = False
        self.setStyle()

    def setStyle(self):
        # A forma mais simples de alterar a cor ao hover é no stylesheet
        # e não usando a cor de hover para o ícone. O Qt se encarrega disso.
        style = f"""
        QPushButton {{
            color: {self.text_color};
            background-color: {self.btn_color};
            padding-left: {self.text_padding}px;
            text-align: left;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {self.btn_hover};
            color: white; /* O texto também muda de cor ao hover */
        }}
        """
        style_active = f"""
        QPushButton {{
            background-color: {self.btn_hover};
            color: white;
            border-right: 5px solid #D9D9D9;
        }}

        """

        if (self.is_active):
            self.setStyleSheet(style + style_active)
        else:
            self.setStyleSheet(style)

    def setActive(self, value):
        self.is_active = value

        self.setStyle()

    def enterEvent(self, event):
        self.is_hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        # A forma mais simples é deixar o QPushButton desenhar tudo e depois adicionar o ícone.
        super().paintEvent(event)
        
        # Cria o QPainter para desenhar o ícone
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        
        # Define a cor do ícone
        if self.is_hovered or self.is_active:
            color = "#FFFFFF" # Cor branca no hover
        else:
            color = self.icon_color # Cor padrão
            
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