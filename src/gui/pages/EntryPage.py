from PySide6.QtWidgets import *
from PySide6.QtCore import QDate, QPoint
from PySide6.QtGui import QIcon

from src.controllers.personController import PersonController
from src.controllers.productController import ProductController
from src.controllers.utilsController import UtilsController
from src.gui.widgets import *

from src.models.personModel import getPersonID

from src.gui.utils import createTableButtons, createWindowButtons
from src.gui.widgets.removeWindow import MessageDialog
from src.utils.itemExplorer import ItemExplorer

class EntryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.item_explorer = ItemExplorer(self, type="compra")

        self.labels_box = QWidget()
        self.labels_box_layout = QVBoxLayout()

        self.title = Label("Entrada de notas", type="Title")
        self.subtitle = Label("Gerencie todas as notas cadastradas", type="Subtitle")

        self.labels_box_layout.addWidget(self.title)
        self.labels_box_layout.addWidget(self.subtitle)

        self.labels_box.setLayout(self.labels_box_layout)

        self.search_tab = self.createSearchTab()
        self.edition_tab = self.createEditionTab()

        self.tab = Tab()
        self.tab.addTab(self.search_tab, "Pesquisar entradas")
        self.tab.addTab(self.edition_tab, "Adicionar/Editar entradas")

        self.main_layout.addWidget(self.labels_box)
        self.main_layout.addWidget(self.tab)
        
        self.setLayout(self.main_layout)

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

        search_button.clicked.connect(lambda: UtilsController.getEntries(self, {"initial_date": self.initial_date.text(), "final_date": self.final_date.text()}))

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

        self.search_table = Table(["ID", "Data", "Cliente", "Valor total"])

        self.search_table.add_action.triggered.connect(lambda: self.tab.setCurrentWidget(self.edition_tab))
        self.search_table.edit_action.triggered.connect(self.editEntry)
        self.search_table.remove_action.triggered.connect(self.removeEntry)

        search_layout.addWidget(self.search_table, 2, 0, 1, 6)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.search_table)

        return widget
    
    def createEditionTab(self):
        self.form_widget = TabWidget()
        self.form_layout = QVBoxLayout()

        self.form_widget.setLayout(self.form_layout)

        self.entry_group = GroupBox("Detalhes da entrada")
        self.entry_layout = QGridLayout()
        self.entry_group.setLayout(self.entry_layout)

        self.supplier_search_label = Label("Fornecedor", type="InputLabel")
        self.product_search_label = Label("Produto", type="InputLabel")
        self.product_current_price_label = Label("Preço atual", type="InputLabel")
        self.product_price_label = Label("Novo preço de compra", type="InputLabel")
        self.product_quantity_label = Label("Quantidade", type="InputLabel")
        self.has_expiration_date_label = Label("Possui data de validade?", type="InputLabel")
        self.expiry_date_label = Label("Data de validade", type="InputLabel")

        self.entry_id = SpinBox()
        self.entry_id.setReadOnly(True)
        self.entry_id.hide()

        self.supplier_search_input = LineEdit(placeholder="Procure por um fornecedor...")
        self.product_search_input = LineEdit(placeholder="Procure por um produto...")

        self.product_current_price_input = DoubleSpinBox()
        self.product_current_price_input.setPrefix("R$ ")
        self.product_current_price_input.setDisabled(True)

        self.product_price_input = DoubleSpinBox()
        self.product_quantity_input = SpinBox()
        self.has_expiration_date_input = QCheckBox()
        self.expiry_date_input = DateEdit(date=QDate.currentDate())
        self.expiry_date_input.setEnabled(False)

        self.has_expiration_date_input.stateChanged.connect(self.updateExpirationDate)

        self.supplier_search_input.setMaximumWidth(3000)
        self.product_search_input.setMaximumWidth(3000)

        self.setupSearch(self.supplier_search_input, "Person")
        self.setupSearch(self.product_search_input, "Product")
        
        self.product_price_input.setPrefix("R$ ")

        self.buttons_widget, self.buttons = createTableButtons()

        self.buttons[0].clicked.connect(self.addItemToTable)
        self.buttons[1].clicked.connect(self.editItemInTable)
        self.buttons[2].clicked.connect(self.removeItemFromTable)

        self.table = Table(["ID", "Nome", "Preço de compra", "Quantidade", "Data de validade"])

        self.windowb_widgets, self.window_buttons = createWindowButtons()

        self.window_buttons[0].clicked.connect(self.saveEntry)
        self.window_buttons[1].clicked.connect(lambda: self.clearFields())
        self.window_buttons[2].clicked.connect(lambda: print("Cancelar entrada"))

        self.entry_layout.addWidget(self.supplier_search_label, 0, 0)
        self.entry_layout.addWidget(self.product_search_label, 2, 0)
        self.entry_layout.addWidget(self.product_current_price_label, 4, 0)
        self.entry_layout.addWidget(self.product_price_label, 4, 1)
        self.entry_layout.addWidget(self.product_quantity_label, 4, 2)
        self.entry_layout.addWidget(self.expiry_date_label, 4, 3)
        self.entry_layout.addWidget(self.has_expiration_date_label, 4, 4)

        self.entry_layout.addWidget(self.supplier_search_input, 1, 0, 1, 6)
        self.entry_layout.addWidget(self.product_search_input, 3, 0, 1, 6)
        self.entry_layout.addWidget(self.product_current_price_input, 5, 0)
        self.entry_layout.addWidget(self.product_price_input, 5, 1)
        self.entry_layout.addWidget(self.product_quantity_input, 5, 2)
        self.entry_layout.addWidget(self.expiry_date_input, 5, 3)
        self.entry_layout.addWidget(self.has_expiration_date_input, 5, 4)
        self.entry_layout.addWidget(self.buttons_widget, 5, 5)
        self.entry_layout.addWidget(self.table, 6, 0, 1, 6)

        self.form_layout.addWidget(self.entry_group)
        self.form_layout.addWidget(self.windowb_widgets)

        return self.form_widget
    
    def saveEntry(self):
        try:
            items = self.getAllItems()

            data = {"fornecedor": getPersonID(self.supplier_search_input.text())[0],
                    "itens": items,
                    "data": QDate.currentDate().toString("yyyy-MM-dd"),
                    "valor_total": sum([item["preco_compra"] * item["quantidade"] for item in items])}
            
            if self.entry_id.value() != 0:
                UtilsController.editEntry(self.entry_id.value(), data)
            else:
                UtilsController.addEntry(data)

            self.table.setRowCount(0)
            self.clearFields([self.supplier_search_input, self.product_search_input, self.product_price_input, self.product_quantity_input, self.has_expiration_date_input, self.expiry_date_input])

            msg = MessageDialog(self, title="Sucesso", message="Entrada salva com sucesso!", msg_type=MessageDialog.SUCCESS)
            msg.exec()
        except Exception as e:
            msg = MessageDialog(self, title="Erro", message=f"Ocorreu um erro ao salvar a entrada: {str(e)}", msg_type=MessageDialog.ERROR)
            msg.exec()
            return
        
    def editEntry(self):
        selected_items = self.search_table.selectedItems()
        if not selected_items:
            msg = MessageDialog(self, title="Erro", message="Por favor, selecione uma entrada para editar.", msg_type=MessageDialog.ERROR)
            msg.exec()
            return

        entry_id = selected_items[0].text()

        items = UtilsController.getEntryByID(entry_id)

        self.supplier_search_input.setText(items[0][0])
        self.supplier_search_input.setReadOnly(True)
        self.entry_id.setValue(items[0][5])

        for item in items:
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(self.table.rowCount() - 1)))
            self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(item[1]))
            self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(f"R$ {item[3]:.2f}"))
            self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem(str(item[2])))
            self.table.setItem(self.table.rowCount() - 1, 4, QTableWidgetItem(item[4] if item[4] != None else ""))

        self.tab.setCurrentWidget(self.edition_tab)
        self.item_explorer.hide()

    def removeEntry(self):
        selected_items = self.search_table.selectedItems()
        if not selected_items:
            msg = MessageDialog(self, title="Erro", message="Por favor, selecione uma entrada para remover.", msg_type=MessageDialog.ERROR)
            msg.exec()
            return
        
        entry_id = selected_items[0].text()
    
    def getAllItems(self):
        items = []
        for row in range(self.table.rowCount()):
            item = {
                "nome": self.table.item(row, 1).text(),
                "preco_compra": float(self.table.item(row, 2).text().replace("R$ ", "")),
                "quantidade": int(self.table.item(row, 3).text()),
                "data_validade": self.table.item(row, 4).text() if self.table.item(row, 4).text() != "" else None
            }
            items.append(item)
        return items

    def setupSearch(self, search_widget : QLineEdit, controller):
        # Botão de limpar
        clear_action = search_widget.addAction(QIcon.fromTheme("window-close"), QLineEdit.TrailingPosition)
        clear_action.triggered.connect(lambda: self.clearFields([search_widget]))

        targets = {"nome": search_widget}
        if controller == "Product":
            targets["valor"] = self.product_current_price_input

        # Conecta textChanged
        search_widget.textChanged.connect(
            lambda text: self.searchItems(PersonController.get_suppliers({"pesquisa": search_widget.text()}) if controller == "Person" else ProductController.get(self, {"pesquisa": search_widget.text()}, "search_item"), targets, search_widget))
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

    def updateExpirationDate(self):
        if self.has_expiration_date_input.isChecked():
            self.expiry_date_input.setEnabled(True)
        else:
            self.expiry_date_input.setEnabled(False)
            self.expiry_date_input.setDate(QDate.currentDate())

    def addItemToTable(self):
        name = self.product_search_input.text()
        price = self.product_price_input.value()
        quantity = self.product_quantity_input.value()
        expiry_date = self.expiry_date_input.date().toString("dd/MM/yyyy") if self.has_expiration_date_input.isChecked() else "N/A"

        if not name or price <= 0 or quantity <= 0:
            msg = MessageDialog(self, title="Erro", message="Por favor, preencha todos os campos corretamente.", msg_type=MessageDialog.ERROR)
            msg.exec()
            return

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
        self.table.setItem(row_position, 1, QTableWidgetItem(name))
        self.table.setItem(row_position, 2, QTableWidgetItem(f"R$ {price:.2f}"))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(quantity)))
        
        if expiry_date == "N/A":
            self.table.setItem(row_position, 4, QTableWidgetItem(""))
        else:
            self.table.setItem(row_position, 4, QTableWidgetItem(expiry_date))

        self.clearFields([self.product_search_input, self.product_price_input, self.product_quantity_input, self.has_expiration_date_input, self.expiry_date_input])
    
    def editItemInTable(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            msg = MessageDialog(self, title="Erro", message="Por favor, selecione um item para editar.", msg_type=MessageDialog.ERROR)
            msg.exec()
            return

        selected_row = selected_items[0].row()

        self.product_search_input.setText(self.table.item(selected_row, 1).text())
        price_text = self.table.item(selected_row, 2).text().replace("R$ ", "")
        self.product_price_input.setValue(float(price_text))
        self.product_quantity_input.setValue(int(self.table.item(selected_row, 3).text()))
        expiry_date_text = self.table.item(selected_row, 4).text()
        if expiry_date_text != "":
            self.has_expiration_date_input.setChecked(True)
            day, month, year = map(int, expiry_date_text.split("/"))
            self.expiry_date_input.setDate(QDate(year, month, day))
        else:
            self.has_expiration_date_input.setChecked(False)

        #self.clearFields([self.product_search_input, self.product_price_input, self.product_quantity_input, self.has_expiration_date_input, self.expiry_date_input])
        self.removeItemFromTable(True)
        self.item_explorer.hide()

    def removeItemFromTable(self, edit=False):
        selected_items = self.table.selectedItems()
        if not selected_items:
            msg = MessageDialog(self, title="Erro", message="Por favor, selecione um item para remover.", msg_type=MessageDialog.ERROR)
            msg.exec()
            return
        
        selected_row = selected_items[0].row()

        if edit == False:
            confirm = MessageDialog(self, title="Confirmar Remoção", message="Tem certeza que deseja remover o item selecionado?", msg_type=MessageDialog.WARNING)
            if confirm.exec() == QDialog.Accepted:
                self.table.removeRow(selected_row)
        else:
            self.table.removeRow(selected_row)