from PySide6.QtWidgets import *

from src.gui.widgets import *
from src.gui.utils import *
from src.gui.colors import *

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

        brand_name_input = LineEdit(placeholder="Digite o nome da marca")

        buttons_widget, buttons = createTableButtons()

        brand_table = Table(["ID", "Nome", "Produtos"])

        brand_box_layout.addWidget(brand_name_label, 0, 0)

        brand_box_layout.addWidget(brand_name_input, 1, 0)
        brand_box_layout.addWidget(buttons_widget, 1, 1)

        brand_box_layout.addWidget(brand_table, 2, 0, 1, 2)

        brand_box_layout.setColumnStretch(0, 3)
        brand_box_layout.setColumnStretch(1, 1)

        category_box = GroupBox("Informações de categoria")
        category_box_layout = QGridLayout()
        category_box.setLayout(category_box_layout)

        category_name_label = Label("Categoria", type="InputLabel")

        category_name_input = LineEdit(placeholder="Digite o nome da categoria")

        buttons_widget, buttons = createTableButtons()

        category_table = Table(["ID", "Nome", "Produtos"])

        category_box_layout.addWidget(category_name_label, 0, 0)

        category_box_layout.addWidget(category_name_input, 1, 0)
        category_box_layout.addWidget(buttons_widget, 1, 1)

        category_box_layout.addWidget(category_table, 2, 0, 1, 2)

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

        name_label = Label("Nome de serviço", type="InputLabel")
        description_label = Label("Descrição", type="InputLabel")
        price_label = Label("Preço", type="InputLabel")

        name_input = LineEdit(placeholder="Digite o nome do serviço")
        description_input = LineEdit(placeholder="Adicione uma descrição para o serviço (Opcional)")
        price_input = DoubleSpinBox()
        price_input.setPrefix("R$ ")

        buttons_widget, buttons = createTableButtons()

        table = Table(["ID", "Tipo", "Preço", "Descrição"])

        info_box_layout.addWidget(name_label, 0, 0)
        info_box_layout.addWidget(price_label, 0, 1)
        info_box_layout.addWidget(description_label, 2, 0)

        info_box_layout.addWidget(name_input, 1, 0)
        info_box_layout.addWidget(price_input, 1, 1)
        info_box_layout.addWidget(description_input, 3, 0)
        info_box_layout.addWidget(buttons_widget, 3, 1)

        info_box_layout.addWidget(table, 4, 0, 1, 2)

        info_box_layout.setColumnStretch(0, 3)
        info_box_layout.setColumnStretch(1, 1)

        layout.addWidget(info_box)

        return widget

    def createPaymentTab(self):
        widget = TabWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 12, 20, 12)
        widget.setLayout(layout)

        info_box = GroupBox("Configurações de pagamentos")
        info_box_layout = QGridLayout()
        info_box.setLayout(info_box_layout)

        payment_method_label = Label("Forma de pagamento", type="InputLabel")

        payment_method_input = LineEdit(placeholder="Digite o nome da forma de pagamento")

        buttons_widget, buttons = createTableButtons()

        table = Table(["ID", "Tipo", "Preço", "Descrição"])

        info_box_layout.addWidget(payment_method_label, 0, 0)

        info_box_layout.addWidget(payment_method_input, 1, 0)
        info_box_layout.addWidget(buttons_widget, 1, 1)

        info_box_layout.addWidget(table, 2, 0, 1, 2)

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

        light_radio = QRadioButton("Claro")
        light_radio.setChecked(True)
        dark_radio = QRadioButton("Escuro")

        theme_box_layout.addWidget(light_radio)
        theme_box_layout.addWidget(dark_radio)
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
        secondary_color_label = Label("Cor secundária", type="InputLabel")

        self.primary_color_input = ColorLineEdit(initial_color=PRIMARY_COLOR, parent=self)
        self.secondary_color_input = ColorLineEdit(initial_color=SECONDARY_COLOR, parent=self)

        colors_box_layout.addWidget(primary_color_label, 0, 0)
        colors_box_layout.addWidget(secondary_color_label, 0, 1)

        colors_box_layout.addWidget(self.primary_color_input, 1, 0)
        colors_box_layout.addWidget(self.secondary_color_input, 1, 1)

        options_box_layout.addWidget(fonts_box)
        options_box_layout.addWidget(colors_box)
        options_box_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        apply_button = PushButton("Salvar", icon_path="disk.svg")

        apply_button.clicked.connect(self.saveConfig)

        layout.addWidget(theme_box)
        layout.addWidget(options_box)
        layout.addWidget(apply_button)

        return widget
    
    def saveConfig(self):
        try:
            with open("src/configuration.json", "w") as f:
                json.dump(self.config, f, indent=4)

            self.main_window.applyStyle()

            print("Configurações salvas com sucesso!")
        except Exception as e:
            print(f"ERRO ao salvar configurações: {e}")