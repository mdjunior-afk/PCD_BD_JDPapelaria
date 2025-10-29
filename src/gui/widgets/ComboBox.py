from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QColor, QIcon

from ..config import *

class ComboBox(QComboBox):
    def __init__(self, items = [], has_menu=False):
        super().__init__()

        self.addItems(items)

        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        if has_menu:
            self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.customContextMenuRequested.connect(self.contextMenu)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setColor(QColor(0, 0, 0, 25))
        self.shadow.setOffset(4, 4)

        self.setGraphicsEffect(self.shadow)

        self.setStyle()

    def contextMenu(self, point):
        menu = QMenu(self)

        menu.setStyleSheet(f"""
        QMenu {{
            background-color: {GROUP_BOX_BG_COLOR};
            border: 1px solid lightgray;
            color: {TEXT_COLOR};
            font-size: 14px;
        }}
                           
        QMenu::item {{
            padding: 3px 12px;
        }}
                           
        QMenu::item:selected {{
            background-color: {BTN_HOVER_BACKGROUND_COLOR};
            color: {BTN_HOVER_TEXT_COLOR};
        }}
                           
        QMenu::icon {{
            padding: 0 6px;
        }}
        """)

        menu.addAction(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "Adicionar")
        menu.addAction(self.style().standardIcon(QStyle.SP_FileDialogContentsView), "Editar")

        menu.exec(self.mapToGlobal(point))

    def setStyle(self):
        style = f"""
        QComboBox {{
            background-color: {BTN_TEXT_COLOR};
            padding: 8px;
            border-radius: 8px;
            outline: none;
            box-shadow: none;
        }}

        QComboBox::drop-down {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background-color: {BTN_BACKGROUND_COLOR};
        }}

        QComboBox:down-arrow {{
            image: url(src/gui/icons/caret-down.svg);
            width: 10px;
            height: 10px;
        }}
        """

        self.setStyleSheet(style)