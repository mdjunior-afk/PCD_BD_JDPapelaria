from PySide6.QtWidgets import *
from PySide6.QtCore import QDate, Qt

from src.gui.widgets import *
from src.gui.utils import *

from src.controllers import *

from src.utils import itemExplorer

class ProductPage(QWidget):
    def __init__(self):
        super().__init__()

        self.name_input = None
        self.brand_input = None
        self.category_input = None
        self.barcode_input = None
        self.purchase_input = None
        self.adjust_input = None
        self.sale_input = None
        self.minimum_stock_input = None
        self.current_stock_input = None

        self.search_input = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.item_explorer = itemExplorer.ItemExplorer(self)
        self.item_explorer.setFixedSize(self.item_explorer.size())

        # Labels
        labels_widget = QWidget()
        labels_layout = QVBoxLayout()
        labels_widget.setLayout(labels_layout)

        title_label = Label(text="Painel de Produtos", type="Title")
        subtitle_label = Label(text="Gerencie todos os produtos cadastrados", type="Subtitle")

        labels_layout.addWidget(title_label)
        labels_layout.addWidget(subtitle_label)

        self.tab = Tab()
        
        search_tab, self.search_table = self.createSearchTab()
        edition_tab = self.createEditionTab()

        self.search_table.add_action.triggered.connect(lambda: self.tab.setCurrentIndex(1))
        self.search_table.edit_action.triggered.connect(lambda: self.editProduct(self.search_table))
        self.search_table.remove_action.triggered.connect(lambda: self.removeProduct(self.search_table))

        self.tab.addTab(search_tab, "Pesquisar", )
        self.tab.addTab(edition_tab, "Adicionar/Editar")

        layout.addWidget(labels_widget)
        layout.addWidget(self.tab)

    def createSearchTab(self):
        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        search_layout = QGridLayout()

        search_label = Label("Pesquisar", type="InputLabel")
        category_label = Label("Categoria", type="InputLabel")

        self.search_input = LineEdit("Pesquise por um produto")
        category_input = ComboBox(["Categoria 1", "Car 2", "Categoria 3"])
        search_button = PushButton("Pesquisar", icon_path="search.svg", type="WithoutBackground")
        export_button = PushButton("Exportar", icon_path="download.svg", type="WithBackground")

        search_button.clicked.connect(lambda: ProductController.get(self, {"procura": self.search_input.text(), "categoria": category_input.currentText()}), "search")

        search_layout.addWidget(search_label, 0, 0)
        search_layout.addWidget(category_label, 0, 1)

        search_layout.addWidget(self.search_input, 1, 0)
        search_layout.addWidget(category_input, 1, 1)
        search_layout.addWidget(search_button, 1, 2)

        search_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 3)

        search_layout.addWidget(export_button, 1, 4)

        table = Table(["ID", "Nome", "Estoque", "Preço de compra", "Reajuste", "Preço de venda", "Estoque mínimo", "Marca", "Categoria"])

        layout.addLayout(search_layout)
        layout.addWidget(table)

        return widget, (table)
    
    def createEditionTab(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent !important;")

        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        info_box = GroupBox("Informações do produto")
        info_layout = QGridLayout()
        info_box.setLayout(info_layout)

        buttons_widget, buttons = createWindowButtons()

        name_label = Label("Nome", type="InputLabel")
        brand_label = Label("Marca", type="InputLabel")
        category_label = Label("Categoria", type="InputLabel")
        barcode_label = Label("Cód. barra", type="InputLabel")
        purchase_label = Label("Preço de compra", type="InputLabel")
        adjust_label = Label("Reajuste(%)", type="InputLabel")
        sale_label = Label("Preço de venda", type="InputLabel")
        minimum_stock_label = Label("Estoque mínimo", type="InputLabel")
        current_stock_label = Label("Estoque atual", type="InputLabel")

        self.name_input = LineEdit()
        self.brand_input = ComboBox(["Marca 1", "Marca 2", "Marca 3"])
        self.category_input = ComboBox(["Categoria 1", "Car 2", "ASD 3"])
        self.barcode_input = LineEdit()
        self.purchase_input = DoubleSpinBox()
        self.adjust_input = DoubleSpinBox()
        self.sale_input = DoubleSpinBox()
        self.minimum_stock_input = SpinBox()
        self.current_stock_input = SpinBox()

        self.purchase_input.setPrefix("R$ ")
        self.sale_input.setPrefix("R$ ")
        self.adjust_input.setSuffix("%")

        self.adjust_input.editingFinished.connect(self.updateSalePrice)
        self.sale_input.editingFinished.connect(self.updateAdjustValue)

        info_layout.addWidget(name_label, 0, 0)
        info_layout.addWidget(brand_label, 2, 0)
        info_layout.addWidget(category_label, 2, 1)
        info_layout.addWidget(barcode_label, 2, 2)
        info_layout.addWidget(purchase_label, 4, 0)
        info_layout.addWidget(adjust_label, 4, 1)
        info_layout.addWidget(sale_label, 4, 2)
        info_layout.addWidget(minimum_stock_label, 6, 0)
        info_layout.addWidget(current_stock_label, 6, 1)

        info_layout.addWidget(self.name_input, 1, 0, 1, 3)
        info_layout.addWidget(self.brand_input, 3, 0)
        info_layout.addWidget(self.category_input, 3, 1)
        info_layout.addWidget(self.barcode_input, 3, 2)
        info_layout.addWidget(self.purchase_input, 5, 0)
        info_layout.addWidget(self.adjust_input, 5, 1)
        info_layout.addWidget(self.sale_input, 5, 2)
        info_layout.addWidget(self.minimum_stock_input, 7, 0)
        info_layout.addWidget(self.current_stock_input, 7, 1)

        info_layout.setColumnStretch(0, 1)
        info_layout.setColumnStretch(1, 1)
        info_layout.setColumnStretch(2, 1)

        supplier_box = GroupBox("Informações de fornecedor")
        supplier_layout = QGridLayout()
        supplier_box.setLayout(supplier_layout)

        search_label = Label("Pesquisar", type="InputLabel")
        quantity_label = Label("Quantidade", type="InputLabel")
        has_expiration_label = Label("Possui data de validade", type="InputLabel")
        self.expiration_date_label = Label("Data de validade", type="InputLabel")
        self.expiration_date_label.hide()

        search_input = LineEdit("Pesquise por um fornecedor")

        data = [
            {"id": 0, "nome": "LUIZ FELIPE", "cnpj": "999.999.999.99"},
            {"id": 1, "nome": "MARCIO DOUGLAS CASSEMIRO JUNIOR", "cnpj": "150.464.346.10"}
        ]

        self.setupSearch(search_input,data)

        quantity_input = SpinBox()
        self.has_expiration = QCheckBox()
        self.expiration_date_input = DateEdit(date=QDate.currentDate())
        self.expiration_date_input.setDisplayFormat("dd/MM/yyyy")
        self.expiration_date_input.hide()
        supplier_table = Table(["Razão social", "Quantidade", "Data de validade"])

        self.has_expiration.checkStateChanged.connect(self.updateExpirationDate)

        supplier_layout.addWidget(search_label, 0, 0)
        supplier_layout.addWidget(quantity_label, 2, 0)
        supplier_layout.addWidget(has_expiration_label, 2, 2)
        supplier_layout.addWidget(self.expiration_date_label, 2, 1)

        table_buttons_widget, table_buttons = createTableButtons()

        table_buttons[0].clicked.connect(lambda: self.addSupplier(supplier_table, search_input, quantity_input, self.expiration_date_input))
        table_buttons[1].clicked.connect(lambda: self.editSupplier(supplier_table, search_input, quantity_input, self.expiration_date_input))
        table_buttons[2].clicked.connect(lambda: self.removeSupplier(supplier_table))

        supplier_layout.addWidget(search_input, 1, 0, 1, 5)
        supplier_layout.addWidget(quantity_input, 3, 0)
        supplier_layout.addWidget(self.has_expiration, 3, 2)
        supplier_layout.addWidget(self.expiration_date_input, 3, 1)
        supplier_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 3, 3)
        supplier_layout.addWidget(table_buttons_widget, 3, 4)
        supplier_layout.addWidget(supplier_table, 4, 0, 1, 5)

        supplier_layout.setColumnStretch(2, 2)

        layout.addWidget(info_box)
        layout.addWidget(supplier_box)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(buttons_widget)

        buttons[0].clicked.connect(self.addProduct)

        scroll_area.setWidget(widget)

        return scroll_area
    
    def editProduct(self, table: Table):
        selectedItems = table.selectedItems()

        ProductController.get(self, {"id": selectedItems}, "edit")

        self.tab.setCurrentIndex(1)

    def removeProduct(self, table: Table):
        pass
    
    def updateExpirationDate(self, has):
        if has != Qt.CheckState.Checked:
            self.expiration_date_label.hide()
            self.expiration_date_input.hide()
        else:
            self.expiration_date_label.show()
            self.expiration_date_input.show()
    
    def addSupplier(self,table: Table, name : LineEdit, quantity: SpinBox, date: DateEdit):
        if table:
            if name.text() != "" and quantity.value() > 0:
                table.setRowCount(table.rowCount() + 1)

                row = table.rowCount() - 1

                table.setItem(row, 0, QTableWidgetItem(name.text()))
                table.setItem(row, 1, QTableWidgetItem(str(quantity.value())))
                if self.has_expiration.isChecked():
                    table.setItem(row, 2, QTableWidgetItem(str(date.date().toString("dd/MM/yyyy"))))

                self.current_stock_input.setValue(self.current_stock_input.value() + quantity.value())

            self.clearFields([name, quantity, date])

    def editSupplier(self,table: Table, name : LineEdit, quantity: SpinBox, date: DateEdit):
        selectedItems = table.selectedItems()

        if table and selectedItems:
            row = 0
            for item in selectedItems:
                if item.column() == 0:
                    row = item.row()
                    name.setText(item.text())
                elif item.column() == 1:
                    quantity.setValue(float(item.text()))
                    self.current_stock_input.setValue(self.current_stock_input.value() - quantity.value())
                elif item.column() == 2:
                    date.setDate(QDate.fromString(item.text(), "dd/MM/yyyy"))

            table.removeRow(row)
            self.item_explorer.destroy()
            name.setReadOnly(True)

    def removeSupplier(self, table: Table):
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
                self.current_stock_input.setValue(self.current_stock_input.value() - int(table.item(selectedItem[1].row(), selectedItem[1].column()).text()))
                table.removeRow(selectedItem[0].row())

    def setupSearch(self, search_widget : QLineEdit, data: list[dict]):
        # Botão de limpar
        clear_action = search_widget.addAction(QIcon.fromTheme("window-close"), QLineEdit.TrailingPosition)
        clear_action.triggered.connect(lambda: self.clearFields([search_widget]))

        # Conecta textChanged
        search_widget.textChanged.connect(
            lambda text: self.searchItems(data, {"nome": search_widget}, search_widget))

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

    def updateSalePrice(self):
        purchase = self.purchase_input.value()
        adjust = self.adjust_input.value()

        self.sale_input.setValue(purchase + (purchase * (adjust / 100)))

    def updateAdjustValue(self):
        sell = self.sale_input.value()
        purchase = self.purchase_input.value()

        self.adjust_input.setValue(((sell/purchase) - 1) * 100)

    def addProduct(self):
        data = {
            "name": self.name_input.text(),
            "brand": self.brand_input.currentText(),
            "category": self.category_input.currentText(),
            "barcode": self.barcode_input.text(),
            "purchase_price": self.purchase_input.value(),
            "adjust": self.adjust_input.value(),
            "sale_price": self.sale_input.value(),
            "minimum_stock": self.minimum_stock_input.value(),
            "current_stock": self.current_stock_input.value()
        }
