from PySide6 import QtWidgets
from src.gui.mainWindow import MainWindow

import sys, os, json

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        
        print("mainwindow")
        try:
            mainwindow = MainWindow()
            print("MainWindow criada com sucesso")
        except Exception as e:
            print(f"ERRO ao criar MainWindow: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        print("main.show")
        mainwindow.show()
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"ERRO CRÍTICO NA APLICAÇÃO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
