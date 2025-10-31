from PySide6.QtWidgets import *
from gui.widgets import Button

def create_add_buttons():
    widget = QWidget()
    widget.setStyleSheet("background: none;")
    layout = QHBoxLayout()

    add_button = Button("Salvar", icon_path="disk.svg")
    edit_button = Button("Novo", icon_path="plus.svg")
    remove_button = Button("Cancelar", icon_path="cross.svg")

    layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
    layout.addWidget(add_button)
    layout.addWidget(edit_button)
    layout.addWidget(remove_button)

    widget.setLayout(layout)

    return widget
