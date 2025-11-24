from PySide6 import QtWidgets
from src.gui.mainWindow import MainWindow

import sys, os, json

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
