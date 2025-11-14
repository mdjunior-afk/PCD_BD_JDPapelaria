from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *

from src.gui.colors import *

class SalesPage(QWidget):
    def __init__(self):
        super().__init__()

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