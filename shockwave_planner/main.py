#!/usr/bin/env python3
"""
SHOCKWAVE PLANNER v1.1
Desktop Launch Operations Planning System
Enhanced with Timeline View, Date Filters, and NOTAM Support

Author: Remix Astronautics  
Date: November 2025
Version: 1.1.0
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
    app.setApplicationName("SHOCKWAVE PLANNER v1.1")
    app.setOrganizationName("Remix Astronautics")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
