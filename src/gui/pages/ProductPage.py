from PySide6.QtWidgets import *

from ..widgets import *

from .Dialogs import *

class ProductPage(GroupBox):
    def __init__(self, title="Consulta de Produtos"):
        super().__init__(title)

        layout = QVBoxLayout()

        inputs = self.createInputs()

        layout.addWidget(inputs)

        self.setLayout(layout)

    def createOptionsButtons(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 6, 6)

        add_button = PageButton("Adicionar", icon_path="plus.svg")
        edit_button = PageButton("Editar", icon_path="edit.svg")
        remove_button = PageButton("Remover", icon_path="cross.svg")

        add_button.clicked.connect(self.addWindow)
        edit_button.clicked.connect(self.editWindow)
        remove_button.clicked.connect(self.removeWindow)

        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(remove_button)

        widget.setLayout(layout)

        return widget

    def createInputs(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 6, 0)

        inputs_widget = QWidget()
        inputs_layout = QHBoxLayout()
        inputs_layout.setContentsMargins(0, 0, 0, 0)

        search_widget = LineComplement("Pesquise por um produto", items=["Todos", "Pen-Drives", "Carregadores", "Canetas", "Cadernos"])
        options_widget = self.createOptionsButtons()

        inputs_layout.addWidget(search_widget)
        inputs_layout.addItem(QSpacerItem(120, 20, QSizePolicy.Maximum, QSizePolicy.Minimum))
        inputs_layout.addWidget(options_widget)

        inputs_widget.setLayout(inputs_layout)

        table_widget = TableWidget(["ID", "Nome", "Estoque", "Preço", "Categoria"])

        row_count = 1000

        table_widget.setRowCount(row_count)

        for i in range(row_count):
            table_widget.setItem(i, 0, QTableWidgetItem(str(i)))
            table_widget.setItem(i, 1, QTableWidgetItem("Produto" + str(i)))
            table_widget.setItem(i, 2, QTableWidgetItem("0"))
            table_widget.setItem(i, 3, QTableWidgetItem("100,00"))
            table_widget.setItem(i, 4, QTableWidgetItem("Categoria" + str(i)))

        layout.addWidget(inputs_widget)
        layout.addWidget(table_widget)
        layout.addWidget(Label(f"{row_count} produtos encontrados!"))

        widget.setLayout(layout)

        widget.setStyleSheet("background-color: transparent !important;")

        return widget

    def addWindow(self):
        self.current_win = ProductDialog()

        self.current_win.exec()

    def editWindow(self):
        self.current_win = ProductDialog()

        self.current_win.exec()
        pass

    def removeWindow(self):
        self.current_win = BaseDialog()

        self.current_win.exec()
        pass