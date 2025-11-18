"""
Crypto widget for displaying multiple crypto prices with slide animation
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QStackedWidget
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty
from PyQt5.QtGui import QFont, QCursor
from src.services.crypto_service import CryptoService


class CryptoWidget(QWidget):
    """Crypto widget that displays multiple crypto prices with slide animation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.crypto_service = CryptoService()

        # Coin rotation setup
        self.coins = ['BTC', 'USDT', 'ETH', 'XRP', 'SOL']
        self.current_coin_index = 0

        self.init_ui()
        self.start_timer()
        self.update_crypto()

    def init_ui(self):
        """Initialize the user interface with right-aligned layout"""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)

        # Push everything to the right
        layout.addStretch()

        # Coin + change rate label (e.g., "USDT (-0.67%)")
        self.coin_change_label = QLabel("BTC (--)")
        self.coin_change_label.setFont(QFont('Ubuntu', 10, QFont.Bold))
        self.coin_change_label.setMinimumWidth(200)
        self.coin_change_label.setMaximumWidth(200)
        self.coin_change_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.coin_change_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.coin_change_label.mousePressEvent = self.mousePressEvent

        # Price label - left-aligned (e.g., "₩142,350,000")
        self.price_label = QLabel("₩--")
        price_font = QFont('Ubuntu Mono', 10)
        self.price_label.setFont(price_font)
        self.price_label.setMinimumWidth(180)
        self.price_label.setMaximumWidth(180)
        self.price_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Changed to left
        self.price_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.price_label.mousePressEvent = self.mousePressEvent

        # Signal icons - fixed width
        self.signal_label = QLabel("● ● ● ● ●")
        signal_font = QFont('Ubuntu', 10)
        self.signal_label.setFont(signal_font)
        self.signal_label.setStyleSheet("color: #888888;")
        self.signal_label.setMinimumWidth(170)
        self.signal_label.setMaximumWidth(170)
        self.signal_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        layout.addWidget(self.coin_change_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.signal_label)

        self.setLayout(layout)

        # Set minimum width to prevent widget from shrinking
        # Total: coin(200) + price(180) + signal(170) + margins + spacing = ~570
        self.setMinimumWidth(570)

    def mousePressEvent(self, event):
        """Handle mouse click to open website"""
        if event.button() == Qt.LeftButton:
            import webbrowser
            webbrowser.open('https://7code.co.kr')

    def start_timer(self):
        """Start the timer to rotate coins and update crypto info"""
        # Timer for coin rotation (every 5 seconds)
        self.rotation_timer = QTimer(self)
        self.rotation_timer.timeout.connect(self.rotate_coin)
        self.rotation_timer.start(5000)  # Rotate every 5 seconds

        # Timer for data refresh (every 30 seconds)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_all_data)
        self.refresh_timer.start(30000)  # Refresh all data every 30 seconds

    def rotate_coin(self):
        """Rotate to the next coin with slide animation"""
        # Slide out to the left
        widget_width = self.width()

        # Animate all labels sliding out to left
        self.slide_out_animations = []
        for label in [self.coin_change_label, self.price_label, self.signal_label]:
            anim = QPropertyAnimation(label, b"pos")
            anim.setDuration(400)
            anim.setStartValue(label.pos())
            anim.setEndValue(QPoint(label.pos().x() - widget_width, label.pos().y()))
            anim.setEasingCurve(QEasingCurve.InOutCubic)
            self.slide_out_animations.append(anim)

        # Connect last animation to switch coin
        self.slide_out_animations[-1].finished.connect(self.switch_coin)

        # Start all animations
        for anim in self.slide_out_animations:
            anim.start()

    def switch_coin(self):
        """Switch to next coin and slide in from right"""
        # Move to next coin
        self.current_coin_index = (self.current_coin_index + 1) % len(self.coins)

        widget_width = self.width()

        # Position labels off-screen to the right
        for label in [self.coin_change_label, self.price_label, self.signal_label]:
            current_pos = label.pos()
            label.move(current_pos.x() + widget_width * 2, current_pos.y())

        # Update content
        self.update_crypto()

        # Slide in from right
        self.slide_in_animations = []
        for label in [self.coin_change_label, self.price_label, self.signal_label]:
            anim = QPropertyAnimation(label, b"pos")
            anim.setDuration(400)
            anim.setStartValue(label.pos())
            anim.setEndValue(QPoint(label.pos().x() - widget_width, label.pos().y()))
            anim.setEasingCurve(QEasingCurve.InOutCubic)
            self.slide_in_animations.append(anim)

        # Start all animations
        for anim in self.slide_in_animations:
            anim.start()

    def refresh_all_data(self):
        """Refresh data for current coin"""
        self.update_crypto()

    def update_crypto(self):
        """Update cryptocurrency information for current coin"""
        current_symbol = self.coins[self.current_coin_index]
        coin_data = self.crypto_service.get_coin_data(current_symbol)

        if coin_data:
            # Get price and change rate
            price = coin_data.get('closing_price', 0)
            change_rate = coin_data.get('fluctate_rate', 0)
            coin_name = coin_data.get('name', current_symbol)

            # Update coin + change rate
            if change_rate > 0:
                change_text = f'<span style="color: #00ff00;">(+{change_rate:.2f}%)</span>'
            elif change_rate < 0:
                change_text = f'<span style="color: #ff0000;">({change_rate:.2f}%)</span>'
            else:
                change_text = f'<span style="color: #888888;">(0.00%)</span>'

            self.coin_change_label.setText(f"{current_symbol} {change_text}")

            # Update price
            if price > 0:
                formatted_price = self.crypto_service.format_price(price)
                self.price_label.setText(formatted_price)
            else:
                self.price_label.setText("₩--")

            # Update signals (if available in data)
            signals = coin_data.get('signals', [])
            if signals:
                signal_icons = self.crypto_service.get_signal_icons(signals)
                self.signal_label.setText(signal_icons)
            else:
                # If no signals field, use change_rate to show trend with colored circles
                if change_rate > 2:
                    self.signal_label.setText('<span style="color: #00ff00;">● ● ●</span> <span style="color: #888888;">● ●</span>')
                elif change_rate > 0:
                    self.signal_label.setText('<span style="color: #00ff00;">● ●</span> <span style="color: #888888;">● ● ●</span>')
                elif change_rate < -2:
                    self.signal_label.setText('<span style="color: #ff0000;">● ● ●</span> <span style="color: #888888;">● ●</span>')
                elif change_rate < 0:
                    self.signal_label.setText('<span style="color: #ff0000;">● ●</span> <span style="color: #888888;">● ● ●</span>')
                else:
                    self.signal_label.setText('<span style="color: #888888;">● ● ● ● ●</span>')
                self.signal_label.setStyleSheet("")  # Clear default style

            # Update tooltip
            tooltip = f"{current_symbol} ({coin_name})\n"
            tooltip += f"현재가: {self.crypto_service.format_price(price)}\n"
            tooltip += f"변동: {change_rate:+.2f}%\n"
            if 'volume' in coin_data:
                volume = coin_data['volume']
                tooltip += f"거래량: ₩{volume/100000000:.1f}억\n"
            tooltip += "\n클릭하여 7code.co.kr에서 더 보기"
            for label in [self.coin_change_label, self.price_label]:
                label.setToolTip(tooltip)
        else:
            self.coin_change_label.setText(f"{current_symbol} (--)")
            self.price_label.setText("₩--")
            self.signal_label.setText('<span style="color: #888888;">● ● ● ● ●</span>')
            for label in [self.coin_change_label, self.price_label]:
                label.setToolTip("데이터 로딩 실패\n클릭하여 7code.co.kr에서 더 보기")
