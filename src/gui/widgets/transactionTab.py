from PySide6.QtWidgets import *

from src.gui.widgets import *
from src.gui.utils import *
from src.utils import itemExplorer

class TransactionTab(Tab):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.product_table: Table = None
        self.services_table: Table = None

        self.item_explorer = itemExplorer.ItemExplorer(parent=self)

        self.setStyleSheet(f"QTabWidget::pane{{ background: #F9F9F9 !important }}")

        product_tab, services_tab, payment_tab = self.createProductsTab(), self.createServicesTab(), self.createPaymentTab()

        self.addTab(product_tab, "Produtos")
        self.addTab(services_tab, "Serviços")
        self.addTab(payment_tab, "Pagamentos")

    def createProductsTab(self):
        widget = TabWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        buttons_widget, buttons = createTableButtons()

        search_label = Label("Pesquisa", type="InputLabel")
        price_label = Label("Preço", type="InputLabel")
        quantity_label = Label("Quantidade", type="InputLabel")
        subtotal_label = Label("Subtotal", type="InputLabel")

        search_input = LineEdit("Pesquise por um produto")
        price_input = DoubleSpinBox()
        quantity_input = SpinBox()
        subtotal_input = DoubleSpinBox()

        price_input.editingFinished.connect(lambda: subtotal_input.setValue(price_input.value() * quantity_input.value()))
        quantity_input.editingFinished.connect(lambda: subtotal_input.setValue(price_input.value() * quantity_input.value()))

        self.setupSearch(search_input, (price_input, quantity_input, subtotal_input), 
        [
            {"nome": "PENDRIVE SAMSUNG 8G", "quantidade": 1, "valor": 39.90},
            {"nome": "PENDRIVE SANDISK 16GB", "quantidade": 1, "valor": 59.90}
        ])

        self.products_table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])

        price_input.setPrefix("R$ ")
        subtotal_input.setPrefix("R$ ")

        buttons[0].clicked.connect(lambda: self.addProduct(search_input, price_input, quantity_input, subtotal_input))
        buttons[1].clicked.connect(self.editProduct)
        buttons[2].clicked.connect(self.removeProduct)

        layout.addWidget(search_label, 0, 0)
        layout.addWidget(price_label, 2, 0)
        layout.addWidget(quantity_label, 2, 1)
        layout.addWidget(subtotal_label, 2, 2)

        layout.addWidget(search_input, 1, 0, 1, 5)
        layout.addWidget(price_input, 3, 0)
        layout.addWidget(quantity_input, 3, 1)
        layout.addWidget(subtotal_input, 3, 2)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 3, 3)
        layout.addWidget(buttons_widget, 3, 4)
        layout.addWidget(self.products_table, 4, 0, 1, 5)

        return widget
    
    def createServicesTab(self):
        widget = TabWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        
        buttons_widget, buttons = createTableButtons()

        search_label = Label("Pesquisa", type="InputLabel")
        price_label = Label("Preço", type="InputLabel")
        quantity_label = Label("Quantidade", type="InputLabel")
        subtotal_label = Label("Subtotal", type="InputLabel")

        search_input = LineEdit("Pesquise por um serviço")
        price_input = DoubleSpinBox()
        quantity_input = SpinBox()
        subtotal_input = DoubleSpinBox()

        self.services_table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])

        price_input.setPrefix("R$ ")
        subtotal_input.setPrefix("R$ ")

        layout.addWidget(search_label, 0, 0)
        layout.addWidget(price_label, 2, 0)
        layout.addWidget(quantity_label, 2, 1)
        layout.addWidget(subtotal_label, 2, 2)

        layout.addWidget(search_input, 1, 0, 1, 5)
        layout.addWidget(price_input, 3, 0)
        layout.addWidget(quantity_input, 3, 1)
        layout.addWidget(subtotal_input, 3, 2)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 3, 3)
        layout.addWidget(buttons_widget, 3, 4)
        layout.addWidget(self.services_table, 4, 0, 1, 5)

        return widget
    def createPaymentTab(self):
        widget = TabWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        buttons_widget, buttons = createTableButtons()

        document_label = Label(text="Forma de pagamento", type="InputLabel")
        value_label = Label(text="Valor", type="InputLabel")

        document_input = ComboBox(["Dinheiro", "Cartão de débito", "Cartão de crédito", "PIX"])
        value_input = DoubleSpinBox()

        value_input.setPrefix("R$ ")

        table = Table(["Data", "Forma de pagamento", "Valor"])

        layout.addWidget(document_label, 0, 0)
        layout.addWidget(value_label, 0, 1)
        
        layout.addWidget(document_input, 1, 0)
        layout.addWidget(value_input, 1, 1)
        layout.addWidget(buttons_widget, 1, 2)
        layout.addWidget(table, 2, 0, 1, 3)

        return widget

    def addProduct(self, name : LineEdit, price: QDoubleSpinBox, quantity: SpinBox, subtotal: QDoubleSpinBox):
        if self.product_table:
            if name.text() != "" and price.value() > 0 and quantity.value() > 0:
                self.product_table.setRowCount(self.product_table.rowCount() + 1)

                self.product_table.setItem(self.product_table.rowCount() - 1, 0, QTableWidgetItem(str(self.product_table.rowCount())))
                self.product_table.setItem(self.product_table.rowCount() - 1, 1, QTableWidgetItem(name.text()))
                self.product_table.setItem(self.product_table.rowCount() - 1, 2, QTableWidgetItem(str(price.value())))
                self.product_table.setItem(self.product_table.rowCount() - 1, 3, QTableWidgetItem(str(quantity.value())))
                self.product_table.setItem(self.product_table.rowCount() - 1, 4, QTableWidgetItem(str(subtotal.value())))

                self.total_input.setValue(self.updateTotal())

    def updateTotal(self):
        total = 0

        for i in range(self.product_table.rowCount()):
            total += int(self.product_table.item(i, 2))

        for i in range(self.services_table.rowCount()):
            total += int(self.services_table.item(i, 2))

        return total

    def editProduct(self):
        pass

    def removeProduct(self):
        pass

    def setupSearch(self, search_widget : QLineEdit, inputs: tuple, data: list[dict]):
        # Botão de limpar
        clear_action = search_widget.addAction(QIcon.fromTheme("window-close"), QLineEdit.TrailingPosition)
        clear_action.triggered.connect(lambda: self.clearFields([search_widget, *inputs]))

        # Conecta textChanged
        search_widget.textChanged.connect(
            lambda text: self.searchItems(data,
                                            {"nome": search_widget,
                                            "valor": inputs[0],
                                            "quantidade": inputs[1],
                                            "subtotal": inputs[2]},
                                            search_widget))


    def searchItems(self, data: list, targets: dict, search_widget: QLineEdit):
            if not search_widget.text():
                self.item_explorer.hide()
                return
            self.item_explorer.setTarget(targets)
            self.item_explorer.showData(data)

            # Posiciona o dropdown
            pos_global = search_widget.mapToGlobal(QPoint(0, 0))
            final_pos_global = QPoint(pos_global.x(), pos_global.y() + search_widget.height())
            
            self.item_explorer.move(final_pos_global)
            self.item_explorer.setFixedWidth(search_widget.width())


    def clearFields(self: QWidget, fields: list):
        for f in fields:
            if isinstance(f, QLineEdit):
                if f.isReadOnly():
                    f.setReadOnly(False)
                    f.clear()
            elif isinstance(f, (QSpinBox, QDoubleSpinBox)):
                f.setValue(0)

        self.item_explorer.hide()