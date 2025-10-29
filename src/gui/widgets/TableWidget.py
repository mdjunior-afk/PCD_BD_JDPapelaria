from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ..config import *

class TableWidget(QTableWidget):
    def __init__(self, columns=[]):
        super().__init__()

        self.setMinimumHeight(150)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: #f4f6fb;
            }}
            QTableWidget {{
                background-color: transparent !important;
                border-radius: 10px;
                gridline-color: #e0e4ec;
                selection-background-color: #e8f0fe;
                font-size: 12px;
                padding: 0;
                margin: 0;
            }}
            QHeaderView::section {{
                background-color: {CONTENT_COLOR};
                font-size: 12px;
                border: none;
                padding: 8px;
                font-weight: 600;
                color: #555;
            }}

            QTableWidget::item:selected {{
                background-color: {PRIMARY_COLOR};
            }}

            QHeaderView::section:first {{
                border-top-left-radius: 8px;
                border-bottom-left-radius: 8px;
            }}

            QHeaderView::section:last {{
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
            QPushButton {{
                background-color: #eef4ff;
                border: 1px solid #d0d9ff;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: #dce6ff;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)

        self.table = QTableWidget()
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(i)
            if item:
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Dados de exemplo

        self.table.setRowCount(3)
        for row in range(3):
            self.table.setItem(row, 0, QTableWidgetItem(f"{row}"))
            self.table.setItem(row, 1, QTableWidgetItem(f"Item {row}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{row+2}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"100,00"))
            self.table.setItem(row, 4, QTableWidgetItem(f"Categoria 1"))

        layout.addWidget(self.table)
