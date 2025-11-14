from PySide6.QtWidgets import *

from gui.pages import *

class PageManager(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.home_page = HomePage()
        self.insertWidget(0, self.home_page)

        self.product_page = ProductPage()
        self.insertWidget(1, self.product_page)

        self.people_page = PersonPage()
        self.insertWidget(2, self.people_page)

        self.sell_page = SalesPage()
        self.insertWidget(3, self.sell_page)

        self.services_page = ServicePage()
        self.insertWidget(4, self.services_page)

        self.settings_page = SettingsPage()
        self.insertWidget(6, self.settings_page)