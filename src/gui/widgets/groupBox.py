from PySide6.QtWidgets import *

class GroupBox(QGroupBox):
    def __init__(self, title=""):
        super().__init__(title)