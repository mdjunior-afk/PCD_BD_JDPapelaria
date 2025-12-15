from PySide6.QtWidgets import *
from PySide6.QtCore import QLocale

class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        self.setMaximum(99999)
        self.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))
        
        # Estilo para quando disabled
        self.setStyleSheet("""
            QSpinBox:disabled {
                background-color: #f0f0f0;
                color: #a0a0a0;
                border: 1px solid #d0d0d0;
            }
        """)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()

        self.setMaximum(99999)
        self.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))
        
        # Estilo para quando disabled
        self.setStyleSheet("""
            QDoubleSpinBox:disabled {
                background-color: #f0f0f0;
                color: #a0a0a0;
                border: 1px solid #d0d0d0;
            }
        """)