from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

import requests, json

def searchCNPJ(cnpj_input: QLineEdit) -> dict:
    cnpj = cnpj_input.text()

    cnpj = ''.join(filter(str.isdigit, cnpj))

    if len(cnpj) != 14:
        print("ERRO")
        return

    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"

    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar o CNPJws: {e}")
        return None
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON.")
        return None
    finally:
        #self.warning_label.setText("")
        QApplication.restoreOverrideCursor()