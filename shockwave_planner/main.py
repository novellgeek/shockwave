#!/usr/bin/env python3
"""
SHOCKWAVE PLANNER v1.0
Desktop Launch Operations Planning System
For tracking Chinese launch activities

Author: Remix Astronautics
Date: November 2025
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow


def main():
    """Main application entry point"""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("SHOCKWAVE PLANNER")
    app.setOrganizationName("Remix Astronautics")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
