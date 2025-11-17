"""
Dark theme stylesheet for the application
"""

DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Ubuntu', 'Segoe UI', Arial, sans-serif;
}

QPushButton {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3d3d3d;
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #3d3d3d;
    border: 1px solid #4d4d4d;
}

QPushButton:pressed {
    background-color: #252525;
}

QLabel {
    background-color: transparent;
    color: #ffffff;
}

QFrame {
    background-color: #2d2d2d;
    border-radius: 8px;
    border: 1px solid #3d3d3d;
}

QCalendarWidget {
    background-color: #2d2d2d;
    color: #ffffff;
}

QCalendarWidget QToolButton {
    background-color: #2d2d2d;
    color: #ffffff;
    border: none;
    border-radius: 3px;
    padding: 5px;
}

QCalendarWidget QToolButton:hover {
    background-color: #3d3d3d;
}

QCalendarWidget QMenu {
    background-color: #2d2d2d;
    color: #ffffff;
}

QCalendarWidget QSpinBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3d3d3d;
    border-radius: 3px;
}

QCalendarWidget QAbstractItemView {
    background-color: #2d2d2d;
    color: #ffffff;
    selection-background-color: #0078d4;
    selection-color: #ffffff;
}

QCalendarWidget QAbstractItemView:enabled {
    color: #ffffff;
}

QCalendarWidget QAbstractItemView:disabled {
    color: #808080;
}

/* Calendar header (days of week) */
QCalendarWidget QWidget {
    alternate-background-color: #2d2d2d;
}

QCalendarWidget QAbstractItemView:enabled {
    color: #ffffff;
    background-color: #2d2d2d;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #2d2d2d;
}

QCalendarWidget QTableView {
    background-color: #2d2d2d;
    color: #ffffff;
}

/* Days of week header */
QCalendarWidget QHeaderView::section {
    background-color: #3d3d3d;
    color: #ffffff;
    padding: 5px;
    border: 1px solid #4d4d4d;
    font-weight: bold;
}
"""
