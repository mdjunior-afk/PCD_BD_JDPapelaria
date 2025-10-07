from PySide6.QtWidgets import QLabel

class Label(QLabel):
    def __init__(self, text):
        super().__init__(text)

        style = """
        QLabel {
            background-color: transparent;
        }
        """

        self.setStyleSheet(style)