from PySide6 import *

from src.models.utilsModels import *

class UtilsController:
    @staticmethod
    def getLowerStocks(window):
        lower_stock = getLowerStocks()

        window.stock_info.info_label.setText(str(lower_stock[0] if lower_stock != None else "0"))

    def getAnniversaries(window):
        anniversaries = getAnniversaries()

        window.birthday_qtd.info_label.setText(str(anniversaries[0] if anniversaries != None else "0"))

    def getTodaySale(window):
        today_sale = getTodaySale()

        window.daily_sale.info_label.setText(str(today_sale[0] if today_sale != None else "0"))