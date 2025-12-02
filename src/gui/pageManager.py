from PySide6.QtWidgets import *

from src.gui.pages import *

from src.controllers import *

class PageManager(QStackedWidget):
    def __init__(self, main_window):
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

        self.settings_page = SettingsPage(main_window)
        self.insertWidget(5, self.settings_page)

        self.currentChanged.connect(self.updateData)
    
    def updateData(self, index):
        if index == 1:
            ProductController.getCategories(self.product_page)
            ProductController.getBrands(self.product_page)
        elif index == 3:
            SalesController.getPaymentMethods(self.sell_page.transaction_tab.document_input)