from PySide6.QtWidgets import *
from PySide6.QtGui import QColor

from gui.widgets import *

def createShadow() -> QGraphicsDropShadowEffect:
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(5)
    shadow.setColor(QColor(0, 0, 0, 25))
    shadow.setOffset(4, 4)

    return shadow

def createWindowButtons():
    widget = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)

    save_button = PushButton("Salvar", icon_path="disk.svg")
    new_button = PushButton("Novo", icon_path="plus.svg")
    cancel_button = PushButton("Cancelar", icon_path="cross.svg")

    layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
    layout.addWidget(save_button)
    layout.addWidget(new_button)
    layout.addWidget(cancel_button)

    return widget, (save_button, new_button, cancel_button)

def createTableButtons():
    widget = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)

    add_button = PushButton("Adicionar", icon_path="plus.svg")
    edit_button = PushButton("Editar", icon_path="edit.svg")
    remove_button = PushButton("Remover", icon_path="cross.svg")

    layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
    layout.addWidget(add_button)
    layout.addWidget(edit_button)
    layout.addWidget(remove_button)

    return widget, (add_button, edit_button, remove_button)