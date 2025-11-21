from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *
from src.gui.colors import *

from src.utils.itemExplorer import *

class SalesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.item_explorer = ItemExplorer(self)
        self.item_explorer.setFixedSize(self.item_explorer.size())

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Labels
        labels_widget = QWidget()
        labels_layout = QVBoxLayout()
        labels_widget.setLayout(labels_layout)

        title_label = Label(text="Painel de Vendas", type="Title")
        subtitle_label = Label(text="Gerencie todas as vendas cadastradas", type="Subtitle")

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

        initial_date_label = Label("Período incial", type="InputLabel")
        final_date_label = Label("Período final", type="InputLabel")

        initial_date = QDateEdit(date=QDate.currentDate())
        final_date = QDateEdit(date=QDate.currentDate())
        search_button = PushButton("Pesquisar", icon_path="search.svg", type="WithoutBackground")
        export_button = PushButton("Exportar", icon_path="download.svg", type="WithBackground")

        initial_date.setDisplayFormat("dd/MM/yyyy")
        final_date.setDisplayFormat("dd/MM/yyyy")

        search_layout.addWidget(initial_date_label, 0, 0)
        search_layout.addWidget(Label("Até"), 1, 1)
        search_layout.addWidget(final_date_label, 0, 2)

        search_layout.addWidget(initial_date, 1, 0)
        search_layout.addWidget(final_date, 1, 2)
        search_layout.addWidget(search_button, 1, 3)

        search_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 4)

        search_layout.addWidget(export_button, 1, 5)

        table = Table(["ID", "Nome", "Estoque", "Preço"])

        search_layout.addWidget(table, 2, 0, 1, 6)
        
        layout.addLayout(search_layout)
        layout.addWidget(table)

        return widget
    
    def createEditionTab(self):
        def createProductsTab():
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

            self.setupSearch(search_input, (price_input, quantity_input, subtotal_input), 
            [
                {"nome": "PENDRIVE SAMSUNG 8G", "quantidade": 1, "valor": 39.90},
                {"nome": "PENDRIVE SANDISK 16GB", "quantidade": 1, "valor": 59.90}
            ])

            table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])

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
        def createServicesTab():
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

            table = Table(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])

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
        def createPaymentTab():
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

        widget = TabWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        client_box = GroupBox("Informações do cliente")
        client_layout = QVBoxLayout()
        client_box.setLayout(client_layout)

        search_client_label = Label(text="Cliente", type="InputLabel")
        
        search_client_input = LineEdit("Pesquise por um cliente")

        client_layout.addWidget(search_client_label)
        client_layout.addWidget(search_client_input)

        tab = Tab()
        tab.setStyleSheet(f"QTabWidget::pane{{ background: #F9F9F9 !important }}")

        product_tab, services_tab, payment_tab = createProductsTab(), createServicesTab(), createPaymentTab()

        tab.addTab(product_tab, "Produtos")
        tab.addTab(services_tab, "Serviços")
        tab.addTab(payment_tab, "Pagamentos")

        layout.addWidget(client_box)
        layout.addWidget(tab)

        return widget
    
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