from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QAction, QIcon


class LineEdit(QLineEdit):
    def __init__(self, placeholder="", maximum_width=600, font_size=14, text_padding=8, border_radius=16, text_color="#747474", background_color="#EFEFEF"):
        super().__init__()

        self.setPlaceholderText(placeholder)  # tamanho inicial # limite

        self.setMaximumWidth(maximum_width)
        
        self.font_size = font_size
        self.text_color = text_color
        self.background_color = background_color
        self.text_padding = text_padding
        self.border_radius = border_radius

        search_icon_path = 'gui/icons/search.svg' # Exemplo de caminho relativo
        search_action = QAction(QIcon(search_icon_path), '', self)
        
        # Adiciona a ação (o ícone) ao lado esquerdo do QLineEdit
        self.addAction(search_action, QLineEdit.LeadingPosition)

        self.setStyle()

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

    def setStyle(self):
        style = f"""
        QLineEdit {{
            color: {self.text_color};
            background-color: {self.background_color};
            font-size: {self.font_size}px;
            padding: {self.text_padding}px;
            border-radius: {self.border_radius}px;
        }}
        """

        self.setStyleSheet(style)
