"""
Cryptocurrency service for fetching BTC data from 7code.co.kr API
"""
import requests
from typing import Optional, Dict, List


class CryptoService:
    """Service to fetch cryptocurrency data from 7code.co.kr"""

    def __init__(self):
        """Initialize the crypto service"""
        self.base_url = "https://7code.co.kr/api"

    def get_btc_data(self) -> Optional[Dict]:
        """
        Get BTC data from coins API

        Returns:
            Dictionary with BTC data or None if request fails
        """
        try:
            response = requests.get(f'{self.base_url}/coins', timeout=10)
            response.raise_for_status()
            coins = response.json()

            # Find BTC in the coin list
            for coin in coins:
                if coin.get('symbol') == 'BTC_KRW' or coin.get('symbol') == 'BTC':
                    return coin

            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching BTC data: {e}")
            return None

    @staticmethod
    def format_price(price: float) -> str:
        """Format price with appropriate separators"""
        if price >= 1000000:
            return f"₩{price:,.0f}"
        elif price >= 1000:
            return f"₩{price:,.0f}"
        else:
            return f"₩{price:.2f}"

    @staticmethod
    def get_signal_icons(signals: List[str]) -> str:
        """
        Convert signal list to icon string

        Signal colors typically:
        - Green: Buy/Bullish
        - Red: Sell/Bearish
        - Gray: Neutral
        """
        if not signals or len(signals) == 0:
            return "⚪⚪⚪⚪⚪"

        icon_map = {
            'buy': '🟢',
            'sell': '🔴',
            'neutral': '⚪',
            'strong_buy': '🟢',
            'strong_sell': '🔴'
        }

        icons = []
        for signal in signals[:5]:  # Maximum 5 icons
            signal_lower = str(signal).lower()
            if 'buy' in signal_lower or 'bull' in signal_lower:
                icons.append('🟢')
            elif 'sell' in signal_lower or 'bear' in signal_lower:
                icons.append('🔴')
            else:
                icons.append('⚪')

        # Pad with gray if less than 5
        while len(icons) < 5:
            icons.append('⚪')

        return ''.join(icons)
