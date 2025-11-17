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
        Get air quality description based on PM2.5 in Korean

        Args:
            pm25: PM2.5 value

        Returns:
            Korean description of air quality
        """
        if pm25 <= 15:
            return "좋음"
        elif pm25 <= 35:
            return "보통"
        elif pm25 <= 75:
            return "나쁨"
        else:
            return "매우 나쁨"

    @staticmethod
    def get_weather_description(weather_code: int) -> str:
        """
        Get weather description based on WMO weather code in Korean

        Args:
            weather_code: WMO weather code

        Returns:
            Korean weather description
        """
        weather_descriptions = {
            0: "맑음",
            1: "대체로 맑음",
            2: "구름 조금",
            3: "흐림",
            45: "안개",
            48: "안개",
            51: "가벼운 이슬비",
            53: "이슬비",
            55: "강한 이슬비",
            61: "약한 비",
            63: "비",
            65: "강한 비",
            71: "약한 눈",
            73: "눈",
            75: "강한 눈",
            77: "진눈깨비",
            80: "소나기",
            81: "소나기",
            82: "강한 소나기",
            85: "눈",
            86: "강한 눈",
            95: "뇌우",
            96: "뇌우",
            99: "강한 뇌우"
        }
        return weather_descriptions.get(weather_code, "알 수 없음")

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
