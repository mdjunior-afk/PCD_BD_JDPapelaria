from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

from src.gui.widgets import *
from src.gui.utils import *
from src.gui.colors import *

from src.controllers.salesController import SalesController
from src.controllers.personController import PersonController

from src.gui.widgets.removeWindow import MessageDialog
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

        self.tab = Tab()
        
        search_tab, self.search_table = self.createSearchTab()
        edition_tab = self.createEditionTab()

        self.search_table.add_action.triggered.connect(lambda: self.tab.setCurrentIndex(1))
        self.search_table.edit_action.triggered.connect(lambda: self.editSale(self.search_table))
        self.search_table.remove_action.triggered.connect(lambda: self.removeSale(self.search_table))

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

        initial_date_label = Label("Período incial", type="InputLabel")
        final_date_label = Label("Período final", type="InputLabel")

        self.initial_date = DateEdit(date=QDate.currentDate())
        self.final_date = DateEdit(date=QDate.currentDate())
        search_button = PushButton("Pesquisar", icon_path="search.svg", type="WithoutBackground")
        export_button = PushButton("Exportar", icon_path="download.svg", type="WithBackground")

        search_button.clicked.connect(lambda: SalesController.get(self, {"data_inicio": self.initial_date.text(), "data_final": self.final_date.text()}, "search"))

        self.initial_date.setDisplayFormat("dd/MM/yyyy")
        self.final_date.setDisplayFormat("dd/MM/yyyy")

        search_layout.addWidget(initial_date_label, 0, 0)
        search_layout.addWidget(Label("Até"), 1, 1)
        search_layout.addWidget(final_date_label, 0, 2)

        search_layout.addWidget(self.initial_date, 1, 0)
        search_layout.addWidget(self.final_date, 1, 2)
        search_layout.addWidget(search_button, 1, 3)

        search_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 4)

        search_layout.addWidget(export_button, 1, 5)

        table = Table(["ID", "Data", "Cliente", "Valor total", "Forma de pagamento"])

        search_layout.addWidget(table, 2, 0, 1, 6)
        
        layout.addLayout(search_layout)
        layout.addWidget(table)

        return widget, table
    
    def createEditionTab(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent !important;")
    
        widget = TabWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.id_input = SpinBox()
        self.id_input.setValue(0)
        self.id_input.hide()

        client_box = GroupBox("Informações do cliente")
        client_layout = QVBoxLayout()
        client_box.setLayout(client_layout)

        search_client_label = Label(text="Cliente", type="InputLabel")
        
        self.search_client_input = LineEdit("Pesquise por um cliente")

        self.setupSearch(self.search_client_input, PersonController.get(self, {"pesquisa": self.search_client_input.text()}, "search_item"))

        client_layout.addWidget(search_client_label)
        client_layout.addWidget(self.search_client_input)

        total_box = QWidget()
        total_box_layout = QHBoxLayout()
        total_box.setLayout(total_box_layout)

        products_total_label = Label("Produtos:", type="InputLabel")
        total_label = Label("Total:", type="InputLabel")
        
        self.total_input = DoubleSpinBox()

        self.total_input.setPrefix("R$ ")
        
        self.total_input.setReadOnly(True)

        self.transaction_tab = TransactionTab(parent=self, total=self.total_input)
        
        buttons_widget, buttons = createWindowButtons()

        buttons[0].clicked.connect(lambda: self.saveSale(self.search_client_input, self.transaction_tab))
        buttons[1].clicked.connect(lambda: self.resetInputs())

        total_box_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        total_box_layout.addWidget(products_total_label)
        total_box_layout.addWidget(total_label)
        total_box_layout.addWidget(self.total_input)

        layout.addWidget(client_box)
        layout.addWidget(self.transaction_tab)
        layout.addWidget(total_box)
        layout.addWidget(buttons_widget)

        scroll_area.setWidget(widget)

        return scroll_area
    
    def saveSale(self, client: LineEdit, tab: TransactionTab):
        data = {
            "cliente": client.text(),
            "itens": tab.getAllProducts(),
            "pagamentos": tab.getAllPayments(),
            "valor_total": self.total_input.value(),
        }

        try:
            if self.id_input.value() == 0:
                SalesController.save(data)
            else:
                SalesController.remove(self.id_input.value())
                data["id_pedido"] = self.id_input.value()
                SalesController.save(data)
            
            message = MessageDialog(self, title="Sucesso", message="Venda salva com sucesso!", msg_type=MessageDialog.SUCCESS)
            message.exec()
        except Exception as e:
            message = MessageDialog(self, title="Erro", message=f"Erro ao salvar a venda: {str(e)}", msg_type=MessageDialog.ERROR)
            message.exec()
            return

        self.resetInputs()
        self.transaction_tab.resetInputs()

        client.setText("CONSUMIDOR PADRÃO")
        client.setReadOnly(True)
        self.item_explorer.hide()

    def resetInputs(self):
        self.search_client_input.setText("")
        self.transaction_tab.resetInputs()
        self.total_input.setValue(0)

    def editSale(self, table: Table):
        selectedItems = table.selectedItems()

        SalesController.get(self, {"id": selectedItems[0].text()}, "edit")

        self.tab.setCurrentIndex(1)

    def removeSale(self, table: Table):
        selectedItems = table.selectedItems()
    
        SalesController.remove(selectedItems[0].text())

        SalesController.get(self, {"data_inicio": self.initial_date.text(), "data_final": self.final_date.text()}, "search")
    
    def setupSearch(self, search_widget : QLineEdit, data):
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