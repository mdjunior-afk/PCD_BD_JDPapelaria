from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *

class ProductPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Labels
        labels_widget = QWidget()
        labels_layout = QVBoxLayout()
        labels_widget.setLayout(labels_layout)

        title_label = Label(text="Painel de Produtos", type="Title")
        subtitle_label = Label(text="Gerencie todos os produtos cadastrados", type="Subtitle")

        labels_layout.addWidget(title_label)
        labels_layout.addWidget(subtitle_label)

        tab = Tab()
        
        search_tab = self.createSearchTab()
        edition_tab = self.createEditionTab()

        tab.addTab(search_tab, "Pesquisar", )
        tab.addTab(edition_tab, "Adicionar/Editar")

        layout.addWidget(labels_widget)
        layout.addWidget(tab)

    def createSearchTab(self):
        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        search_layout = QGridLayout()

        search_label = Label("Pesquisar", type="InputLabel")
        category_label = Label("Categoria", type="InputLabel")

        search_input = LineEdit("Pesquise por um produto")
        category_input = ComboBox(["Categoria 1", "Car 2", "Categoria 3"])
        search_button = PushButton("Pesquisar", icon_path="search.svg", type="WithoutBackground")
        export_button = PushButton("Exportar", icon_path="download.svg", type="WithBackground")

        data = {
            "search": search_input.text(),
            "category": category_input.currentText()
        }

        search_layout.addWidget(search_label, 0, 0)
        search_layout.addWidget(category_label, 0, 1)

        search_layout.addWidget(search_input, 1, 0)
        search_layout.addWidget(category_input, 1, 1)
        search_layout.addWidget(search_button, 1, 2)

        search_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 3)

        search_layout.addWidget(export_button, 1, 4)

        table = Table(["ID", "Nome", "Estoque", "Preço"])

        search_layout.addWidget(table, 2, 0, 1, 4)
        
        layout.addLayout(search_layout)
        layout.addWidget(table)

        return widget
    
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
        expiration_date_label = Label("Data de validade", type="InputLabel")

        search_input = LineEdit("Pesquise por um fornecedor")
        add_button = PushButton("Adicionar", icon_path="plus.svg", type="WithoutBackground")
        quantity_input = SpinBox()
        expiration_date_input = QDateEdit(date=QDate.currentDate())
        expiration_date_input.setDisplayFormat("dd/MM/yyyy")
        supplier_table = Table(["CNPJ", "Razão social", "Data de validade"])

        supplier_layout.addWidget(search_label, 0, 0)
        supplier_layout.addWidget(quantity_label, 0, 1)
        supplier_layout.addWidget(expiration_date_label, 0, 2)

        supplier_layout.addWidget(search_input, 1, 0)
        supplier_layout.addWidget(quantity_input, 1, 1)
        supplier_layout.addWidget(expiration_date_input, 1, 2)
        supplier_layout.addWidget(add_button, 1, 3)
        supplier_layout.addWidget(supplier_table, 2, 0, 1, 4)

        supplier_layout.setColumnStretch(0, 2)

        layout.addWidget(info_box)
        layout.addWidget(supplier_box)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(buttons_widget)

        buttons[0].clicked.connect(self.addProduct)

        scroll_area.setWidget(widget)

        return scroll_area

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
