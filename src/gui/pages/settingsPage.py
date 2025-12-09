from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from src.gui.widgets import *
from src.gui.widgets.removeWindow import RemoveDialog, MessageDialog
from src.gui.utils import *
from src.gui.colors import *

from src.models import productModel, utilsModels

import json

class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.main_window = main_window

        with open("src/configuration.json", "r") as f:
            self.config = json.load(f)

        # Labels
        labels_widget = QWidget()
        labels_layout = QVBoxLayout()
        labels_widget.setLayout(labels_layout)

        title_label = Label(text="Painel de Configuração", type="Title")
        subtitle_label = Label(text="Configure novos valores ou customize o layout", type="Subtitle")

        labels_layout.addWidget(title_label)
        labels_layout.addWidget(subtitle_label)

        tab = Tab()
        
        product_detail_tab = self.createProductDetailTab()
        services_tab = self.createServicesTab()
        payment_tab = self.createPaymentTab()
        customization_tab = self.createCustomizationTab()

        tab.addTab(product_detail_tab, "Produtos")
        tab.addTab(services_tab, "Serviços")
        tab.addTab(payment_tab, "Pagamentos")
        tab.addTab(customization_tab, "Aparência")

        layout.addWidget(labels_widget)
        layout.addWidget(tab)

    def createProductDetailTab(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent !important;")

        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        brand_box = GroupBox("Informações de marcas")
        brand_box_layout = QGridLayout()
        brand_box.setLayout(brand_box_layout)

        brand_name_label = Label("Marca", type="InputLabel")

        self.brand_id = SpinBox()
        self.brand_id.setReadOnly(True)
        self.brand_id.setValue(0)
        self.brand_id.hide()

        self.brand_name_input = LineEdit(placeholder="Digite o nome da marca")
        self.brand_name_input.editingFinished.connect(lambda: self.getBrands(self.brand_name_input.text()))

        brand_buttons_widget, brand_buttons = createTableButtons()

        brand_buttons[0].clicked.connect(self.addBrand)
        brand_buttons[1].clicked.connect(self.editBrand)
        brand_buttons[2].clicked.connect(self.removeBrand)

        self.brand_table = Table(["ID", "Nome", "Produtos"])

        brand_box_layout.addWidget(brand_name_label, 0, 0)

        brand_box_layout.addWidget(self.brand_name_input, 1, 0)
        brand_box_layout.addWidget(brand_buttons_widget, 1, 1)

        brand_box_layout.addWidget(self.brand_table, 2, 0, 1, 2)

        brand_box_layout.setColumnStretch(0, 3)
        brand_box_layout.setColumnStretch(1, 1)

        category_box = GroupBox("Informações de categoria")
        category_box_layout = QGridLayout()
        category_box.setLayout(category_box_layout)

        category_name_label = Label("Categoria", type="InputLabel")

        self.category_id = SpinBox()
        self.category_id.setReadOnly(True)
        self.category_id.setValue(0)
        self.category_id.hide()

        self.category_name_input = LineEdit(placeholder="Digite o nome da categoria")
        self.category_name_input.editingFinished.connect(lambda: self.getCategories(self.category_name_input.text()))

        self.category_buttons_widget, category_buttons = createTableButtons()

        category_buttons[0].clicked.connect(self.addCategory)
        category_buttons[1].clicked.connect(self.editCategory)
        category_buttons[2].clicked.connect(self.removeCategory)

        self.category_table = Table(["ID", "Nome", "Produtos"])

        category_box_layout.addWidget(category_name_label, 0, 0)

        category_box_layout.addWidget(self.category_name_input, 1, 0)
        category_box_layout.addWidget(self.category_buttons_widget, 1, 1)

        category_box_layout.addWidget(self.category_table, 2, 0, 1, 2)

        category_box_layout.setColumnStretch(0, 3)
        category_box_layout.setColumnStretch(1, 1)

        layout.addWidget(brand_box)
        layout.addWidget(category_box)

        scroll_area.setWidget(widget)

        return scroll_area

    def createServicesTab(self):
        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        info_box = GroupBox("Informações de serviços")
        info_box_layout = QGridLayout()
        info_box.setLayout(info_box_layout)

        self.service_id = SpinBox()
        self.service_id.setReadOnly(True)
        self.service_id.setValue(0)
        self.service_id.hide()

        name_label = Label("Nome de serviço", type="InputLabel")
        description_label = Label("Descrição", type="InputLabel")
        price_label = Label("Preço", type="InputLabel")

        self.service_name_input = LineEdit(placeholder="Digite o nome do serviço")
        self.service_description_input = LineEdit(placeholder="Adicione uma descrição para o serviço (Opcional)")
        self.service_price_input = DoubleSpinBox()
        self.service_price_input.setPrefix("R$ ")

        self.service_name_input.editingFinished.connect(lambda: self.getServices(self.service_name_input.text()))

        buttons_widget, buttons = createTableButtons()

        buttons[0].clicked.connect(self.addService)
        buttons[1].clicked.connect(self.editService)
        buttons[2].clicked.connect(self.removeService)

        self.services_table = Table(["ID", "Tipo", "Preço", "Descrição"])

        info_box_layout.addWidget(name_label, 0, 0)
        info_box_layout.addWidget(price_label, 0, 1)
        info_box_layout.addWidget(description_label, 2, 0)

        info_box_layout.addWidget(self.service_name_input, 1, 0)
        info_box_layout.addWidget(self.service_price_input, 1, 1)
        info_box_layout.addWidget(self.service_description_input, 3, 0)
        info_box_layout.addWidget(buttons_widget, 3, 1)

        info_box_layout.addWidget(self.services_table, 4, 0, 1, 2)

        info_box_layout.setColumnStretch(0, 3)
        info_box_layout.setColumnStretch(1, 1)

        layout.addWidget(info_box)

        return widget

    def createPaymentTab(self):
        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        self.payment_method_id = SpinBox()
        self.payment_method_id.setReadOnly(True)
        self.payment_method_id.setValue(0)
        self.payment_method_id.hide()

        info_box = GroupBox("Configurações de pagamentos")
        info_box_layout = QGridLayout()
        info_box.setLayout(info_box_layout)

        payment_method_label = Label("Forma de pagamento", type="InputLabel")

        self.payment_method_input = LineEdit(placeholder="Digite o nome da forma de pagamento")
        self.payment_method_input.editingFinished.connect(lambda: self.getPaymentMethods(self.payment_method_input.text()))

        buttons_widget, buttons = createTableButtons()

        buttons[0].clicked.connect(self.addPaymentMethod)
        buttons[1].clicked.connect(self.editPaymentMethod)
        buttons[2].clicked.connect(self.removePaymentMethod)

        self.payments_table = Table(["ID", "Tipo"])

        info_box_layout.addWidget(payment_method_label, 0, 0)

        info_box_layout.addWidget(self.payment_method_input, 1, 0)
        info_box_layout.addWidget(buttons_widget, 1, 1)

        info_box_layout.addWidget(self.payments_table, 2, 0, 1, 2)

        info_box_layout.setColumnStretch(0, 3)
        info_box_layout.setColumnStretch(1, 1)

        layout.addWidget(info_box)

        return widget
        
    def createCustomizationTab(self):
        def onValueChanged(value, config_name):
            self.config[config_name] = value

        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        theme_box = GroupBox("Temas")
        theme_box_layout = QHBoxLayout()
        theme_box.setLayout(theme_box_layout)

        self.light_radio = QRadioButton("Claro")
        #self.dark_radio = QRadioButton("Escuro")

        if self.config["THEME"] == "dark":
            self.dark_radio.setChecked(True)
        else:
            self.light_radio.setChecked(True)

        #self.light_radio.toggled.connect(lambda checked: self.onThemeChanged("light") if checked else None)
        #self.dark_radio.toggled.connect(lambda checked: self.onThemeChanged("dark") if checked else None)

        theme_box_layout.addWidget(self.light_radio)
        #theme_box_layout.addWidget(self.dark_radio)
        theme_box_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        options_box = GroupBox("Personalizar")
        options_box_layout = QVBoxLayout()
        options_box.setLayout(options_box_layout)

        fonts_box = GroupBox("Tamanho de fontes")
        fonts_box_layout = QGridLayout()
        fonts_box.setLayout(fonts_box_layout)

        sidemenu_label_size = Label("Menu lateral", type="InputLabel")
        normal_label_size = Label("Normal", type="InputLabel")
        input_label_size = Label("Inputs (em negrito)", type="InputLabel")
        title_label_size = Label("Títulos", type="InputLabel")
        subtitle_label_size = Label("Subtítulo", type="InputLabel")

        sidemenu_input_size = SpinBox()
        sidemenu_input_size.valueChanged.connect(lambda size: onValueChanged(size, "SIDE_MENU_LABEL_SIZE"))
        sidemenu_input_size.setValue(self.config["SIDE_MENU_LABEL_SIZE"])
        sidemenu_input_size.setSuffix(" px")
        
        normal_input_size = SpinBox()
        normal_input_size.valueChanged.connect(lambda size: onValueChanged(size, "NORMAL_LABEL_SIZE"))
        normal_input_size.setValue(self.config["NORMAL_LABEL_SIZE"])
        normal_input_size.setSuffix(" px")
        
        input_input_size = SpinBox()
        input_input_size.valueChanged.connect(lambda size: onValueChanged(size, "INPUT_LABEL_SIZE"))
        input_input_size.setValue(self.config["INPUT_LABEL_SIZE"])
        input_input_size.setSuffix(" px")
        
        title_input_size = SpinBox()
        title_input_size.valueChanged.connect(lambda size: onValueChanged(size, "TITLE_LABEL_SIZE"))
        title_input_size.setValue(self.config["TITLE_LABEL_SIZE"])
        title_input_size.setSuffix(" px")
        
        subtitle_input_size = SpinBox()
        subtitle_input_size.valueChanged.connect(lambda size: onValueChanged(size, "SUBTITLE_LABEL_SIZE"))
        subtitle_input_size.setValue(self.config["SUBTITLE_LABEL_SIZE"])
        subtitle_input_size.setSuffix(" px")

        fonts_box_layout.addWidget(sidemenu_label_size, 0, 0)
        fonts_box_layout.addWidget(normal_label_size, 0, 1)
        fonts_box_layout.addWidget(input_label_size, 0, 2)
        fonts_box_layout.addWidget(title_label_size, 0, 3)
        fonts_box_layout.addWidget(subtitle_label_size, 0, 4)

        fonts_box_layout.addWidget(sidemenu_input_size, 1, 0)
        fonts_box_layout.addWidget(normal_input_size, 1, 1)
        fonts_box_layout.addWidget(input_input_size, 1, 2)
        fonts_box_layout.addWidget(title_input_size, 1, 3)
        fonts_box_layout.addWidget(subtitle_input_size, 1, 4)

        colors_box = GroupBox("Cores")
        colors_box_layout = QGridLayout()
        colors_box.setLayout(colors_box_layout)

        primary_color_label = Label("Cor primária", type="InputLabel")
        primary_color_hover_label = Label("Cor primária (Hover)", type="InputLabel")
        secondary_color_label = Label("Cor secundária", type="InputLabel")
        secondary_color_hover_label = Label("Cor secundária (Hover)", type="InputLabel")

        self.primary_color_input = ColorLineEdit(initial_color=self.config["PRIMARY_COLOR"], parent=self)
        self.primary_color_hover_input = ColorLineEdit(initial_color=self.config["PRIMARY_COLOR_HOVER"], parent=self)
        self.secondary_color_input = ColorLineEdit(initial_color=self.config["SECONDARY_COLOR"], parent=self)
        self.secondary_color_hover_input = ColorLineEdit(initial_color=self.config["SECONDARY_COLOR_HOVER"], parent=self)

        colors_box_layout.addWidget(primary_color_label, 0, 0)
        colors_box_layout.addWidget(secondary_color_label, 2, 0)
        colors_box_layout.addWidget(primary_color_hover_label, 0, 1)
        colors_box_layout.addWidget(secondary_color_hover_label, 2, 1)

        colors_box_layout.addWidget(self.primary_color_input, 1, 0)
        colors_box_layout.addWidget(self.secondary_color_input, 3, 0)
        colors_box_layout.addWidget(self.primary_color_hover_input, 1, 1)
        colors_box_layout.addWidget(self.secondary_color_hover_input, 3, 1) 

        options_box_layout.addWidget(fonts_box)
        options_box_layout.addWidget(colors_box)
        options_box_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        buttons = QWidget()
        buttons_layout = QHBoxLayout()
        buttons.setLayout(buttons_layout)

        reset_inputs_button = PushButton("Restaurar valores", icon_path="reset.svg")
        reset_colors_button = PushButton("Restaurar cores", icon_path="reset.svg")
        apply_button = PushButton("Salvar", icon_path="disk.svg")

        buttons_layout.addWidget(reset_inputs_button)
        buttons_layout.addWidget(reset_colors_button)
        buttons_layout.addWidget(apply_button)

        reset_inputs_button.clicked.connect(lambda x: self.resetInputs(sidemenu_input_size, normal_input_size, input_input_size, title_input_size, subtitle_input_size))
        reset_colors_button.clicked.connect(self.resetColors)
        apply_button.clicked.connect(self.saveConfig)

        layout.addWidget(theme_box)
        layout.addWidget(options_box)
        layout.addWidget(buttons)

        return widget

    # Dentro da classe SettingsPage

    # --- Métodos de Marcas (Brands) ---

    def getBrands(self, name=''):
        """Carregwa dados de marcas do DB e preenche a tabela."""
        try:
            # ⚠️ Substitua 'db_manager' pela sua instância de conexão real, se necessário.
            brands = productModel.getBrands(name)
            self.brand_table.setRowCount(0) # Limpa a tabela
            for row, brand in enumerate(brands):
                self.brand_table.insertRow(row)
                self.brand_table.setItem(row, 0, QTableWidgetItem(str(brand[0])))
                self.brand_table.setItem(row, 1, QTableWidgetItem(brand[1]))
                self.brand_table.setItem(row, 2, QTableWidgetItem(str(brand[2])))
        except Exception as e:
            print(f"ERRO ao carregar marcas: {e}")

    def addBrand(self):
        """Adiciona uma nova marca usando o nome do input."""
        name = self.brand_name_input.text().strip()
        if name:
            try:
                # Lógica de validação e chamada ao DB
                if self.brand_id.value() == 0:
                    productModel.addBrand(name)
                else:
                    productModel.updateBrand(self.brand_id.value(), name)
                    self.brand_id.setValue(0)
                self.brand_name_input.clear()
                self.getBrands() # Recarrega a tabela
                
                message = MessageDialog(self, "Sucesso", message=f"Marca '{name}' adicionada com sucesso!", msg_type=MessageDialog.SUCCESS)
                message.exec()
            except Exception as e:
                message = MessageDialog(self, "Erro", message=f"ERRO ao adicionar marca: {e}", msg_type=MessageDialog.ERROR)
                message.exec()
        else:
            print("O nome da marca não pode estar vazio.")

    def editBrand(self):
        """Edita a marca selecionada na tabela (requer lógica para obter ID e novo nome)."""
        selected_items = self.brand_table.selectedItems()
        if not selected_items:
            print("Selecione uma marca para editar.")
            return

        # Pega o ID da primeira célula da linha selecionada
        row = selected_items[0].row()
        self.brand_id.setValue(int(self.brand_table.item(row, 0).text()))

        self.brand_name_input.setText(selected_items[1].text())

    def removeBrand(self):
        """Remove a marca selecionada na tabela."""
        selected_items = self.brand_table.selectedItems()
        if not selected_items:
            print("Selecione uma marca para remover.")
            return
            
        row = selected_items[0].row()
        brand_id = int(self.brand_table.item(row, 0).text())
        brand_name = self.brand_table.item(row, 1).text()
        
        # Mostra dialog de confirmação
        dialog = RemoveDialog(
            parent=self,
            title="Remover Marca",
            item_name=f"Marca: {brand_name}"
        )
        
        if dialog.exec() == QDialog.Accepted:
            try:
                productModel.removeBrand(brand_id)
                self.getBrands()
                print(f"Marca ID {brand_id} removida com sucesso.")
            except Exception as e:
                print(f"ERRO ao remover marca: {e}")

    # --- Métodos de Categorias (Categories) ---

    def getCategories(self, name=''):
        """Carrega dados de categorias do DB e preenche a tabela."""
        try:
            categories = productModel.getCategories(name)
            self.category_table.setRowCount(0)
            for row, category in enumerate(categories):
                self.category_table.insertRow(row)
                self.category_table.setItem(row, 0, QTableWidgetItem(str(category[0])))
                self.category_table.setItem(row, 1, QTableWidgetItem(category[1]))
                self.category_table.setItem(row, 2, QTableWidgetItem(str(category[2])))
        except Exception as e:
            print(f"ERRO ao carregar categorias: {e}")

    def addCategory(self):
        """Adiciona uma nova categoria usando o nome do input."""
        name = self.category_name_input.text().strip()
        if name:
            try:
                if self.category_id.value() == 0:
                    productModel.addCategory(name)
                else:
                    productModel.updateCategory(self.category_id.value(), name)
                    self.category_id.setValue(0)
                self.category_name_input.clear()
                self.getCategories()
                
                message = MessageDialog(self, "Sucesso", message=f"Categoria '{name}' adicionada com sucesso!", msg_type=MessageDialog.SUCCESS)
                message.exec()
            except Exception as e:
                message = MessageDialog(self, "Erro", message=f"ERRO ao adicionar categoria: {e}", msg_type=MessageDialog.ERROR)
                message.exec()
        else:
            print("O nome da categoria não pode estar vazio.")

    def editCategory(self):
        """Edita a marca selecionada na tabela (requer lógica para obter ID e novo nome)."""
        selected_items = self.category_table.selectedItems()
        if not selected_items:
            print("Selecione uma marca para editar.")
            return

        # Pega o ID da primeira célula da linha selecionada
        row = selected_items[0].row()
        self.category_id.setValue(int(self.category_table.item(row, 0).text()))

        self.category_name_input.setText(selected_items[1].text())

    def removeCategory(self):
        """Remove a categoria selecionada na tabela."""
        selected_items = self.category_table.selectedItems()
        if not selected_items:
            print("Selecione uma categoria para remover.")
            return
            
        row = selected_items[0].row()
        category_id = int(self.category_table.item(row, 0).text())
        category_name = self.category_table.item(row, 1).text()
        
        # Mostra dialog de confirmação
        dialog = RemoveDialog(
            parent=self,
            title="Remover Categoria",
            item_name=f"Categoria: {category_name}"
        )
        
        if dialog.exec() == QDialog.Accepted:
            try:
                productModel.removeCategory(category_id)
                self.getCategories()
                print(f"Categoria ID {category_id} removida com sucesso.")
            except Exception as e:
                print(f"ERRO ao remover categoria: {e}")

    def getPaymentMethods(self, name=''):
        """Carregwa dados de marcas do DB e preenche a tabela."""
        try:
            # ⚠️ Substitua 'db_manager' pela sua instância de conexão real, se necessário.
            methods = utilsModels.getPaymentsMethods(name)
            print(methods)
            self.payments_table.setRowCount(0) # Limpa a tabela
            for row, method in enumerate(methods):
                self.payments_table.insertRow(row)
                self.payments_table.setItem(row, 0, QTableWidgetItem(str(method[0])))
                self.payments_table.setItem(row, 1, QTableWidgetItem(method[1]))
        except Exception as e:
            print(f"ERRO ao carregar marcas: {e}")

    def addPaymentMethod(self):
        """Adiciona uma nova marca usando o nome do input."""
        name = self.payment_method_input.text().strip()
        if name:
            try:
                if self.payment_method_id.value() == 0:
                    utilsModels.addPaymenthMethod(name)
                else:
                    utilsModels.updatePaymentMethods(self.payment_method_id.value(), name)
                    self.payment_method_id.setValue(0)
                self.payment_method_input.clear()
                self.getPaymentMethods() # Recarrega a tabela
                
                message = MessageDialog(self, "Sucesso", message=f"Forma de Pagamento '{name}' adicionada com sucesso!", msg_type=MessageDialog.SUCCESS)
                message.exec()

            except Exception as e:
                message = MessageDialog(self, "ERRO", message=f"ERRO ao adicionar forma de pagamento: {e}", msg_type=MessageDialog.ERROR)
                message.exec()
        else:
            print("O nome da marca não pode estar vazio.")

    def editPaymentMethod(self):
        """Edita a marca selecionada na tabela (requer lógica para obter ID e novo nome)."""
        selected_items = self.payments_table.selectedItems()
        if not selected_items:
            print("Selecione uma marca para editar.")
            return

        # Pega o ID da primeira célula da linha selecionada
        row = selected_items[0].row()
        self.payment_method_id.setValue(int(self.payments_table.item(row, 0).text()))

        self.payment_method_input.setText(selected_items[1].text())

    def removePaymentMethod(self):
        """Remove a marca selecionada na tabela."""
        selected_items = self.payments_table.selectedItems()
        if not selected_items:
            print("Selecione uma marca para remover.")
            return
            
        row = selected_items[0].row()
        self.payment_method_id.setValue(int(self.payments_table.item(row, 0).text()))
        
        dialog = RemoveDialog(
            parent=self,
            title="Remover forma de pagamento",
            item_name=f"Forma de pagamento: {self.payments_table.item(row, 1).text()}"
        )

        if dialog.exec() == QDialog.Accepted:
            try:
                utilsModels.removePaymentMethods(self.payment_method_id.value())
                self.getPaymentMethods()
                print(f"Marca ID {self.payment_method_id.value()} removida com sucesso.")
            except Exception as e:
                print(f"ERRO ao remover marca: {e}")

    def getServices(self, name=''):
        """Carregwa dados de marcas do DB e preenche a tabela."""
        try:
            # ⚠️ Substitua 'db_manager' pela sua instância de conexão real, se necessário.
            services = utilsModels.getServices(name)
            self.services_table.setRowCount(0) # Limpa a tabela
            for row, service in enumerate(services):
                self.services_table.insertRow(row)
                self.services_table.setItem(row, 0, QTableWidgetItem(str(service[0])))
                self.services_table.setItem(row, 1, QTableWidgetItem(service[1]))
                self.services_table.setItem(row, 2, QTableWidgetItem(str(service[2])))
                self.services_table.setItem(row, 3, QTableWidgetItem(str(service[3])))
        except Exception as e:
            print(f"ERRO ao carregar marcas: {e}")

    def addService(self):
        """Adiciona uma nova marca usando o nome do input."""
        name = self.service_name_input.text().strip()
        price = self.service_price_input.value()
        description = self.service_description_input.text()

        data = {"name": name, "price": price, "description": description}
        if name:
            try:
                # Lógica de validação e chamada ao DB
                if self.service_id.value() == 0:
                    utilsModels.addService(data)
                else:
                    utilsModels.updateService(self.service_id.value(), data)
                    self.service_id.setValue(0)
                
                self.service_name_input.clear()
                self.service_price_input.setValue(0.0)
                self.service_description_input.clear()
                self.getServices() # Recarrega a tabela
                
                message = MessageDialog(self, "Sucesso", message=f"Serviço '{name}' adicionada com sucesso!", msg_type=MessageDialog.SUCCESS)
                message.exec()
            except Exception as e:
                message = MessageDialog(self, "ERRO", message=f"ERRO ao adicionar serviço: {e}", msg_type=MessageDialog.ERROR)
                message.exec()
        else:
            print("O nome da marca não pode estar vazio.")

    def editService(self):
        """Edita a marca selecionada na tabela (requer lógica para obter ID e novo nome)."""
        selected_items = self.services_table.selectedItems()
        if not selected_items:
            print("Selecione uma marca para editar.")
            return

        # Pega o ID da primeira célula da linha selecionada
        row = selected_items[0].row()
        self.service_id.setValue(int(self.services_table.item(row, 0).text()))

        self.service_name_input.setText(selected_items[1].text())
        self.service_price_input.setValue(float(selected_items[2].text()))
        self.service_description_input.setText(selected_items[3].text())

    def removeService(self):
        """Remove a marca selecionada na tabela."""
        selected_items = self.services_table.selectedItems()
        if not selected_items:
            print("Selecione uma marca para remover.")
            return
            
        row = selected_items[0].row()
        self.service_id.setValue(int(self.services_table.item(row, 0).text()))
        
        dialog = RemoveDialog(
            parent=self,
            title="Remover serviço",
            item_name=f"Serviço: {self.services_table.item(row, 1).text()}"
        )

        if dialog.exec() == QDialog.Accepted:
            try:
                utilsModels.removeService(self.service_id.value())
                self.service_id.setValue(0)
                self.getServices()
                print(f"Marca ID {self.service_id.value()} removida com sucesso.")
            except Exception as e:
                print(f"ERRO ao remover marca: {e}")
    
    def onThemeChanged(self, theme):
        self.config["THEME"] = theme
    
    def saveConfig(self):
        try:
            self.setCursor(Qt.WaitCursor)

            new_primary = self.primary_color_input.text()
            new_primary_hover = self.primary_color_hover_input.text()
            new_secondary = self.secondary_color_input.text()
            new_secondary_hover = self.secondary_color_hover_input.text()

            self.config["PRIMARY_COLOR"] = new_primary
            self.config["PRIMARY_COLOR_HOVER"] = new_primary_hover
            self.config["SECONDARY_COLOR"] = new_secondary
            self.config["SECONDARY_COLOR_HOVER"] = new_secondary_hover

            with open("src/configuration.json", "w") as f:
                json.dump(self.config, f, indent=4)

            self.main_window.applyStyle()

            self.setCursor(Qt.ArrowCursor)

            print("Configurações salvas com sucesso!")
        except Exception as e:
            print(f"ERRO ao salvar configurações: {e}")

    def resetInputs(self, sidemenu, normal, input, title, subtitle):
        sidemenu.setValue(12)
        normal.setValue(12)
        input.setValue(12)
        title.setValue(20)
        subtitle.setValue(16)

    def resetColors(self):
        self.primary_color_input.setText("#0A54C3")
        self.primary_color_input.currentColor = self.primary_color_input.text()
        self.primary_color_input.editingFinished.emit()
        
        self.primary_color_hover_input.setText("#0847A4")
        self.primary_color_hover_input.currentColor = self.primary_color_hover_input.text()
        self.primary_color_hover_input.editingFinished.emit()
        
        self.secondary_color_input.setText("#EA7712")
        self.secondary_color_input.currentColor = self.secondary_color_input.text()
        self.secondary_color_input.editingFinished.emit()
        
        self.secondary_color_hover_input.setText("#C9650D")
        self.secondary_color_hover_input.currentColor = self.secondary_color_hover_input.text()
        self.secondary_color_hover_input.editingFinished.emit()