from PySide6.QtWidgets import QLabel

class Label(QLabel):
    def __init__(self, text="", type="Normal"):
        super().__init__(text)

        self.setProperty("type", type)

