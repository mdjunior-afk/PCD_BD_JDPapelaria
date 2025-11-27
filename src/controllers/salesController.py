from src.models.saleModel import *

class SalesController:
    @staticmethod
    def saveSale(data={}):
        print(f"add: {data}")

        addSale(data)

    @staticmethod
    def removeSale(data={}):
        pass