"""
Location service for detecting user's location based on IP
"""
import requests
from typing import Optional, Dict


class LocationService:
    """Service to detect user's location"""

    @staticmethod
    def get_location_by_ip() -> Optional[Dict]:
        """
        Get location based on IP address

        Returns:
            Dictionary with location data or None if request fails
        """
        try:
            # Use ip-api.com (free, no API key required)
            response = requests.get('http://ip-api.com/json/', timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                return {
                    'city': data.get('city', 'Unknown'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('regionName', 'Unknown')
                }
        except requests.exceptions.RequestException as e:
            print(f"Error detecting location: {e}")

        return None

    @staticmethod
    def get_location_by_ip_alternative() -> Optional[Dict]:
        """
        Alternative method using ipapi.co (backup)

        Returns:
            Dictionary with location data or None if request fails
        """
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                'city': data.get('city', 'Unknown'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'country': data.get('country_name', 'Unknown'),
                'region': data.get('region', 'Unknown')
            }
        except requests.exceptions.RequestException as e:
            print(f"Error detecting location (alternative): {e}")

        return None

    @staticmethod
    def detect_location() -> Dict:
        """
        Detect user's location, trying multiple methods

        Returns:
            Dictionary with location data, falls back to Seoul if detection fails
        """
        # Try primary method
        location = LocationService.get_location_by_ip()

        # Try alternative if primary fails
        if not location:
            location = LocationService.get_location_by_ip_alternative()

        # Fall back to Seoul if both fail
        if not location or not location.get('latitude') or not location.get('longitude'):
            print("Location detection failed, using default (Seoul)")
            return {
                'city': 'Seoul',
                'latitude': 37.5665,
                'longitude': 126.9780,
                'country': 'South Korea',
                'region': 'Seoul'
            }

        return location
