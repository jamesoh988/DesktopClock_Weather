#!/usr/bin/env python3
"""
Desktop Clock & Weather Application
Main entry point
"""
import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main function to start the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Desktop Clock & Weather")
    app.setOrganizationName("DesktopClock")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Start event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
