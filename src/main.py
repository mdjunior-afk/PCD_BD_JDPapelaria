import sys
from PySide6 import QtWidgets

from gui.ui_MainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
