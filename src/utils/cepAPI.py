from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

import requests, json

def searchCEP(cep_input : QLineEdit, inputs={}):
    cep = cep_input.text()
    #self.warning_label.setText("Consultando...")

    cep = ''.join(filter(str.isdigit, cep))

    if len(cep) != 8:
        print("ERRO")
        return

    url = f"https://viacep.com.br/ws/{cep}/json/"

    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'erro' in data and data['erro']:
            print(f"CEP não encontrado!")
            return

        uf_do_cep = data['uf']
        estate_index = inputs["estate_input"].findData(uf_do_cep)

        if estate_index >= 0:
            inputs["estate_input"].setCurrentIndex(estate_index)

            city = data['localidade']

            city_index = inputs["city_input"].findText(city, Qt.MatchFlag.MatchExactly)
            if city_index >= 0:
                inputs["city_input"].setCurrentIndex(city_index)
            else:
                inputs["city_input"].lineEdit().setText(city)

        inputs["neighborhood_input"].setText(data["bairro"])
        inputs["street_input"].setText(data["logradouro"])

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar o ViaCEP: {e}")
        return None
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON.")
        return None
    finally:
        #self.warning_label.setText("")
        QApplication.restoreOverrideCursor()