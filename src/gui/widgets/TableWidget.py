from PySide6.QtWidgets import *
from PySide6.QtGui import QColor

from ..config import *

class TableWidget(QTableWidget):
    def __init__(self, columns=[], name="Produto"):
        super().__init__()
        
        self.columns = columns
        self.name = name

        self.setStyle()
        self.config()
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.setGraphicsEffect(self.shadow)

        """for i in range(10):
            self.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.setItem(i, 1, QTableWidgetItem(f"{name} {i + 1}"))
            self.setItem(i, 2, QTableWidgetItem(str(20 + i)))
            self.setItem(i, 3, QTableWidgetItem("100,00"))
            self.setItem(i, 4, QTableWidgetItem(f"Categoria 1"))"""

    def config(self):
        self.setAlternatingRowColors(True)
        
        self.setColumnCount(len(self.columns))
        self.setRowCount(0)
        
        self.verticalHeader().hide()
        
        self.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.setHorizontalHeaderLabels(self.columns)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def setStyle(self):
        style = f"""
        QTableWidget {{
            alternate-background-color: #F0F0F0;
            background-color: #FFFFFF;
            gridline-color: #C0C0C0;
            border: none;
            color: #747474;
            font-size: 12px;
        }}                         

        QHeaderView::section {{
            background-color: {PRIMARY_COLOR};
            color: white;
            font-size: 14px;
            border: 1px solid #C0C0C0;

            padding: 2px;
            border-top: 0px;
            border-left: 0px;
            subcontrol-origin: padding;                           
        }}                        
                                         
        QTableWidget::item:selected {{
            background-color: #E98A37;                             
        }}
                                         
        /* Estilo para a barra de rolagem vertical */
        QScrollBar:vertical {{
            border: none;
            background: #F0F0F0; /* Cor de fundo da barra de rolagem */
            width: 5px; /* Largura da barra de rolagem */
            margin: 0px;
            border-radius: 5px; /* Adicionado aqui */
        }}

        /* Estilo para o controle deslizante (handle) */
        QScrollBar::handle:vertical {{
            background: #A0A0A0; /* Cor do controle deslizante */
            min-height: 20px;
            border-radius: 2px; /* Borda arredondada */
        }}

        /* Estilo para o controle deslizante quando o mouse está sobre ele */
        QScrollBar::handle:vertical:hover {{
            background: #808080; /* Cor ao passar o mouse */
        }}

        /* Estilo dos botões de setas (ocultos ou customizados) */
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        /* Estilo da área de rolagem */
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        """

        self.setStyleSheet(style)