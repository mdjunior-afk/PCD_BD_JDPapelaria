from PySide6.QtWidgets import *

from src.gui.colors import *

class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()

        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.setMinimumContentsLength(12)

        # ComboBox config
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)