"""
Calendar widget
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QLabel
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QFont


class CalendarWidget(QWidget):
    """Calendar widget that displays the current month"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()

        # Calendar title
        self.title_label = QLabel("달력")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont('Ubuntu', 14, QFont.Bold)
        self.title_label.setFont(title_font)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setFirstDayOfWeek(Qt.Sunday)

        # Set to current date
        self.calendar.setSelectedDate(QDate.currentDate())

        # Current date info label
        self.date_info_label = QLabel()
        self.date_info_label.setAlignment(Qt.AlignCenter)
        info_font = QFont('Ubuntu', 11)
        self.date_info_label.setFont(info_font)
        self.update_date_info()

        # Connect signal
        self.calendar.selectionChanged.connect(self.update_date_info)

        layout.addWidget(self.title_label)
        layout.addWidget(self.calendar)
        layout.addWidget(self.date_info_label)

        self.setLayout(layout)

    def update_date_info(self):
        """Update the date information label"""
        selected_date = self.calendar.selectedDate()

        # Get day name in Korean
        day_names = {
            1: '월요일',
            2: '화요일',
            3: '수요일',
            4: '목요일',
            5: '금요일',
            6: '토요일',
            7: '일요일'
        }

        day_name = day_names.get(selected_date.dayOfWeek(), '')
        date_str = f"{selected_date.year()}년 {selected_date.month()}월 {selected_date.day()}일 {day_name}"

        self.date_info_label.setText(date_str)

    def start_timer(self):
        """Start the timer to update the calendar date daily"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_date)
        # Update every minute (60000 ms) to check if date changed
        self.timer.start(60000)

    def update_current_date(self):
        """Update the calendar to show current date if it has changed"""
        current_date = QDate.currentDate()
        selected_date = self.calendar.selectedDate()

        # Only update if the selected date is not today
        # This allows users to browse other dates without auto-jumping back
        if selected_date != current_date:
            # Check if we're looking at today's month/year
            if (selected_date.year() == current_date.year() and
                selected_date.month() == current_date.month()):
                # If viewing current month, update to current date
                self.calendar.setSelectedDate(current_date)
