"""
Analog clock widget
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QTime, Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QFont
import math


class AnalogClock(QWidget):
    """Analog clock widget that displays time with clock hands"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scale = 1.0
        self.base_size = 200
        self.setMinimumSize(150, 150)
        self.start_timer()

    def start_timer(self):
        """Start the timer to update the clock"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Update every second

    def paintEvent(self, event):
        """Paint the analog clock"""
        from datetime import datetime

        current_time = datetime.now()
        hour = current_time.hour % 12
        minute = current_time.minute
        second = current_time.second

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Get the widget size
        side = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 250.0, side / 250.0)

        # Determine colors based on theme
        # We'll use a simple check of the background to determine if it's dark or light
        bg_color = self.palette().window().color()
        is_dark = bg_color.lightness() < 128

        if is_dark:
            clock_color = QColor(255, 255, 255)
            hand_color = QColor(255, 255, 255)
            second_hand_color = QColor(255, 100, 100)
        else:
            clock_color = QColor(0, 0, 0)
            hand_color = QColor(0, 0, 0)
            second_hand_color = QColor(200, 50, 50)

        # Draw clock face border
        painter.setPen(QPen(clock_color, 3))
        painter.drawEllipse(-100, -100, 200, 200)

        # Draw hour markers
        painter.setPen(QPen(clock_color, 2))
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = int(85 * math.cos(angle))
            y1 = int(85 * math.sin(angle))
            x2 = int(95 * math.cos(angle))
            y2 = int(95 * math.sin(angle))
            painter.drawLine(x1, y1, x2, y2)

        # Draw minute markers
        painter.setPen(QPen(clock_color, 1))
        for i in range(60):
            if i % 5 != 0:  # Skip hour markers
                angle = math.radians(i * 6 - 90)
                x1 = int(90 * math.cos(angle))
                y1 = int(90 * math.sin(angle))
                x2 = int(95 * math.cos(angle))
                y2 = int(95 * math.sin(angle))
                painter.drawLine(x1, y1, x2, y2)

        # Draw hour hand
        hour_angle = math.radians((hour * 30 + minute * 0.5) - 90)
        hour_x = int(50 * math.cos(hour_angle))
        hour_y = int(50 * math.sin(hour_angle))
        painter.setPen(QPen(hand_color, 6, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(0, 0, hour_x, hour_y)

        # Draw minute hand
        minute_angle = math.radians((minute * 6 + second * 0.1) - 90)
        minute_x = int(70 * math.cos(minute_angle))
        minute_y = int(70 * math.sin(minute_angle))
        painter.setPen(QPen(hand_color, 4, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(0, 0, minute_x, minute_y)

        # Draw second hand
        second_angle = math.radians(second * 6 - 90)
        second_x = int(80 * math.cos(second_angle))
        second_y = int(80 * math.sin(second_angle))
        painter.setPen(QPen(second_hand_color, 2, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(0, 0, second_x, second_y)

        # Draw center dot
        painter.setPen(QPen(hand_color, 1))
        painter.setBrush(hand_color)
        painter.drawEllipse(-5, -5, 10, 10)

        # Reset transformation to draw digital time in widget coordinates
        painter.resetTransform()

        # Draw digital time below the clock (centered)
        painter.setPen(QPen(clock_color, 1))
        font = QFont('Ubuntu', 10)
        painter.setFont(font)
        time_str = current_time.strftime('%H:%M:%S')

        # Calculate text width for centering
        fm = painter.fontMetrics()
        text_width = fm.horizontalAdvance(time_str)

        # Position text below the clock circle with 30px gap
        # Calculate the bottom of the clock circle
        clock_bottom = (self.height() / 2) + (side / 2) + 30

        # Draw text centered horizontally, below the clock
        painter.drawText(int(self.width() / 2 - text_width / 2), int(clock_bottom), time_str)

    def set_scale(self, scale):
        """Set the scale factor for the clock"""
        self.scale = scale
        self.update()

    def sizeHint(self):
        """Provide size hint for layout"""
        from PyQt5.QtCore import QSize
        return QSize(400, 400)
