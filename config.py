"""
Configuration file for the Desktop Clock & Weather Application
"""

# Weather API Configuration
# OpenWeatherMap API: https://openweathermap.org/api
WEATHER_API_KEY = ""  # Add your API key here
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
AIR_QUALITY_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

# Default location (Seoul, Korea)
DEFAULT_CITY = "Seoul"
DEFAULT_COUNTRY = "KR"
DEFAULT_LAT = 37.5665
DEFAULT_LON = 126.9780

# Application Settings
APP_NAME = "Desktop Clock & Weather"
APP_VERSION = "1.0.0"

# Window Settings
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 900
MIN_WINDOW_WIDTH = 735
MIN_WINDOW_HEIGHT = 800

# Update Intervals (in milliseconds)
CLOCK_UPDATE_INTERVAL = 1000  # 1 second
WEATHER_UPDATE_INTERVAL = 600000  # 10 minutes

# Theme Settings
THEME_DARK = "dark"
THEME_LIGHT = "light"
DEFAULT_THEME = THEME_DARK

# Clock Settings
CLOCK_MODE_DIGITAL = "digital"
CLOCK_MODE_ANALOG = "analog"
DEFAULT_CLOCK_MODE = CLOCK_MODE_ANALOG
