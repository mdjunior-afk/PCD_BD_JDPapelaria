from PySide6.QtWidgets import *

from ..widgets import *

class BaseDialog(QDialog):
    def __init__(self):
        super().__init__()

    def save(self):
        pass