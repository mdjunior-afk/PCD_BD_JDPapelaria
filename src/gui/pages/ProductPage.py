from PySide6.QtWidgets import *

from ..widgets import *

from .Dialogs import *

class ProductPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        page_title = Label("Painel de Produtos", property="Title", fixed=False)
        page_subtitle = Label("Gerencie todos os produtos cadastrados", property="Subtitle", fixed=False)

        search_tab = QTabWidget()
        search_layout = QVBoxLayout()

        inputs_widget = QWidget()
        inputs_layout = QHBoxLayout()

        search_label = Label("Pesquise:", property="NormalBolder", fixed=False)
        category_label = Label("Categoria:", property="NormalBolder", fixed=False)

        search_input = SearchInput(placeholder="")
        category_input = ComboBox(["Todos", "Pen Drives", "Carregadores", "Canetas", "Cadernos"])
        search_button = Button("Pesquisar", property="WithoutBackground")
        export_button = Button("Exportar", icon_path="download.svg")

        inputs_layout.addWidget(search_label)
        inputs_layout.addWidget(search_input)
        inputs_layout.addWidget(category_label)
        inputs_layout.addWidget(category_input)
        inputs_layout.addWidget(search_button)
        inputs_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        inputs_layout.addWidget(export_button)

        inputs_widget.setLayout(inputs_layout)

        table = TableWidget(["ID", "Nome", "Estoque", "Preço", "Categoria"])
        
        search_layout.addWidget(inputs_widget)
        search_layout.addWidget(table)

        search_tab.setLayout(search_layout)

        filter_tab = TabWidget()

        edit_tab = TabWidget()
        edit_tab_layout = QVBoxLayout()

        edit_widget = self.createEditInputs()
        add_buttons_widget = self.createAddButtons()

        edit_tab_layout.addWidget(edit_widget)
        edit_tab_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        edit_tab_layout.addWidget(add_buttons_widget)

        edit_tab.setLayout(edit_tab_layout)

        tab = Tab()
        tab.addTab(search_tab, "Pesquisar produtos")
        tab.addTab(filter_tab, "Pesquisar com filtros")
        tab.addTab(edit_tab, "Adicionar/Editar produto")

        layout.addWidget(page_title)
        layout.addWidget(page_subtitle)
        layout.addWidget(tab)

        self.setLayout(layout)

    def createAddButtons(self):
        widget = QWidget()
        widget.setStyleSheet("background: none;")
        layout = QHBoxLayout()

        add_button = Button("Salvar", icon_path="disk.svg")
        edit_button = Button("Novo", icon_path="plus.svg")
        remove_button = Button("Cancelar", icon_path="cross.svg")

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(remove_button)

        widget.setLayout(layout)

        return widget

    def createEditInputs(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent !important;")

        widget = QWidget()
        widget.setStyleSheet("background: transparent !important;")
        layout = QGridLayout()

        info_box = GroupBox("Informações do produto")
        info_layout = QGridLayout()

        name_label = Label("Nome:")
        brand_label = Label("Marca:")
        category_label = Label("Categoria:")
        barcode_label = Label("Cód.Barra:")

        name_input = SearchInput(placeholder="", max_width=1200)
        brand_input = ComboBox(["MARCA 1", "MARCA 2"])
        category_input = ComboBox(["CATEGORIA 1", "CATEGORIA 2"])
        barcode_input = SearchInput()
        
        info_layout.addWidget(name_label, 0, 0)
        info_layout.addWidget(name_input, 0, 1, 1, 5)
        info_layout.addWidget(brand_label, 1, 0)
        info_layout.addWidget(brand_input, 1, 1)
        info_layout.addWidget(category_label, 1, 2)
        info_layout.addWidget(category_input, 1 ,3)
        info_layout.addWidget(barcode_label, 1, 4)
        info_layout.addWidget(barcode_input, 1, 5)

        info_layout.setColumnStretch(1, 2)
        info_layout.setColumnStretch(3, 2)
        info_layout.setColumnStretch(5, 2)

        info_box.setLayout(info_layout)

        price_box = GroupBox("Informações de preço")
        price_layout = QGridLayout()

        purchase_label = Label("Compra: R$")
        adjust_label = Label("Reajuste(%):")
        sell_label = Label("Venda: R$")

        self.purchase_input = DoubleSpinBox()
        self.adjust_input = DoubleSpinBox()
        self.sell_input = DoubleSpinBox()

        self.purchase_input.editingFinished.connect(self.updateSellPrice)
        self.adjust_input.editingFinished.connect(self.updateSellPrice)
        self.sell_input.editingFinished.connect(self.updateAdjustPrice)

        price_layout.addWidget(purchase_label, 0, 0)
        price_layout.addWidget(self.purchase_input, 0, 1)
        price_layout.addWidget(adjust_label, 0, 2)
        price_layout.addWidget(self.adjust_input, 0, 3)
        price_layout.addWidget(sell_label, 0, 4)
        price_layout.addWidget(self.sell_input, 0, 5)

        price_layout.setColumnStretch(1, 2)
        price_layout.setColumnStretch(3, 2)
        price_layout.setColumnStretch(5, 2)
        
        price_box.setLayout(price_layout)
        
        stock_box = GroupBox("Informações de estoque")
        stock_layout = QGridLayout()

        min_stock_label = Label("Estoque mínimo:")
        stock_label = Label("Estoque atual:")

        min_stock_input = SpinBox()
        stock_input = SpinBox()

        stock_layout.addWidget(min_stock_label, 0, 0)
        stock_layout.addWidget(min_stock_input, 0, 1)
        stock_layout.addWidget(stock_label, 0, 2)
        stock_layout.addWidget(stock_input, 0, 3)

        stock_layout.setColumnStretch(1, 2)
        stock_layout.setColumnStretch(3, 2)

        stock_box.setLayout(stock_layout)

        supplier_box = GroupBox("Informações do fornecedor")
        supplier_layout = QGridLayout()

        search_label = Label("Fornecedor:")
        search_input = SearchInput(placeholder="Pesquise por um fornecedor", max_width=1200)
        table = TableWidget(["Data", "CNPJ", "Razão social", "Data de validade"])
        table.setFixedHeight(150)
        add_button = Button("Adicionar", icon_path="plus.svg")
        remove_button = Button("Remover", icon_path="cross.svg")

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)

        buttons_widget.setLayout(buttons_layout)

        supplier_layout.addWidget(search_label, 0, 0)
        supplier_layout.addWidget(search_input, 0, 1)
        supplier_layout.addWidget(buttons_widget, 1, 1)
        supplier_layout.addWidget(table, 2, 0, 1, 2)

        supplier_box.setLayout(supplier_layout)

        name_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        brand_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        category_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        barcode_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        purchase_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        adjust_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sell_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        min_stock_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        stock_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        search_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(info_box)
        layout.addWidget(price_box)
        layout.addWidget(stock_box)
        layout.addWidget(supplier_box)

        widget.setLayout(layout)

        scroll_area.setWidget(widget)

        return scroll_area

    def updateSellPrice(self):
        purchase = self.purchase_input.value()
        adjust = self.adjust_input.value()

        self.sell_input.setValue(purchase + (purchase * (adjust / 100)))

    def updateAdjustPrice(self):
        sell = self.sell_input.value()
        purchase = self.purchase_input.value()

        self.adjust_input.setValue(((sell/purchase) - 1) * 100)