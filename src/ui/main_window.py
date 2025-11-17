"""
Main window for the Desktop Clock & Weather Application
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFrame, QSizeGrip, QSlider, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from src.widgets.digital_clock import DigitalClock
from src.widgets.analog_clock import AnalogClock
from src.ui.calendar_widget import CalendarWidget
from src.ui.weather_widget import WeatherWidget
from src.themes.dark_theme import DARK_THEME
from src.themes.light_theme import LIGHT_THEME
from src.utils.settings_manager import SettingsManager
import config


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()

        # Load settings
        self.current_theme = self.settings.get('theme', config.DEFAULT_THEME)
        self.clock_mode = self.settings.get('clock.mode', config.DEFAULT_CLOCK_MODE)
        self.clock_scale = self.settings.get('clock.scale', 1.0)

        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(config.APP_NAME)
        self.setMinimumSize(config.MIN_WINDOW_WIDTH, config.MIN_WINDOW_HEIGHT)

        # Load window size from settings
        width = self.settings.get('window.width', config.DEFAULT_WINDOW_WIDTH)
        height = self.settings.get('window.height', config.DEFAULT_WINDOW_HEIGHT)
        self.resize(width, height)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Control buttons layout
        controls_layout = QHBoxLayout()

        # Theme toggle button
        self.theme_button = QPushButton("🌙 다크 모드")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Clock mode toggle button
        button_text = "🔢 디지털" if self.clock_mode == config.CLOCK_MODE_ANALOG else "🕐 아날로그"
        self.clock_mode_button = QPushButton(button_text)
        self.clock_mode_button.clicked.connect(self.toggle_clock_mode)

        controls_layout.addWidget(self.theme_button)
        controls_layout.addWidget(self.clock_mode_button)
        controls_layout.addStretch()

        # Weather widget
        self.weather_frame = QFrame()
        weather_layout = QVBoxLayout()
        self.weather_widget = WeatherWidget()
        weather_layout.addWidget(self.weather_widget)
        self.weather_frame.setLayout(weather_layout)

        # Content layout (weather and calendar side by side)
        content_layout = QHBoxLayout()

        # Clock container with size control
        clock_container = QVBoxLayout()

        # Clock size slider
        size_control_layout = QHBoxLayout()
        size_label = QLabel("크기:")

        self.clock_size_slider = QSlider(Qt.Horizontal)
        self.clock_size_slider.setMinimum(50)
        self.clock_size_slider.setMaximum(200)
        self.clock_size_slider.setValue(int(self.clock_scale * 100))
        self.clock_size_slider.setMaximumWidth(150)
        self.clock_size_slider.valueChanged.connect(self.on_clock_size_changed)

        size_control_layout.addWidget(size_label)
        size_control_layout.addWidget(self.clock_size_slider)
        size_control_layout.addStretch()

        self.clock_frame = QFrame()
        self.clock_layout = QVBoxLayout()
        self.clock_frame.setLayout(self.clock_layout)

        # Initialize clock based on config
        self.digital_clock = DigitalClock()
        self.analog_clock = AnalogClock()

        # Apply saved scale
        self.digital_clock.set_scale(self.clock_scale)
        self.analog_clock.set_scale(self.clock_scale)

        if self.clock_mode == config.CLOCK_MODE_ANALOG:
            self.clock_layout.addWidget(self.analog_clock)
            self.digital_clock.hide()
        else:
            self.clock_layout.addWidget(self.digital_clock)
            self.analog_clock.hide()

        clock_container.addLayout(size_control_layout)
        clock_container.addWidget(self.clock_frame)

        # Calendar widget
        self.calendar_frame = QFrame()
        calendar_layout = QVBoxLayout()
        self.calendar_widget = CalendarWidget()
        calendar_layout.addWidget(self.calendar_widget)
        self.calendar_frame.setLayout(calendar_layout)

        content_layout.addLayout(clock_container)
        content_layout.addWidget(self.calendar_frame)

        # Add all to main layout
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.weather_frame)
        main_layout.addLayout(content_layout)

        central_widget.setLayout(main_layout)

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.current_theme == config.THEME_DARK:
            self.current_theme = config.THEME_LIGHT
            self.theme_button.setText("☀️ 라이트 모드")
        else:
            self.current_theme = config.THEME_DARK
            self.theme_button.setText("🌙 다크 모드")

        self.settings.set('theme', self.current_theme)
        self.apply_theme()

    def toggle_clock_mode(self):
        """Toggle between digital and analog clock"""
        # Remove current clock widget
        if self.clock_mode == config.CLOCK_MODE_DIGITAL:
            self.clock_layout.removeWidget(self.digital_clock)
            self.digital_clock.hide()

            self.clock_layout.addWidget(self.analog_clock)
            self.analog_clock.show()

            self.clock_mode = config.CLOCK_MODE_ANALOG
            self.clock_mode_button.setText("🔢 디지털")
        else:
            self.clock_layout.removeWidget(self.analog_clock)
            self.analog_clock.hide()

            self.clock_layout.addWidget(self.digital_clock)
            self.digital_clock.show()

            self.clock_mode = config.CLOCK_MODE_DIGITAL
            self.clock_mode_button.setText("🕐 아날로그")

        self.settings.set('clock.mode', self.clock_mode)

    def on_clock_size_changed(self, value):
        """Handle clock size slider change"""
        self.clock_scale = value / 100.0
        self.digital_clock.set_scale(self.clock_scale)
        if self.analog_clock:
            self.analog_clock.set_scale(self.clock_scale)
        self.settings.set('clock.scale', self.clock_scale)

    def apply_theme(self):
        """Apply the current theme to the application"""
        if self.current_theme == config.THEME_DARK:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)

        # Force update of analog clock if it exists
        if self.analog_clock:
            self.analog_clock.update()

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)
        # Save window size
        self.settings.set('window.width', self.width())
        self.settings.set('window.height', self.height())
