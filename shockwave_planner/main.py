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
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "resources", "splash_intro.png")

    # 3. Load the image into a QPixmap
    pixmap = QPixmap(splash_path)

    # 4. Create and show the splash screen
    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    splash.show()

    # Make sure the splash is actually drawn
    app.processEvents()

    # 5. Create your main window (while splash is showing)
    window = MainWindow()

    # 6. Optional: keep the splash up for at least 2 seconds, 
    #    then show main window and hide splash
    def finish_loading():
        window.show()
        splash.finish(window)  # hides the splash

    # Show the main window after 2000 ms (2 seconds)
    QTimer.singleShot(5000, finish_loading)

    # 7. Start the Qt event loop
    sys.exit(app.exec())
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

