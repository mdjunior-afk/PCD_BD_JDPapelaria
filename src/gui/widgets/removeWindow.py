from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class RemoveDialog(QDialog):
    """Dialog genérico para confirmar remoção de items."""
    
    def __init__(self, parent=None, title="Confirmar Remoção", item_name=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout()
        
        # Ícone de aviso e mensagem
        message_layout = QHBoxLayout()
        label_icon = QLabel("⚠️")
        label_icon.setStyleSheet("font-size: 28px;")
        
        message_text = QLabel(f"Tem certeza que deseja remover?\n\n{item_name}")
        message_text.setWordWrap(True)
        
        message_layout.addWidget(label_icon)
        message_layout.addWidget(message_text)
        layout.addLayout(message_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        
        btn_remove = QPushButton("Remover")
        btn_remove.setStyleSheet("background-color: #d32f2f; color: white;")
        btn_remove.clicked.connect(self.accept)
        
        buttons_layout.addWidget(btn_cancel)
        buttons_layout.addWidget(btn_remove)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)


class MessageDialog(QDialog):
    """Dialog genérico para mostrar mensagens com ícones diferentes."""
    
    # Tipos de mensagem
    INFO = "ℹ️"
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    
    def __init__(self, parent=None, title="Mensagem", message="", msg_type=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout()
        
        # Ícone e mensagem
        message_layout = QHBoxLayout()
        
        icon = msg_type if msg_type else self.INFO
        label_icon = QLabel(icon)
        label_icon.setStyleSheet("font-size: 28px;")
        label_icon.setMinimumWidth(50)
        
        message_text = QLabel(message)
        message_text.setWordWrap(True)
        
        message_layout.addWidget(label_icon)
        message_layout.addWidget(message_text)
        layout.addLayout(message_layout)
        
        # Botão OK
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)
        
        self.setLayout(layout)
