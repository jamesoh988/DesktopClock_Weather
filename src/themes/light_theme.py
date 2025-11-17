"""
Light theme stylesheet for the application
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f5;
    color: #000000;
}

QWidget {
    background-color: #f5f5f5;
    color: #000000;
    font-family: 'Ubuntu', 'Segoe UI', Arial, sans-serif;
}

QPushButton {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #d0d0d0;
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #e8e8e8;
    border: 1px solid #c0c0c0;
}

QPushButton:pressed {
    background-color: #d8d8d8;
}

QLabel {
    background-color: transparent;
    color: #000000;
}

QFrame {
    background-color: #ffffff;
    border-radius: 8px;
    border: 1px solid #d0d0d0;
}

QCalendarWidget {
    background-color: #ffffff;
    color: #000000;
}

QCalendarWidget QToolButton {
    background-color: #ffffff;
    color: #000000;
    border: none;
    border-radius: 3px;
    padding: 5px;
}

QCalendarWidget QToolButton:hover {
    background-color: #e8e8e8;
}

QCalendarWidget QMenu {
    background-color: #ffffff;
    color: #000000;
}

QCalendarWidget QSpinBox {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #d0d0d0;
    border-radius: 3px;
}

QCalendarWidget QAbstractItemView {
    background-color: #ffffff;
    color: #000000;
    selection-background-color: #0078d4;
    selection-color: #ffffff;
}

QCalendarWidget QAbstractItemView:enabled {
    color: #000000;
}

QCalendarWidget QAbstractItemView:disabled {
    color: #808080;
}
"""
