from PySide6 import QtWidgets
from gui.MainWindow import MainWindow
from gui.config import *

import sys, os

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyleSheet("Fusion")

    qss_path = os.path.join(os.path.dirname(__file__), "gui", "style.qss")
    with open(qss_path, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
