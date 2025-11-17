from PySide6.QtCore import Slot, Qt

import json

class Location():
    def __init__(self, estate_input, city_input):
        self.filename = "src/utils/estados-cidades.json"
        self.data = {}

        self.estate_input = estate_input
        self.city_input = city_input

        self.estate_map = {}

    def loadData(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                return self.data['estados']
        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.filename}' não encontrado.")
            return []
        except json.JSONDecodeError:
            print(f"Erro: Conteúdo inválido no arquivo JSON.")
            return []
        
    def fillEstates(self):
        if not self.data:
            return
        
        self.estate_input.clear()
        self.estate_input.addItem("")
        
        self.estate_map = {}

        for estate in self.data['estados']:
            estate_acronym = estate['sigla']
            estate_name = estate['nome']

            self.estate_input.addItem(f'{estate_acronym}', userData=estate_acronym)

            self.estate_map[estate_acronym] = estate

    @Slot()
    def filterCities(self):
        self.city_input.clear()
        self.city_input.addItem("")

        selected_acronym = self.estate_input.currentData()

        if not selected_acronym:
            self.city_input.setPlaceholderText("Selecione o Estado primeiro")
            return

        self.city_input.setPlaceholderText("Selecione a cidade")

        selected_estate = self.estate_map.get(selected_acronym)

        if selected_estate and 'cidades' in selected_estate:
            cities = selected_estate['cidades']
            self.city_input.addItems(cities)

            self.current_city_list = [c.lower() for c in cities]
        else:
            self.current_city_list = []

    @Slot()
    def validateCity(self):
        text = self.city_input.lineEdit().text().strip()

        if not text:
            return
        
        lower_text = text.lower()

        if lower_text in self.current_city_list:
            index = self.city_input.findText(text, Qt.MatchFlag.MatchContains)
            if index >= 0:
                 self.city_input.setCurrentIndex(index)

            return
        
        self.city_input.lineEdit().clear()
        self.city_input.setCurrentIndex(0)
