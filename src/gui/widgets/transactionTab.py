from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *
from src.utils import itemExplorer

class TransactionTab(Tab):
    def __init__(self, parent=None, inputs=()):
        super().__init__(parent=parent)

        self.product_total, self.service_total, self.total = inputs
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

        table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])
        table.setObjectName("product")

        price_input.setPrefix("R$ ")
        subtotal_input.setPrefix("R$ ")

        buttons[0].clicked.connect(lambda: self.add(table, search_input, price_input, quantity_input, subtotal_input))
        buttons[1].clicked.connect(lambda: self.edit(table, search_input, price_input, quantity_input, subtotal_input))
        buttons[2].clicked.connect(lambda: self.remove(table))

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
        layout.addWidget(table, 4, 0, 1, 5)

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

        price_input.editingFinished.connect(lambda: subtotal_input.setValue(price_input.value() * quantity_input.value()))
        quantity_input.editingFinished.connect(lambda: subtotal_input.setValue(price_input.value() * quantity_input.value()))

        self.setupSearch(search_input, (price_input, quantity_input, subtotal_input), 
        [
            {"nome": "XEROX", "quantidade": 1, "valor": 0.50},
            {"nome": "CURRICULO", "quantidade": 1, "valor": 10}
        ])

        table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])
        table.setObjectName("service")

        buttons[0].clicked.connect(lambda: self.add(table, search_input, price_input, quantity_input, subtotal_input))
        buttons[1].clicked.connect(lambda: self.edit(table, search_input, price_input, quantity_input, subtotal_input))
        buttons[2].clicked.connect(lambda: self.remove(table))

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
        layout.addWidget(table, 4, 0, 1, 5)

        return widget
    def createPaymentTab(self):
        widget = TabWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        buttons_widget, buttons = createTableButtons()

        document_label = Label(text="Forma de pagamento", type="InputLabel")
        value_label = Label(text="Valor", type="InputLabel")

        document_input = ComboBox()
        document_input.addItems(["Dinheiro", "Cartão de débito", "Cartão de crédito", "PIX"])
        self.payment_value_input = DoubleSpinBox()

        self.payment_value_input.setPrefix("R$ ")
        

        table = Table(["Data", "Forma de pagamento", "Valor"])
        table.setObjectName("payment")

        buttons[0].clicked.connect(lambda: self.addPayment(table, document_input, self.payment_value_input))
        buttons[1].clicked.connect(lambda: self.editPayment(table, document_input, self.payment_value_input))
        buttons[2].clicked.connect(lambda: self.remove(table))

        layout.addWidget(document_label, 0, 0)
        layout.addWidget(value_label, 0, 1)
        
        layout.addWidget(document_input, 1, 0)
        layout.addWidget(self.payment_value_input, 1, 1)
        layout.addWidget(buttons_widget, 1, 2)
        layout.addWidget(table, 2, 0, 1, 3)

        return widget
    
    def addPayment(self, table: Table, document: ComboBox, value):
        if table and value.value() > 0:
            table.setRowCount(table.rowCount() + 1)

            row = table.rowCount() - 1

            table.setItem(row, 0, QTableWidgetItem(str(QDate.currentDate().toString("dd/MM/yyyy"))))
            table.setItem(row, 1, QTableWidgetItem(document.currentText()))
            table.setItem(row, 2, QTableWidgetItem(str(value.value())))

            total = 0
            for row in range(table.rowCount()):
                total += float(table.item(row, 2).text())

            value.setValue(self.total.value() - total)

    def editPayment(self, table: Table, document: ComboBox, value):
        selectedItems = table.selectedItems()

        if table and selectedItems:
            for item in selectedItems:
                if item.row() == 1:
                    document.setCurrentText(item.text())
                elif item.row() == 2:
                    value.setValue(float(item.text()))
        
    def updateTotals(self, table):
        total = 0
        for row in range(table.rowCount()):
            total += float(table.item(row, 4).text())

        if table.objectName() == "product":
            self.product_total.setValue(total)
        elif table.objectName() == "service":
            self.service_total.setValue(total)

        total = self.product_total.value() + self.service_total.value()
        self.total.setValue(total)
        self.payment_value_input.setMaximum(total)
        self.payment_value_input.setValue(total)

    def add(self,table: Table, name : LineEdit, price: QDoubleSpinBox, quantity: SpinBox, subtotal: QDoubleSpinBox):
        if table:
            if name.text() != "" and price.value() > 0 and quantity.value() > 0:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                table.setItem(row, 0, QTableWidgetItem(str(table.rowCount())))
                table.setItem(row, 1, QTableWidgetItem(name.text()))
                table.setItem(row, 2, QTableWidgetItem(str(price.value())))
                table.setItem(row, 3, QTableWidgetItem(str(quantity.value())))
                table.setItem(row, 4, QTableWidgetItem(str(subtotal.value())))

            self.clearFields([name, price, quantity, subtotal])

            self.updateTotals(table)

    def edit(self, table: Table, name : LineEdit, price: QDoubleSpinBox, quantity: SpinBox, subtotal: QDoubleSpinBox):
        selectedItems = table.selectedItems()

        if table and selectedItems:
            row = 0
            for item in selectedItems:

                if item.column() == 1:
                    row = item.row()
                    name.setText(item.text())
                elif item.column() == 2:
                    price.setValue(float(item.text()))
                elif item.column() == 3:
                    quantity.setValue(int(item.text()))
                elif item.column() == 4:
                    subtotal.setValue(float(item.text()))

            table.removeRow(row)
            self.item_explorer.destroy()
            name.setReadOnly(True)

            self.updateTotals(table)

    def remove(self, table: Table):
        selectedItem = table.selectedItems()
        if table and selectedItem:
            # Cria a caixa de mensagem de confirmação
            reply = QMessageBox.question(
                self,
                "Confirmar Remoção",
                "Tem certeza de que deseja remover os produtos selecionados?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            # Verifica a resposta do usuário
            if reply == QMessageBox.Yes:
                table.removeRow(selectedItem[0].row())

            if table.objectName() != "payment":
                self.updateTotals(table)
            else:
                total = 0
                for row in range(table.rowCount()):
                    total += float(table.item(row, 2).text())

                self.payment_value_input.setValue(self.total.value() - total)
                
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