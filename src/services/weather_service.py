"""
Weather service for fetching weather data from OpenWeatherMap API
"""
import requests
from typing import Optional, Dict


class WeatherService:
    """Service to fetch weather and air quality data"""

    def __init__(self, api_key: str):
        """
        Initialize the weather service

        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.air_quality_url = "https://api.openweathermap.org/data/2.5/air_pollution"

    def get_weather(self, city: str = None, lat: float = None, lon: float = None) -> Optional[Dict]:
        """
        Get current weather data

        Args:
            city: City name (optional)
            lat: Latitude (optional)
            lon: Longitude (optional)

        Returns:
            Dictionary with weather data or None if request fails
        """
        if not self.api_key:
            return None

        params = {
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'kr'
        }

        if city:
            params['q'] = city
        elif lat is not None and lon is not None:
            params['lat'] = lat
            params['lon'] = lon
        else:
            return None

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
        if not self.api_key:
            return None

        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }

        try:
            response = requests.get(self.air_quality_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching air quality data: {e}")
            return None

    @staticmethod
    def get_aqi_description(aqi: int) -> str:
        """
        Get air quality description in Korean

        Args:
            aqi: Air Quality Index (1-5)

        Returns:
            Korean description of air quality
        """
        descriptions = {
            1: "좋음",
            2: "보통",
            3: "나쁨",
            4: "매우 나쁨",
            5: "최악"
        }
        return descriptions.get(aqi, "알 수 없음")

    @staticmethod
    def get_weather_icon(icon_code: str) -> str:
        """
        Get weather emoji based on icon code

        Args:
            icon_code: OpenWeatherMap icon code

        Returns:
            Weather emoji
        """
        icon_map = {
            '01d': '☀️',  # clear sky day
            '01n': '🌙',  # clear sky night
            '02d': '⛅',  # few clouds day
            '02n': '☁️',  # few clouds night
            '03d': '☁️',  # scattered clouds
            '03n': '☁️',
            '04d': '☁️',  # broken clouds
            '04n': '☁️',
            '09d': '🌧️',  # shower rain
            '09n': '🌧️',
            '10d': '🌦️',  # rain day
            '10n': '🌧️',  # rain night
            '11d': '⛈️',  # thunderstorm
            '11n': '⛈️',
            '13d': '❄️',  # snow
            '13n': '❄️',
            '50d': '🌫️',  # mist
            '50n': '🌫️'
        }
        return icon_map.get(icon_code, '🌡️')
