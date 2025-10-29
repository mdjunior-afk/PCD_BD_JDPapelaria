from PySide6.QtWidgets import *

from ..config import CONTENT_COLOR
from ..widgets import *

from .Dialogs import *


class ServicePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        page_title = Label("Painel de Serviços", property="Title", fixed=False)
        page_subtitle = Label("Gerencie todos os serviços registrados", property="Subtitle", fixed=False)

        search_tab = QTabWidget()
        search_layout = QVBoxLayout()

        inputs_widget = QWidget()
        inputs_layout = QHBoxLayout()

        search_label = Label("Pesquise:", property="NormalBolder", fixed=False)

        initial_date = DateEdit()
        final_date = DateEdit()

        search_button = Button("Pesquisar", property="WithoutBackground")
        export_button = Button("Exportar", icon_path="download.svg")

        inputs_layout.addWidget(search_label)
        inputs_layout.addWidget(initial_date);
        inputs_layout.addWidget(Label(" até "));
        inputs_layout.addWidget(final_date);
        inputs_layout.addWidget(search_button)
        inputs_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
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
        tab.addTab(search_tab, "Pesquisar vendas")
        tab.addTab(filter_tab, "Pesquisar com filtros")
        tab.addTab(edit_tab, "Adicionar/Editar serviços")

        total_label = Label("Total:")
        total_input = DoubleSpinBox()

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
        layout = QVBoxLayout()

        client_label = Label("Cliente:", fixed=True)

        client_input = SearchInput("Procure por um cliente:", max_width=1200)

        tab = Tab()

        product_tab = self.createProductTab()
        service_tab = self.createServiceTab()
        payment_tab = self.createPaymentTab()

        tab.addTab(product_tab, "Produtos")
        tab.addTab(service_tab, "Serviços")
        tab.addTab(payment_tab, "Pagamentos")

        tab.setCurrentIndex(1)

        total_widget = QWidget()
        total_layout = QHBoxLayout()

        total_label = Label("Total:")
        total_input = DoubleSpinBox()

        total_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        total_layout.addWidget(total_label)
        total_layout.addWidget(total_input)

        total_widget.setLayout(total_layout)

        layout.addWidget(client_label)
        layout.addWidget(client_input)
        layout.addWidget(tab)
        layout.addWidget(total_widget)

        widget.setLayout(layout)

        scroll_area.setWidget(widget)

        return scroll_area

    def createProductTab(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        quantity_label = Label("Quantidade:", fixed=False)
        price_label = Label("Preço:", fixed=False)
        subtotal_label = Label("Subtotal:", fixed=False)

        search_input = SearchInput("Procure por um produto", max_width=1200)
        quantity_input = SpinBox()
        price_input = DoubleSpinBox()
        subtotal_input = DoubleSpinBox()
        subtotal_input.setReadOnly(True)

        table_input = TableWidget(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()

        add_button = Button("Adicionar", icon_path="plus.svg")
        edit_button = Button("Editar", icon_path="edit.svg")
        remove_button = Button("Remover", icon_path="cross.svg")

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(remove_button)

        buttons_widget.setLayout(buttons_layout)

        layout.addWidget(search_input, 0, 0, 1, 8)
        layout.addWidget(quantity_label, 1, 0)
        layout.addWidget(quantity_input, 1, 1)
        layout.addWidget(price_label, 1, 2)
        layout.addWidget(price_input, 1, 3)
        layout.addWidget(subtotal_label, 1, 4)
        layout.addWidget(subtotal_input, 1, 5)
        layout.addWidget(buttons_widget, 1, 7)
        layout.addWidget(table_input, 2, 0, 1, 8)

        return widget

    def createServiceTab(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        quantity_label = Label("Quantidade:", fixed=False)
        price_label = Label("Preço:", fixed=False)
        subtotal_label = Label("Subtotal:", fixed=False)

        search_input = SearchInput("Procure por um serviço", max_width=1200)
        quantity_input = SpinBox()
        price_input = DoubleSpinBox()
        subtotal_input = DoubleSpinBox()
        subtotal_input.setReadOnly(True)

        table_input = TableWidget(["ID", "Nome", "Preço", "Quantidade", "Subtotal"])

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()

        add_button = Button("Adicionar", icon_path="plus.svg")
        edit_button = Button("Editar", icon_path="edit.svg")
        remove_button = Button("Remover", icon_path="cross.svg")

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(remove_button)

        buttons_widget.setLayout(buttons_layout)

        layout.addWidget(search_input, 0, 0, 1, 8)
        layout.addWidget(quantity_label, 1, 0)
        layout.addWidget(quantity_input, 1, 1)
        layout.addWidget(price_label, 1, 2)
        layout.addWidget(price_input, 1, 3)
        layout.addWidget(subtotal_label, 1, 4)
        layout.addWidget(subtotal_input, 1, 5)
        layout.addWidget(buttons_widget, 1, 7)
        layout.addWidget(table_input, 2, 0, 1, 8)

        return widget

    def createPaymentTab(self):
        widget = QWidget()
        layout = QGridLayout()

        payment_label = Label("Forma de pagamento:", fixed=False)
        value_label = Label("Valor:", fixed=False)

        payment_input = ComboBox(["Cartão de Crédito", "Cartão de Débito", "Pix", "Dinheiro"])
        value_input = DoubleSpinBox()

        add_btn = Button("Adicionar", icon_path="plus.svg")
        edit_btn = Button("Editar", icon_path="edit.svg")
        remove_btn = Button("Remover", icon_path="cross.svg")

        table_input = TableWidget(["ID", "Data", "Documento", "Valor"])

        layout.addWidget(payment_label, 0, 0)
        layout.addWidget(payment_input, 0, 1)
        layout.addWidget(value_label, 0, 2)
        layout.addWidget(value_input, 0, 3)
        layout.addWidget(add_btn, 0, 5)
        layout.addWidget(edit_btn, 0, 6)
        layout.addWidget(remove_btn, 0, 7)
        layout.addWidget(table_input, 1, 0, 1, 8)

        widget.setLayout(layout)

        return widget