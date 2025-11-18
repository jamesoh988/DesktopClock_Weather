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
        self.title_label = QLabel("Calendar")
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

        # Get day name in English
        day_names = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        }

        # Get month name in English
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }

        day_name = day_names.get(selected_date.dayOfWeek(), '')
        month_name = month_names.get(selected_date.month(), '')
        date_str = f"{month_name} {selected_date.day()}, {selected_date.year()} {day_name}"

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
