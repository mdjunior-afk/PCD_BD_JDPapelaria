from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *

class ServicePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Labels
        labels_widget = QWidget()
        labels_layout = QVBoxLayout()
        labels_widget.setLayout(labels_layout)

        title_label = Label(text="Painel de Serviços", type="Title")
        subtitle_label = Label(text="Gerencie todos os serviços cadastrados", type="Subtitle")

        labels_layout.addWidget(title_label)
        labels_layout.addWidget(subtitle_label)

        tab = Tab()
        
        search_tab = self.createSearchTab()
        edition_tab = self.createEditionTab()
        edition_tab

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

        initial_date = DateEdit(date=QDate.currentDate())
        final_date = DateEdit(date=QDate.currentDate())
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
        widget = TabWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        client_box = GroupBox("Informações do cliente")
        client_layout = QVBoxLayout()
        client_box.setLayout(client_layout)

        total_box = QWidget()
        total_box_layout = QHBoxLayout()
        total_box.setLayout(total_box_layout)

        products_total_label = Label("Produtos:", type="InputLabel")
        services_total_label = Label("Serviços:", type="InputLabel")
        total_label = Label("Total:", type="InputLabel")
        
        products_total_input = DoubleSpinBox()
        services_total_input = DoubleSpinBox()        
        total_input = DoubleSpinBox()

        total_input.setPrefix("R$ ")
        products_total_input.setPrefix("R$ ")
        services_total_input.setPrefix("R$ ")
        
        total_input.setReadOnly(True)
        products_total_input.setReadOnly(True)
        services_total_input.setReadOnly(True)

        total_box_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        total_box_layout.addWidget(products_total_label)
        total_box_layout.addWidget(products_total_input)
        total_box_layout.addWidget(services_total_label)
        total_box_layout.addWidget(services_total_input)
        total_box_layout.addWidget(total_label)
        total_box_layout.addWidget(total_input)

        buttons_widget, buttons = createWindowButtons()

        search_client_label = Label(text="Cliente", type="InputLabel")
        
        search_client_input = LineEdit("Pesquise por um cliente")

        client_layout.addWidget(search_client_label)
        client_layout.addWidget(search_client_input)

        tab = TransactionTab(parent=self, inputs=(products_total_input, services_total_input, total_input))

        tab.setCurrentIndex(1)

        layout.addWidget(client_box)
        layout.addWidget(tab)
        layout.addWidget(total_box)
        layout.addWidget(buttons_widget)

        return widget
