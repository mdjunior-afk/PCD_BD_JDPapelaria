from PySide6.QtWidgets import *

from ..widgets import *

from .Dialogs import *

class SellPage(GroupBox):
    def __init__(self, title="Consulta de Vendas"):
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

        intial_date = DateEdit(icon_path="calendar.svg")
        date_label = QLabel(" Até ")
        date_label.setStyleSheet("color: #747474")
        final_date = DateEdit(icon_path="calendar.svg")
        search_btn = PageButton("Procurar", icon_path="search.svg")

        options_widget = self.createOptionsButtons()

        inputs_layout.addWidget(intial_date)
        inputs_layout.addWidget(date_label)
        inputs_layout.addWidget(final_date)
        inputs_layout.addWidget(search_btn)
        inputs_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        inputs_layout.addWidget(options_widget)

        inputs_widget.setLayout(inputs_layout)

        table_widget = TableWidget(["Data", "Cliente", "Total", "Forma de Pagamento"])

        row_count = 1000

        table_widget.setRowCount(row_count)

        for i in range(row_count):
            table_widget.setItem(i, 0, QTableWidgetItem(f"Venda {i}"))
            table_widget.setItem(i, 1, QTableWidgetItem(f"Cliente {i}"))
            table_widget.setItem(i, 2, QTableWidgetItem(f"{i+1}00,00"))
            table_widget.setItem(i, 3, QTableWidgetItem("Dinheiro"))

        layout.addWidget(inputs_widget)
        layout.addWidget(table_widget)
        layout.addWidget(Label(f"{row_count} vendas encontradas!"))

        widget.setLayout(layout)

        widget.setStyleSheet("background-color: transparent !important;")

        return widget

    def addWindow(self):
        self.current_win = TransactionDialog()

        self.current_win.exec()

    def editWindow(self):
        self.current_win = TransactionDialog()

        self.current_win.exec()
        pass

    def removeWindow(self):
        self.current_win = BaseDialog()

        self.current_win.exec()
        pass