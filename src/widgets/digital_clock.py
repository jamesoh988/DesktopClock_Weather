"""
Digital clock widget
"""
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont


class DigitalClock(QWidget):
    """Digital clock widget that displays time in digital format"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scale = 1.0
        self.base_time_font_size = 32
        self.base_date_font_size = 16
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Time label
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setWordWrap(True)
        self.time_font = QFont('Ubuntu Mono', self.base_time_font_size, QFont.Bold)
        self.time_label.setFont(self.time_font)

        # Date label
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setWordWrap(True)
        self.date_font = QFont('Ubuntu', self.base_date_font_size)
        self.date_label.setFont(self.date_font)

        layout.addStretch(5)
        layout.addWidget(self.time_label, 5)
        layout.addWidget(self.date_label, 5)
        layout.addStretch(5)

        self.setLayout(layout)
        self.update_time()

    def start_timer(self):
        """Start the timer to update the clock"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        """Update the displayed time"""
        from datetime import datetime

        current_time = datetime.now()

        # Format time as HH:MM:SS
        time_str = current_time.strftime('%H:%M:%S')
        self.time_label.setText(time_str)

        # Format date
        date_str = current_time.strftime('%Y년 %m월 %d일 %A')
        # Translate day names to Korean
        day_names = {
            'Monday': '월요일',
            'Tuesday': '화요일',
            'Wednesday': '수요일',
            'Thursday': '목요일',
            'Friday': '금요일',
            'Saturday': '토요일',
            'Sunday': '일요일'
        }
        for eng, kor in day_names.items():
            date_str = date_str.replace(eng, kor)

        self.date_label.setText(date_str)

    def set_scale(self, scale):
        """Set the scale factor for the clock"""
        self.scale = scale
        # Update font sizes
        self.time_font.setPointSize(int(self.base_time_font_size * scale))
        self.date_font.setPointSize(int(self.base_date_font_size * scale))
        self.time_label.setFont(self.time_font)
        self.date_label.setFont(self.date_font)

    def resizeEvent(self, event):
        """Handle resize event to scale font based on widget size"""
        super().resizeEvent(event)
        # Calculate scale based on widget width
        width = self.width()
        if width > 0:
            # Scale font size based on width (baseline 500px = 1.0 scale)
            scale = width / 500.0
            scale = max(0.6, min(scale, 2.5))  # Limit between 0.6x and 2.5x
            self.set_scale(scale)
