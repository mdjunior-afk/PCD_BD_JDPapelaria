from PySide6.QtWidgets import QDateEdit, QGraphicsDropShadowEffect, QAbstractSpinBox
from PySide6.QtGui import QFontMetrics, QColor
from PySide6.QtCore import QDate
import os

class DateEdit(QDateEdit):
    def __init__(self, border_radius=8, text_color="#747474", icon_path="", background_color="#EFEFEF", hover="#EA7712"):
        super().__init__()

        self.setFixedHeight(36)

        self.background_color = background_color
        self.border_radius = border_radius
        self.text_color = text_color
        self.icon_path = icon_path
        self.hover = hover

        self.setDate(QDate.currentDate())

        self.setCalendarPopup(True)

        self.setStyle()

    def setStyle(self):
        style = f"""
        QDateEdit {{
            background-color: transparent !important;
            border: 1px solid lightgray;
            border-radius: 4px;
            color: {self.text_color};
            font-size: 12px;
            padding: 8px;
        }}

        QCalendarWidget QToolButton {{
            color: white;
            font-size: 12px;
            icon-size: 24px 24px;
            background-color: {self.text_color};
        }}
        
        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background-color: {self.text_color};
        }}

        QDateEdit::drop-down {{
            image: url(src/gui/icons/calendar.svg);
            padding-right: 8px;
            subcontrol-origin: margin;
            subcontrol-position: right center;
            width: 20px;
            height: 20px;
            right: 5px;
            border: none;
        }}
        
        QCalendarWidget QMenu {{
            left:20px;
            color: white;
            font-size: 12px;
            background-color: {self.text_color};
        }}
        
        QCalendarWidget QWidget {{
            alternate-background-color: {self.background_color};
        }}

        QCalendarWidget QAbstractItemView::item:hover {{
            color: {self.text_color};
            border: 2px solid {self.hover};
        }}

        QCalendarWidget QAbstractItemView:enabled {{
            font-size:12px;
            color: {self.text_color};
            background-color: #FFFFFF;    
            selection-background-color: {self.hover};
            selection-color: white;
        }}
        """
        self.setStyleSheet(style)

    
