from PySide6.QtWidgets import QLineEdit, QColorDialog
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap, QAction
from PySide6.QtCore import Qt, QSize

from src.gui.colors import *

class LineEdit(QLineEdit):
    def __init__(self, placeholder="", type="WithoutComplement"):
        super().__init__(placeholderText=placeholder)

        self.setProperty("type", type)

class ColorLineEdit(QLineEdit):
    def __init__(self, initial_color="#0A54C3", parent=None):
        super().__init__(parent=parent)

        self.setInputMask("\#HHHHHH;_")
        
        self.currentColor = QColor(initial_color)
        self.setText(self.currentColor.name().upper())

        # 1. Cria o QAction (O botão dentro do LineEdit)
        self.colorAction = QAction(self)
        self.colorAction.triggered.connect(self.openColorDialog)
        
        # 2. Adiciona o QAction na direita do LineEdit
        # O self.ActionPosition.Trailing coloca o botão à direita (ActionPosition.Leading seria à esquerda)
        self.addAction(self.colorAction, self.ActionPosition.TrailingPosition)
        
        # 3. Atualiza o ícone de amostra de cor
        self.updateColorIcon()
        
        # Opcional: Conecta a mudança de texto para validar e atualizar o ícone
        self.editingFinished.connect(self.handleTextChange)

        self.setProperty("type", "WithoutComplement")

    # Função para desenhar o ícone de amostra
    def createColorPixmap(self, color: QColor) -> QPixmap:
        # Define o tamanho do ícone (ajustável)
        size = QSize(20, 20)
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Desenha um quadrado ou círculo preenchido com a cor
        painter.setBrush(color)
        painter.drawRect(2, 2, size.width() - 4, size.height() - 4) # Desenha o quadrado
        
        # Desenha a borda
        painter.setPen(QColor(Qt.GlobalColor.gray))
        painter.drawRect(2, 2, size.width() - 4, size.height() - 4)
        
        painter.end()
        return pixmap

    # Atualiza o ícone do QAction
    def updateColorIcon(self):
        pixmap = self.createColorPixmap(self.currentColor)
        self.colorAction.setIcon(QIcon(pixmap))

    # Ação que abre o ColorDialog
    def openColorDialog(self):
        # Abre o ColorDialog com a cor atual como inicial
        color = QColorDialog.getColor(
            self.currentColor, 
            self, 
            "Selecione a Cor",
            QColorDialog.ColorDialogOption.ShowAlphaChannel # Opcional: mostra transparência
        )
        
        if color.isValid():
            self.currentColor = color
            self.setText(color.name().upper()) # Atualiza o texto do LineEdit
            self.updateColorIcon()            # Atualiza o ícone

    # Lida com a mudança manual de texto (se o usuário digitar um código hex)
    def handleTextChange(self):
        text = self.text().strip()
        
        # Tenta criar uma cor a partir do texto (suporta #RGB, #RRGGBB, nomes, etc.)
        new_color = QColor(text)
        
        if new_color.isValid():
            self.currentColor = new_color
            # Garante que o texto exibido é o código #RRGGBB em maiúsculas
            self.setText(self.currentColor.name().upper())
            self.updateColorIcon()
        else:
            # Se o código for inválido, volta para o código hex anterior válido
            self.setText(self.currentColor.name().upper())
