from PySide6.QtWidgets import *

from src.gui.colors import *

class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()

        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        # ComboBox config
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

    def updateSize(self):
        self.setMinimumWidth(self.sizeHint().width() + 30)