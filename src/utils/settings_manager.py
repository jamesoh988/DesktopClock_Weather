"""
Settings manager for saving and loading user preferences
"""
import json
import os
from typing import Any, Dict


class SettingsManager:
    """Manages user settings persistence"""

    def __init__(self, settings_file: str = "user_settings.json"):
        """
        Initialize settings manager

        Args:
            settings_file: Path to settings JSON file
        """
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        """
        Load settings from JSON file

        Returns:
            Dictionary of settings
        """
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.get_default_settings()
        else:
            return self.get_default_settings()

    def save_settings(self) -> bool:
        """
        Save current settings to JSON file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value

        Args:
            key: Setting key (supports dot notation like 'window.width')
            default: Default value if key not found

        Returns:
            Setting value or default
        """
        keys = key.split('.')
        value = self.settings

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a setting value

        Args:
            key: Setting key (supports dot notation like 'window.width')
            value: Value to set
        """
        keys = key.split('.')
        current = self.settings

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value
        self.save_settings()

    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        """
        Get default settings

        Returns:
            Dictionary of default settings
        """
        return {
            "window": {
                "width": 1200,
                "height": 900
            },
            "theme": "dark",
            "clock": {
                "mode": "analog",
                "scale": 1.0
            },
            "location": {
                "city": "Seoul",
                "latitude": 37.5665,
                "longitude": 126.978
            }
        }
