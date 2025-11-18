"""
Weather widget
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
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
        temp_font = QFont('Ubuntu', 24, QFont.Bold)
        self.temp_label.setFont(temp_font)

        self.desc_label = QLabel("Loading weather...")
        desc_font = QFont('Ubuntu', 11)
        self.desc_label.setFont(desc_font)

        temp_desc_layout.addWidget(self.temp_label)
        temp_desc_layout.addWidget(self.desc_label)
        temp_desc_layout.addStretch()

        # Additional info in one line
        info_layout = QHBoxLayout()

        info_font = QFont('Ubuntu', 9)

        self.humidity_label = QLabel("Humidity: --%")
        self.humidity_label.setFont(info_font)

        self.air_quality_label = QLabel("PM2.5: --")
        self.air_quality_label.setFont(info_font)

        self.location_label = QLabel(f"{self.location['city']}")
        self.location_label.setFont(info_font)

        info_layout.addWidget(self.humidity_label)
        info_layout.addWidget(self.air_quality_label)
        info_layout.addWidget(self.location_label)
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

            # Update location with detected city
            self.location_label.setText(self.location['city'])

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
