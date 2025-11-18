"""
Weather widget
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty
from PyQt5.QtGui import QFont, QCursor
from src.services.free_weather_service import FreeWeatherService
from src.services.location_service import LocationService
import config


class WeatherWidget(QWidget):
    """Weather widget that displays current weather and air quality"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.weather_service = FreeWeatherService()

        # Detect location based on IP
        self.location = LocationService.detect_location()
        print(f"Detected location: {self.location['city']}, {self.location['country']}")

        # Temperature unit toggle
        self.current_temp_celsius = 0.0
        self.is_fahrenheit = False

        # Animation objects (keep reference to prevent garbage collection)
        self.slide_out_anim = None
        self.slide_in_anim = None
        self.temp_label_original_pos = None

        self.init_ui()
        self.start_timer()
        self.update_weather()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        # Weather icon
        self.icon_label = QLabel("🌡️")
        icon_font = QFont('Ubuntu', 32)
        self.icon_label.setFont(icon_font)
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Main info layout
        main_info_layout = QVBoxLayout()

        # Temperature and description in one line
        temp_desc_layout = QHBoxLayout()

        self.temp_label = QLabel("--°C")
        temp_font = QFont('Ubuntu', 20, QFont.Bold)
        self.temp_label.setFont(temp_font)
        self.temp_label.setMinimumWidth(190)
        self.temp_label.setMaximumWidth(190)
        self.temp_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.temp_label.setStyleSheet("outline: none; border: none;")
        self.temp_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.temp_label.mousePressEvent = self.toggle_temperature_unit

        self.desc_label = QLabel("Loading weather...")
        desc_font = QFont('Ubuntu', 11)
        self.desc_label.setFont(desc_font)
        self.desc_label.setStyleSheet("outline: none; border: none;")

        self.country_label = QLabel(f"{self.location['country']}")
        country_font = QFont('Ubuntu', 10, QFont.Bold)
        self.country_label.setFont(country_font)
        self.country_label.setStyleSheet("outline: none; border: none;")

        temp_desc_layout.addWidget(self.temp_label)
        temp_desc_layout.addWidget(self.desc_label)
        temp_desc_layout.addWidget(self.country_label)
        temp_desc_layout.addStretch()

        # Additional info in one line
        info_layout = QHBoxLayout()

        info_font = QFont('Ubuntu', 9)

        self.humidity_label = QLabel("Humidity: --%")
        self.humidity_label.setFont(info_font)

        self.air_quality_label = QLabel("PM2.5: --")
        self.air_quality_label.setFont(info_font)

        self.city_label = QLabel(f"{self.location['city']}")
        self.city_label.setFont(info_font)

        info_layout.addWidget(self.humidity_label)
        info_layout.addWidget(self.air_quality_label)
        info_layout.addWidget(self.city_label)
        info_layout.addStretch()

        main_info_layout.addLayout(temp_desc_layout)
        main_info_layout.addLayout(info_layout)

        layout.addWidget(self.icon_label)
        layout.addLayout(main_info_layout)
        layout.addStretch()

        self.setLayout(layout)

        # Set maximum height to keep it compact
        self.setMaximumHeight(100)
        self.setMinimumHeight(90)

    def showEvent(self, event):
        """Save original position after widget is shown"""
        super().showEvent(event)
        if self.temp_label_original_pos is None:
            self.temp_label_original_pos = self.temp_label.pos()

    def start_timer(self):
        """Start the timer to update weather periodically"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(config.WEATHER_UPDATE_INTERVAL)  # Update every 10 minutes

    def update_weather(self):
        """Update weather information"""
        # Get weather data using detected location
        weather_data = self.weather_service.get_weather(
            lat=self.location['latitude'],
            lon=self.location['longitude']
        )

        if weather_data and 'current' in weather_data:
            current = weather_data['current']

            # Update temperature
            temp = current.get('temperature_2m', 0)
            self.current_temp_celsius = temp

            # Display in current unit
            if self.is_fahrenheit:
                temp_f = (temp * 9/5) + 32
                self.temp_label.setText(f"{temp_f:.1f}°F")
            else:
                self.temp_label.setText(f"{temp:.1f}°C")

            # Update weather icon and description
            weather_code = current.get('weather_code', 0)
            icon = self.weather_service.get_weather_icon(weather_code)
            desc = self.weather_service.get_weather_description(weather_code)

            self.icon_label.setText(icon)
            self.desc_label.setText(desc)

            # Update humidity
            humidity = current.get('relative_humidity_2m', 0)
            self.humidity_label.setText(f"Humidity: {humidity}%")

            # Update location with detected country and city
            self.country_label.setText(self.location['country'])
            self.city_label.setText(self.location['city'])

            # Get air quality data
            self.update_air_quality()
        else:
            self.desc_label.setText("No weather data")

    def update_air_quality(self):
        """Update air quality information"""
        air_data = self.weather_service.get_air_quality(
            self.location['latitude'],
            self.location['longitude']
        )

        if air_data and 'current' in air_data:
            current = air_data['current']
            pm25 = current.get('pm2_5', 0)
            aqi_desc = self.weather_service.get_pm25_description(pm25)

            self.air_quality_label.setText(f"PM2.5: {aqi_desc}")
        else:
            self.air_quality_label.setText("PM2.5: --")

    def toggle_temperature_unit(self, event):
        """Toggle between Celsius and Fahrenheit with rotation animation"""
        if event.button() == Qt.LeftButton:
            # Save original position if not yet saved
            if self.temp_label_original_pos is None:
                self.temp_label_original_pos = self.temp_label.pos()

            # Animate slide out downward (current temperature slides down and disappears)
            self.slide_out_anim = QPropertyAnimation(self.temp_label, b"pos")
            self.slide_out_anim.setDuration(250)
            self.slide_out_anim.setStartValue(self.temp_label_original_pos)
            self.slide_out_anim.setEndValue(QPoint(self.temp_label_original_pos.x(), self.temp_label_original_pos.y() + 80))
            self.slide_out_anim.setEasingCurve(QEasingCurve.InCubic)

            # Connect to switch unit after slide out
            self.slide_out_anim.finished.connect(self.switch_temperature_display)

            # Start slide out animation
            self.slide_out_anim.start()

    def switch_temperature_display(self):
        """Switch temperature unit and slide in from top (rotation effect)"""
        # Toggle unit
        self.is_fahrenheit = not self.is_fahrenheit

        # Update text with new unit
        if self.is_fahrenheit:
            temp_f = (self.current_temp_celsius * 9/5) + 32
            self.temp_label.setText(f"{temp_f:.1f}°F")
        else:
            self.temp_label.setText(f"{self.current_temp_celsius:.1f}°C")

        # Move label above its normal position (start from top)
        self.temp_label.move(self.temp_label_original_pos.x(), self.temp_label_original_pos.y() - 80)

        # Animate slide in downward (new temperature slides down from top to original position)
        self.slide_in_anim = QPropertyAnimation(self.temp_label, b"pos")
        self.slide_in_anim.setDuration(250)
        self.slide_in_anim.setStartValue(self.temp_label.pos())
        self.slide_in_anim.setEndValue(self.temp_label_original_pos)
        self.slide_in_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Start slide in animation
        self.slide_in_anim.start()
