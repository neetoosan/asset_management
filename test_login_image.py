#!/usr/bin/env python
"""Test script to verify login screen image loads correctly"""
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.gui.views.login_screen import LoginScreen

def main():
    app = QApplication(sys.argv)
    
    print("Creating LoginScreen...")
    login_screen = LoginScreen()
    
    print("Displaying LoginScreen...")
    login_screen.show()
    
    # Close the app after 3 seconds for testing
    QTimer.singleShot(3000, app.quit)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
