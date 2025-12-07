from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *
from src.utils import itemExplorer

from src.controllers.productController import ProductController
from src.controllers.serviceController import ServiceController

class TransactionTab(Tab):
    def __init__(self, parent=None, total=None, type="product"):
        super().__init__(parent=parent)

        self.type = type

        self.setStyleSheet(f"QTabWidget::pane{{ background: #F9F9F9 !important }}")

        self.total = total

        if self.type == "product":
            self.item_explorer = itemExplorer.ItemExplorer(parent=self)

            product_tab = self.createProductsTab()
            self.addTab(product_tab, "Produtos")

        elif self.type == "service":
            self.item_explorer = itemExplorer.ItemExplorer(parent=self)

            services_tab = self.createServicesTab()
            self.addTab(services_tab, "Serviços")

        payment_tab = self.createPaymentTab()
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

        self.product_search_input = LineEdit("Pesquise por um produto")
        self.product_price_input = DoubleSpinBox()
        self.product_quantity_input = SpinBox()
        self.product_subtotal_input = DoubleSpinBox()

        self.product_price_input.editingFinished.connect(lambda: self.product_subtotal_input.setValue(self.product_price_input.value() * self.product_quantity_input.value()))
        self.product_quantity_input.editingFinished.connect(lambda: self.product_subtotal_input.setValue(self.product_price_input.value() * self.product_quantity_input.value()))

        self.setupSearch(self.product_search_input, (self.product_price_input, self.product_quantity_input, self.product_subtotal_input))

        self.products_table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])
        self.products_table.setObjectName("product")

        self.product_price_input.setPrefix("R$ ")
        self.product_subtotal_input.setPrefix("R$ ")

        buttons[0].clicked.connect(lambda: self.add(self.products_table, self.product_search_input, self.product_price_input, self.product_quantity_input, self.product_subtotal_input))
        buttons[1].clicked.connect(lambda: self.edit(self.products_table, self.product_search_input, self.product_price_input, self.product_quantity_input, self.product_subtotal_input))
        buttons[2].clicked.connect(lambda: self.remove(self.products_table))

        layout.addWidget(search_label, 0, 0)
        layout.addWidget(price_label, 2, 0)
        layout.addWidget(quantity_label, 2, 1)
        layout.addWidget(subtotal_label, 2, 2)

        layout.addWidget(self.product_search_input, 1, 0, 1, 5)
        layout.addWidget(self.product_price_input, 3, 0)
        layout.addWidget(self.product_quantity_input, 3, 1)
        layout.addWidget(self.product_subtotal_input, 3, 2)
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

        self.service_search_input = LineEdit("Pesquise por um serviço")
        self.service_price_input = DoubleSpinBox()
        self.service_quantity_input = SpinBox()
        self.service_subtotal_input = DoubleSpinBox()

        self.service_price_input.editingFinished.connect(lambda: self.service_subtotal_input.setValue(self.service_price_input.value() * self.service_quantity_input.value()))
        self.service_quantity_input.editingFinished.connect(lambda: self.service_subtotal_input.setValue(self.service_price_input.value() * self.service_quantity_input.value()))

        self.setupSearch(self.service_search_input, (self.service_price_input, self.service_quantity_input, self.service_subtotal_input), "service")

        self.services_table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])
        self.services_table.setObjectName("service")

        buttons[0].clicked.connect(lambda: self.add(self.services_table, self.service_search_input, self.service_price_input, self.service_quantity_input, self.service_subtotal_input))
        buttons[1].clicked.connect(lambda: self.edit(self.services_table, self.service_search_input, self.service_price_input, self.service_quantity_input, self.service_subtotal_input))
        buttons[2].clicked.connect(lambda: self.remove(self.services_table))

        self.service_price_input.setPrefix("R$ ")
        self.service_subtotal_input.setPrefix("R$ ")

        layout.addWidget(search_label, 0, 0)
        layout.addWidget(price_label, 2, 0)
        layout.addWidget(quantity_label, 2, 1)
        layout.addWidget(subtotal_label, 2, 2)

        layout.addWidget(self.service_search_input, 1, 0, 1, 5)
        layout.addWidget(self.service_price_input, 3, 0)
        layout.addWidget(self.service_quantity_input, 3, 1)
        layout.addWidget(self.service_subtotal_input, 3, 2)
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

        self.document_input = ComboBox()
        self.payment_value_input = DoubleSpinBox()

        self.payment_value_input.setPrefix("R$ ")

        self.payments_table = Table(["Data", "Forma de pagamento", "Valor"])
        self.payments_table.setObjectName("payment")

        buttons[0].clicked.connect(lambda: self.addPayment(self.payments_table, self.document_input, self.payment_value_input))
        buttons[1].clicked.connect(lambda: self.editPayment(self.payments_table, self.document_input, self.payment_value_input))
        buttons[2].clicked.connect(lambda: self.remove(self.payments_table))

        layout.addWidget(document_label, 0, 0)
        layout.addWidget(value_label, 0, 1)
        
        layout.addWidget(self.document_input, 1, 0)
        layout.addWidget(self.payment_value_input, 1, 1)
        layout.addWidget(buttons_widget, 1, 2)
        layout.addWidget(self.payments_table, 2, 0, 1, 3)

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

    def updateProductTable(self, name, price, quantity, subtotal):
        row = self.products_table.rowCount()
        self.products_table.setRowCount(self.products_table.rowCount() + 1)

        self.products_table.setItem(row, 0, QTableWidgetItem(str(self.products_table.rowCount())))
        self.products_table.setItem(row, 1, QTableWidgetItem(name))
        self.products_table.setItem(row, 2, QTableWidgetItem(str(price)))
        self.products_table.setItem(row, 3, QTableWidgetItem(str(quantity)))
        self.products_table.setItem(row, 4, QTableWidgetItem(str(subtotal)))
    
    def updateServiceTable(self, name, price, quantity, subtotal):
        row = self.services_table.rowCount()
        self.services_table.setRowCount(self.services_table.rowCount() + 1)

        self.services_table.setItem(row, 0, QTableWidgetItem(str(self.services_table.rowCount())))
        self.services_table.setItem(row, 1, QTableWidgetItem(name))
        self.services_table.setItem(row, 2, QTableWidgetItem(str(price)))
        self.services_table.setItem(row, 3, QTableWidgetItem(str(quantity)))
        self.services_table.setItem(row, 4, QTableWidgetItem(str(subtotal)))

    def updatePaymentTable(self, value, method):
        row = self.payments_table.rowCount()
        self.payments_table.setRowCount(self.payments_table.rowCount() + 1)

        self.payments_table.setItem(row, 0, QTableWidgetItem(str(self.payments_table.rowCount())))
        self.payments_table.setItem(row, 1, QTableWidgetItem(method))
        self.payments_table.setItem(row, 2, QTableWidgetItem(str(value)))
                
    def setupSearch(self, search_widget : QLineEdit, inputs: tuple, type="product"):
        # Botão de limpar
        clear_action = search_widget.addAction(QIcon.fromTheme("window-close"), QLineEdit.TrailingPosition)
        clear_action.triggered.connect(lambda: self.clearFields([search_widget, *inputs]))

        # Conecta textChanged
        search_widget.textChanged.connect(
            lambda text: self.searchItems(ProductController.get(self, {"pesquisa": text}, "search_item") if type == "product" else ServiceController.get(self, {"pesquisa": text}, "search_item"),
                                            {"nome": search_widget,
                                            "valor": inputs[0],
                                            "quantidade": inputs[1],
                                            "subtotal": inputs[2]},
                                            search_widget))


    def searchItems(self, data, targets: dict, search_widget: QLineEdit):
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

    def getAllProducts(self) -> list:
        """Retorna uma lista de dicionários com todos os produtos na tabela."""
        if not hasattr(self, 'products_table'):
            return []
            
        table = self.products_table
        
        # Mapeamento das colunas da tabela para as chaves do dicionário de saída
        column_map = ["ID", "nome", "preco", "quantidade", "subtotal"]
        
        products = []
        for row in range(table.rowCount()):
            product_data = {}
            for col, key in enumerate(column_map):
                item = table.item(row, col)
                # Tenta converter valores numéricos para float/int se necessário
                text = item.text() if item is not None else ""
                
                if key in ["preco", "subtotal"]:
                    # Remove "R$ " e tenta converter para float
                    text = text.replace("R$ ", "").replace(",", ".") # Ajuste para o formato float
                    try:
                        product_data[key] = float(text)
                    except ValueError:
                        product_data[key] = 0.0
                elif key == "quantidade":
                    try:
                        product_data[key] = int(text)
                    except ValueError:
                        product_data[key] = 0
                else:
                    product_data[key] = text
            
            # Remove o ID temporário se você não quiser enviá-lo para o DB
            # product_data.pop("ID", None) 
            products.append(product_data)
            
        return products

    def getAllServices(self) -> list:
        """Retorna uma lista de dicionários com todos os serviços na tabela."""
        if not hasattr(self, 'services_table'):
            return []
            
        table = self.services_table
        
        # Mapeamento das colunas da tabela para as chaves do dicionário de saída
        column_map = ["ID", "nome", "preco", "quantidade", "subtotal"]
        
        services = []
        for row in range(table.rowCount()):
            service_data = {}
            for col, key in enumerate(column_map):
                item = table.item(row, col)
                text = item.text() if item is not None else ""
                
                if key in ["preco", "subtotal"]:
                    text = text.replace("R$ ", "").replace(",", ".")
                    try:
                        service_data[key] = float(text)
                    except ValueError:
                        service_data[key] = 0.0
                elif key == "quantidade":
                    try:
                        service_data[key] = int(text)
                    except ValueError:
                        service_data[key] = 0
                else:
                    service_data[key] = text
            
            # service_data.pop("ID", None) 
            services.append(service_data)
            
        return services

    def getAllPayments(self) -> list:
        """Retorna uma lista de dicionários com todos os pagamentos na tabela."""
        if not hasattr(self, 'payments_table'):
            return []
            
        table = self.payments_table
        
        # Mapeamento das colunas da tabela para as chaves do dicionário de saída
        column_map = ["data", "forma_pagamento", "valor"]
        
        payments = []
        for row in range(table.rowCount()):
            payment_data = {}
            for col, key in enumerate(column_map):
                item = table.item(row, col)
                text = item.text() if item is not None else ""
                
                if key == "valor":
                    # O valor na tabela é inserido como string de float sem prefixo, 
                    # então a conversão direta é mais simples.
                    try:
                        payment_data[key] = float(text)
                    except ValueError:
                        payment_data[key] = 0.0
                else:
                    payment_data[key] = text
            
            payments.append(payment_data)
            
        return payments

    def resetInputs(self):
        if self.type == "product":
            self.product_search_input.clear()
            self.product_price_input.setValue(0)
            self.product_quantity_input.setValue(0)
            self.product_subtotal_input.setValue(0)
            self.products_table.setRowCount(0)

        if self.type == "service":
            self.service_search_input.clear()
            self.service_price_input.setValue(0)
            self.service_quantity_input.setValue(0)
            self.service_subtotal_input.setValue(0)
            self.services_table.setRowCount(0)

        self.document_input.setCurrentIndex(0)
        self.payment_value_input.setValue(0)
        self.payments_table.setRowCount(0)