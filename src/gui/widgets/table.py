from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from src.gui.colors import *

class Table(QTableWidget):
    def __init__(self, columns=[]):
        super().__init__()

        self.setMinimumHeight(150)

        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        # Table configuration
        self.setFocusPolicy(Qt.NoFocus)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.columnCount()):
            item = self.horizontalHeaderItem(i)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        #self.setRowCount(10)

        for i in range(self.rowCount()):
            self.setItem(i, 0, QTableWidgetItem(f"{i}"))
            self.setItem(i, 1, QTableWidgetItem(f"{i}"))
            self.setItem(i, 2, QTableWidgetItem(f"{i}"))
            self.setItem(i, 3, QTableWidgetItem(f"{i}"))
            self.setItem(i, 4, QTableWidgetItem(f"{i}"))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

    def contextMenu(self, point):
        menu = QMenu(self)

        menu.setStyleSheet(
        f"""
        QMenu {{
            background-color: {CONTENT_COLOR};
            color: {TEXT_COLOR};
        }}
        
        QMenu::item:selected {{
            background-color: {BTN_HOVER_BACKGROUND_COLOR};
            color: {BTN_HOVER_TEXT_COLOR};
        }}
        """)

        menu.addAction(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "Adicionar")
        menu.addAction(self.style().standardIcon(QStyle.SP_FileDialogContentsView), "Editar")
        menu.addAction(self.style().standardIcon(QStyle.SP_TrashIcon), "Remover")

        menu.exec(self.mapToGlobal(point))

    def setStyle(self, config):
        _style = f"""
        QWidget {{
            background-color: transparent !important;
        }}

        QHeaderView::section {{
            background-color: {CONTENT_COLOR};
        }}

        QTableWidget::item:selected {{
            background-color: {config["PRIMARY_COLOR"]};
        }}
        """

        self.setStyleSheet(_style)