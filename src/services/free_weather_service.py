"""
Free weather service using Open-Meteo API (no API key required)
"""
import requests
from typing import Optional, Dict


class FreeWeatherService:
    """Service to fetch weather data from Open-Meteo API (free, no API key)"""

    def __init__(self):
        """Initialize the free weather service"""
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def get_weather(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get current weather data

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with weather data or None if request fails
        """
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m',
            'timezone': 'Asia/Seoul'
        }

        try:
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get air quality data

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with air quality data or None if request fails
        """
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'pm2_5,pm10',
            'timezone': 'Asia/Seoul'
        }

        try:
            response = requests.get(self.air_quality_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching air quality data: {e}")
            return None

    @staticmethod
    def get_pm25_description(pm25: float) -> str:
        """
        Get air quality description based on PM2.5 in English

        Args:
            pm25: PM2.5 value

        Returns:
            English description of air quality
        """
        if pm25 <= 15:
            return "Good"
        elif pm25 <= 35:
            return "Moderate"
        elif pm25 <= 75:
            return "Unhealthy"
        else:
            return "Very Unhealthy"

    @staticmethod
    def get_weather_description(weather_code: int) -> str:
        """
        Get weather description based on WMO weather code in English

        Args:
            weather_code: WMO weather code

        Returns:
            English weather description
        """
        weather_descriptions = {
            0: "Clear",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light Drizzle",
            53: "Drizzle",
            55: "Heavy Drizzle",
            61: "Light Rain",
            63: "Rain",
            65: "Heavy Rain",
            71: "Light Snow",
            73: "Snow",
            75: "Heavy Snow",
            77: "Sleet",
            80: "Showers",
            81: "Showers",
            82: "Heavy Showers",
            85: "Snow",
            86: "Heavy Snow",
            95: "Thunderstorm",
            96: "Thunderstorm",
            99: "Heavy Thunderstorm"
        }
        return weather_descriptions.get(weather_code, "Unknown")

    @staticmethod
    def get_weather_icon(weather_code: int) -> str:
        """
        Get weather emoji based on weather code

        Args:
            weather_code: WMO weather code

        Returns:
            Weather emoji
        """
        if weather_code == 0:
            return "☀️"
        elif weather_code in [1, 2]:
            return "⛅"
        elif weather_code == 3:
            return "☁️"
        elif weather_code in [45, 48]:
            return "🌫️"
        elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "🌧️"
        elif weather_code in [71, 73, 75, 77, 85, 86]:
            return "❄️"
        elif weather_code in [95, 96, 99]:
            return "⛈️"
        else:
            return "🌡️"
