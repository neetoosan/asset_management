from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication
from pathlib import Path
from enum import Enum

class Theme(str, Enum):
    SYSTEM = "System"
    LIGHT = "Light"
    DARK = "Dark"

class ThemeManager:
    def __init__(self):
        self.settings = QSettings("AssetManagement", "Settings")
        self.base_dir = Path(__file__).parent.parent
        self._current_theme = None
    
    def get_system_theme(self) -> Theme:
        """Detect the system theme."""
        # This is a Windows-specific implementation
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return Theme.LIGHT if value == 1 else Theme.DARK
        except:
            return Theme.LIGHT  # Default to light if detection fails
    
    def load_theme(self, theme: Theme = None) -> str:
        """Load and return the appropriate theme stylesheet."""
        if theme is None:
            # Get theme from settings or use system default
            theme = Theme(self.settings.value("theme", Theme.SYSTEM))
        
        if theme == Theme.SYSTEM:
            theme = self.get_system_theme()
        
        # Load the appropriate stylesheet
        theme_file = "lightmode.qss" if theme == Theme.LIGHT else "darkmode.qss"
        css_path = self.base_dir / "static" / "css" / theme_file
        
        try:
            with open(css_path, 'r') as file:
                stylesheet = file.read()
            self._current_theme = theme
            return stylesheet
        except Exception as e:
            print(f"Error loading theme {theme}: {e}")
            return ""
    
    def apply_theme(self, theme: Theme = None):
        """Apply the specified theme to the application."""
        stylesheet = self.load_theme(theme)
        if stylesheet:
            QApplication.instance().setStyleSheet(stylesheet)
            if theme is not None:
                self.settings.setValue("theme", theme)
    
    @property
    def current_theme(self) -> Theme:
        """Get the current theme."""
        if self._current_theme is None:
            saved_theme = Theme(self.settings.value("theme", Theme.SYSTEM))
            self._current_theme = self.get_system_theme() if saved_theme == Theme.SYSTEM else saved_theme
        return self._current_theme