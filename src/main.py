from PySide6 import QtWidgets
from gui.mainWindow import MainWindow

import sys, os, json

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    qss_path = os.path.join(os.path.dirname(__file__), "gui", "styles.qss")
    with open("configuration.json", "r") as f:
        config = json.load(f)
    
    with open(qss_path, "r") as f:
        _style = f.read()
        _style = _style.format(
            SIDE_MENU_LABEL_SIZE=config["SIDE_MENU_LABEL_SIZE"],
            NORMAL_LABEL_SIZE=config["NORMAL_LABEL_SIZE"],
            INPUT_LABEL_SIZE=config["INPUT_LABEL_SIZE"],
            TITLE_LABEL_SIZE=config["TITLE_LABEL_SIZE"],
            SUBTITLE_LABEL_SIZE=config["SUBTITLE_LABEL_SIZE"]
        )

        app.setStyleSheet(_style)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
