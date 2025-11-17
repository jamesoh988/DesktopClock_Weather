"""
Crypto widget for displaying BTC price and analysis
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QCursor
from src.services.crypto_service import CryptoService


class CryptoWidget(QWidget):
    """Crypto widget that displays BTC price and signals"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.crypto_service = CryptoService()
        self.init_ui()
        self.start_timer()
        self.update_crypto()

    def init_ui(self):
        """Initialize the user interface"""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        # BTC label
        self.btc_label = QLabel("BTC")
        btc_font = QFont('Ubuntu', 10, QFont.Bold)
        self.btc_label.setFont(btc_font)

        # Price label
        self.price_label = QLabel("₩--")
        price_font = QFont('Ubuntu', 10)
        self.price_label.setFont(price_font)

        # Change label
        self.change_label = QLabel("--")
        change_font = QFont('Ubuntu', 9)
        self.change_label.setFont(change_font)

        # Signal icons
        self.signal_label = QLabel("⚪⚪⚪⚪⚪")
        signal_font = QFont('Ubuntu', 10)
        self.signal_label.setFont(signal_font)

        layout.addWidget(self.btc_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.change_label)
        layout.addWidget(self.signal_label)
        layout.addStretch()

        self.setLayout(layout)

        # Make clickable
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip("클릭하여 7code.co.kr에서 더 보기")

    def mousePressEvent(self, event):
        """Handle mouse click to open website"""
        if event.button() == Qt.LeftButton:
            import webbrowser
            webbrowser.open('https://7code.co.kr')

    def start_timer(self):
        """Start the timer to update crypto info periodically"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_crypto)
        self.timer.start(30000)  # Update every 30 seconds

    def update_crypto(self):
        """Update cryptocurrency information"""
        btc_data = self.crypto_service.get_btc_data()

        if btc_data:
            # Update price
            price = btc_data.get('closing_price', 0)
            if price > 0:
                formatted_price = self.crypto_service.format_price(price)
                self.price_label.setText(formatted_price)

            # Update change percentage
            change_rate = btc_data.get('fluctate_rate_24H', 0)
            if change_rate != 0:
                if change_rate > 0:
                    self.change_label.setText(f"(+{change_rate:.2f}%)")
                    self.change_label.setStyleSheet("color: #00ff00;")
                else:
                    self.change_label.setText(f"({change_rate:.2f}%)")
                    self.change_label.setStyleSheet("color: #ff0000;")
            else:
                self.change_label.setText("(0.00%)")
                self.change_label.setStyleSheet("color: #888888;")

            # Update signals (if available in data)
            signals = btc_data.get('signals', [])
            if signals:
                signal_icons = self.crypto_service.get_signal_icons(signals)
                self.signal_label.setText(signal_icons)
            else:
                # If no signals field, use change_rate to show trend
                if change_rate > 2:
                    self.signal_label.setText("🟢🟢🟢⚪⚪")
                elif change_rate > 0:
                    self.signal_label.setText("🟢🟢⚪⚪⚪")
                elif change_rate < -2:
                    self.signal_label.setText("🔴🔴🔴⚪⚪")
                elif change_rate < 0:
                    self.signal_label.setText("🔴🔴⚪⚪⚪")
                else:
                    self.signal_label.setText("⚪⚪⚪⚪⚪")

            # Update tooltip
            tooltip = f"BTC (Bitcoin)\n"
            tooltip += f"현재가: {self.crypto_service.format_price(price)}\n"
            tooltip += f"24h 변동: {change_rate:+.2f}%\n"
            if 'acc_trade_value_24H' in btc_data:
                volume = btc_data['acc_trade_value_24H']
                tooltip += f"거래량: ₩{volume/100000000:.1f}억\n"
            tooltip += "\n클릭하여 7code.co.kr에서 더 보기"
            self.setToolTip(tooltip)
        else:
            self.price_label.setText("₩--")
            self.change_label.setText("--")
            self.signal_label.setText("⚪⚪⚪⚪⚪")
            self.setToolTip("데이터 로딩 실패\n클릭하여 7code.co.kr에서 더 보기")
