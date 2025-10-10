from PySide6.QtWidgets import *

from ..widgets import *

from .Dialogs import *

class PeoplePage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 24)
        self.main_layout.setSpacing(12)

        self.search_widget = QWidget()
        
        self.search_layout = QHBoxLayout(self.search_widget)
        self.search_layout.setContentsMargins(0, 0, 0, 12)

        self.search_input = LineEdit("Procure por uma pessoa...")

        self.search_layout.addWidget(self.search_input)

        self.box_widget = QWidget()
        self.box_widget_layout = QHBoxLayout(self.box_widget)
        self.box_widget_layout.setContentsMargins(0, 0, 0, 6)

        self.add_btn = PageButton("Adicionar", icon_path="plus.svg")
        self.edit_btn = PageButton("Editar", icon_path="edit.svg")
        self.remove_btn = PageButton("Remover", icon_path="cross.svg")
        self.box_widget_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.add_btn.clicked.connect(self.addWindow)
        self.edit_btn.clicked.connect(self.editWindow)
        self.remove_btn.clicked.connect(self.removeWindow)

        self.box_widget_layout.addWidget(self.add_btn)
        self.box_widget_layout.addWidget(self.edit_btn)
        self.box_widget_layout.addWidget(self.remove_btn)
        self.box_widget_layout.addItem(self.box_widget_spacer)

        self.table = TableWidget(["ID", "Nome", "CPF/CNPJ", "Endereço"], "Pessoa")

        self.main_layout.addWidget(self.search_widget)
        self.main_layout.addWidget(self.box_widget)
        self.main_layout.addWidget(self.table)

    def addWindow(self):
        self.current_win = PeopleDialog()

        self.current_win.exec()

    def editWindow(self):
        self.current_win = PeopleDialog()

        self.current_win.exec()
        pass

    def removeWindow(self):
        self.current_win = BaseDialog()

        self.current_win.exec()
        pass

class PeoplePage(GroupBox):
    def __init__(self, title="Consulta de Pessoas"):
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

        search_widget = LineComplement("Pesquise por uma pessoa", items=["Todas", "Pessoa Física", "Pessoa Jurídica"])
        options_widget = self.createOptionsButtons()

        inputs_layout.addWidget(search_widget)
        inputs_layout.addItem(QSpacerItem(120, 20, QSizePolicy.Maximum, QSizePolicy.Minimum))
        inputs_layout.addWidget(options_widget)

        inputs_widget.setLayout(inputs_layout)

        table_widget = TableWidget(["ID", "Nome", "CPF/CNPJ", "Telefone", "Email", "Endereço"])

        row_count = 1000

        table_widget.setRowCount(row_count)

        for i in range(row_count):
            table_widget.setItem(i, 0, QTableWidgetItem(str(i)))
            table_widget.setItem(i, 1, QTableWidgetItem(f"Pessoa {i}"))
            table_widget.setItem(i, 2, QTableWidgetItem("999.999.999-99"))
            table_widget.setItem(i, 3, QTableWidgetItem("(99) 99999-9999"))
            table_widget.setItem(i, 4, QTableWidgetItem(f"user{i}@gmail.com"))
            table_widget.setItem(i, 5, QTableWidgetItem(f"Address {i}"))

        layout.addWidget(inputs_widget)
        layout.addWidget(table_widget)
        layout.addWidget(Label(f"{row_count} pessoas encontradas!"))

        widget.setLayout(layout)

        widget.setStyleSheet("background-color: transparent !important;")

        return widget

    def addWindow(self):
        self.current_win = PeopleDialog()

        self.current_win.exec()

    def editWindow(self):
        self.current_win = PeopleDialog()

        self.current_win.exec()
        pass

    def removeWindow(self):
        self.current_win = BaseDialog()

        self.current_win.exec()
        pass