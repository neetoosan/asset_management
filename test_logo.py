#!/usr/bin/env python3
"""Test script to verify logo loading"""

import os
import sys
from app.core.config import Config
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

def test_logo():
    app = QApplication(sys.argv)
    
    config = Config()
    logo_path = os.path.join(config.BASE_DIR, "app", "static", "images", "logo.png")
    
    print(f"[Test] Config BASE_DIR: {config.BASE_DIR}")
    print(f"[Test] Logo path: {logo_path}")
    print(f"[Test] Logo exists: {os.path.exists(logo_path)}")
    
    if os.path.exists(logo_path):
        pixmap = QPixmap(logo_path)
        print(f"[Test] Pixmap loaded: {not pixmap.isNull()}")
        print(f"[Test] Pixmap size: {pixmap.width()}x{pixmap.height()}")
        
        # Test scaling
        from PySide6.QtCore import Qt
        scaled = pixmap.scaledToHeight(45, Qt.SmoothTransformation)
        print(f"[Test] Scaled size: {scaled.width()}x{scaled.height()}")
        print("[Test] Logo loading test PASSED")
    else:
        print("[Test] Logo file not found!")

if __name__ == "__main__":
    test_logo()
