from PySide6.QtWidgets import *
from PySide6.QtCore import QLocale

class SpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

        self.setMaximum(99999)
        self.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()

        self.setMaximum(99999)
        self.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))