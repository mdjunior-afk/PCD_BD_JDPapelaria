from PySide6.QtWidgets import *

from gui.widgets.LineEdit import LineEdit

class PageManager(QStackedWidget):
    def __init__(self):
        super().__init__()

        

        self.addWidget(self.product_page)