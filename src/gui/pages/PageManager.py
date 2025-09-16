from PySide6.QtWidgets import *

from gui.widgets import *

from . import *

class PageManager(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.home_page = HomePage()
        self.insertWidget(0, self.home_page)

        self.product_page = ProductPage()
        self.insertWidget(1, self.product_page)

        self.people_page = PeoplePage()
        self.insertWidget(2, self.people_page)

        self.sell_page = SellPage()
        self.insertWidget(3, self.sell_page)