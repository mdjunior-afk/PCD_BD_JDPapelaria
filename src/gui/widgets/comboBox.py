from PySide6.QtWidgets import *

from gui.colors import *

class ComboBox(QComboBox):
    def __init__(self, items=[]):
        super().__init__()

        self.addItems(items)

        # ComboBox config
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        self.setStyle()

    def setStyle(self):
        _style = f"""
        QComboBox {{
            background-color: transparent !important;
            border: 1px solid lightgray;
        }}

        QComboBox:focus {{
            border-color: {PRIMARY_COLOR};
        }}

        """

        self.setStyleSheet(_style)