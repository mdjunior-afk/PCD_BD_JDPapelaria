from PySide6.QtWidgets import QGroupBox, QVBoxLayout

class GroupBox(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        
        # 1. Aplicar a Folha de Estilo (QSS)
        self.setStyleSheet("""
            /* Estilo da moldura principal do GroupBox */
            QGroupBox {
                background-color: #f7f9fc; /* Cor de fundo suave (cinza claro/azul) */
                border: 2px solid #a9b9cf; /* Borda sutil */
                border-radius: 8px; /* Cantos arredondados */
                margin-top: 20px; /* Espaço para o título não ser cortado */
            }

            /* Estilo do título */
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left; /* Posição do título */
                padding: 0 10px; /* Espaço interno ao redor do título */
                background-color: #4a6fa5; /* Cor de fundo do título (Azul marinho) */
                color: white; /* Cor do texto do título */
                border-radius: 5px; /* Cantos arredondados para a caixa do título */
            }
        """)

        # 2. Configurar o layout interno (exemplo com QVBoxLayout)
        # O layout interno será o responsável por organizar os widgets DENTRO do GroupBox
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)