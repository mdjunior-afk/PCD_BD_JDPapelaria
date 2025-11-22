from PySide6.QtWidgets import *
from PySide6.QtCore import *

from src.gui.colors import *

class ItemExplorer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.targets = None

        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip)
        self.setMinimumWidth(300)

        self.setMinimumHeight(200)
        self.setMaximumHeight(400)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = QListWidget()
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        self.list_widget.setStyleSheet("border: none")

        self.main_layout.addWidget(self.list_widget)

        self.inputs = {}

        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {BTN_TEXT_COLOR};
                background: white;
            }}

            QListWidget::item {{
                padding: 8px;
            }}

            QListWidget::item:hover {{
                background: {BTN_HOVER_BACKGROUND_COLOR};   /* cor do hover */
                color: {BTN_HOVER_TEXT_COLOR};
            }}

            QListWidget::item:selected {{
                background: {BTN_HOVER_BACKGROUND_COLOR};   /* quando clicado */
                color: {BTN_HOVER_TEXT_COLOR};
            }}
        """)

        self.list_widget.itemClicked.connect(self.onItemClicked)

        self.hide()

    def setTarget(self, inputs : dict):
        self.inputs = inputs

    def onItemClicked(self, item):
        data = item.data(Qt.UserRole)

        if data and self.inputs:
            if "nome" in self.inputs:
                self.inputs["nome"].setText(data["nome"])
            if "quantidade" in self.inputs:
                self.inputs["quantidade"].setValue(data["quantidade"])
            if "valor" in self.inputs:
                self.inputs["valor"].setValue(data["valor"])
            if "subtotal" in self.inputs:
                self.inputs["subtotal"].setValue(data["valor"] * data["quantidade"])

        self.inputs["nome"].setReadOnly(True)
        self.hide()

    def showData(self, data):
        self.list_widget.clear()
        self.data = data

        if not data:
            self.list_widget.addItem("Nenhum resultado encontrado!")
            self.show()
            return 
        
        for obj in data:
            item = QListWidgetItem(obj["nome"])
            print(item)
            item.setData(Qt.UserRole, obj)
            self.list_widget.addItem(item)

        item_height = self.list_widget.sizeHintForRow(0) if self.list_widget.count() > 0 else 20
        total_height = item_height * self.list_widget.count() + 10
        self.setFixedHeight(min(total_height, 400))

        self.show()

    def updateTarget(self, parent: QWidget, inputs: dict):
        targets = {
            "nome": inputs["name"],
            "quantidade": inputs["quantity"],
            "valor": inputs["value"],
            "subtotal": inputs["subtotal"]
        }

        self.inputs = targets