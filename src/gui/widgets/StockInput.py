from PySide6.QtWidgets import *

from ..config import *

class StockInput(QSpinBox):
    def __init__(self):
        super().__init__()

        self.setStyle()