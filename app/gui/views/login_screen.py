from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
from app.gui.ui.login_screen_ui import Ui_LoginScreen
from app.services.session_service import SessionService
from app.services.config_service import ConfigService

class LoginScreen(QWidget):
    """Login screen widget for the asset management system"""
    
    # Signal emitted when login is successful with session token
    loginSuccessful = Signal(str)  # Passes session token
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginScreen()
        self.ui.setupUi(self)
        
        # Initialize session service and config service
        self.session_service = SessionService()
        self.config_service = ConfigService()
        
        # Set window properties
        self.setWindowTitle("Asset Management System - Login")
        self.setFixedSize(800, 500)  # Fixed size window
        
        # Connect signals
        self.ui.loginButton.clicked.connect(self.handle_login)
        self.ui.passwordInput.returnPressed.connect(self.handle_login)
        
        # Load background image
        self.load_background_image()
        
        # Clear any error message
        self.ui.errorLabel.clear()
        
        # Set dynamic admin hint based on configuration
        self.update_admin_hint()
        
        # Set placeholder text for clarity
        self.ui.usernameInput.setPlaceholderText("Enter your email address")
    
    def update_admin_hint(self):
        """Update the admin credentials hint based on current configuration"""
        try:
            if self.config_service.is_using_default_credentials():
                admin_creds = self.config_service.get_admin_credentials()
                self.ui.errorLabel.setText(f"Default admin login - Email: {admin_creds['email']}, Password: {admin_creds['password']}")
                self.ui.errorLabel.setStyleSheet("color: blue;")
            else:
                self.ui.errorLabel.setText("Enter your credentials to login")
                self.ui.errorLabel.setStyleSheet("color: gray;")
        except Exception as e:
            self.ui.errorLabel.setText("Enter your credentials to login")
            self.ui.errorLabel.setStyleSheet("color: gray;")
        
    def load_background_image(self):
        """Load the background image for the right frame"""
        try:
            import os
            import sys
            
            # Get the base directory - works both in dev and PyInstaller
            if getattr(sys, 'frozen', False):
                # Running as PyInstaller executable
                base_dir = sys._MEIPASS
            else:
                # Running as normal Python script
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            
            image_path = os.path.join(base_dir, "app", "static", "images", "rhv_login.jpg")
            pixmap = QPixmap(image_path)
            
            if not pixmap.isNull():
                self.ui.backgroundLabel.setPixmap(pixmap)
            else:
                print(f"Could not load background image from: {image_path}")
        except Exception as e:
            print(f"Error loading background image: {e}")
    
    def handle_login(self):
        """Handle the login button click or enter key press"""
        # Use email instead of username for consistency
        email = self.ui.usernameInput.text().strip()
        password = self.ui.passwordInput.text().strip()
        
        if not email or not password:
            self.show_error("Please enter both email and password")
            return
        
        # Validate email format (basic check)
        if "@" not in email:
            self.show_error("Please enter a valid email address")
            return
            
        # Authenticate using auth service
        if self.authenticate(email, password):
            self.show_success("Login successful!")
            self.loginSuccessful.emit(self._session_token)
            # Hide instead of close so the login screen can be shown again after logout
            try:
                self.hide()
            except Exception:
                # Fallback to close if hide is not available
                try:
                    self.close()
                except Exception:
                    pass
        else:
            self.ui.passwordInput.clear()  # Clear password on failed attempt
    
    def authenticate(self, email: str, password: str) -> bool:
        """Authenticate user with provided credentials and return success status.
        
        Args:
            email: User's email address
            password: User's password
        
        Returns:
            True if authentication succeeds, False otherwise
        """
        try:
            # Disable login button to prevent multiple attempts
            self.ui.loginButton.setEnabled(False)
            self.ui.loginButton.setText("Logging in...")
            
            print(f"Attempting login for email: {email}")  # Debug logging
            
            # Use the session service login method with email
            result = self.session_service.login(email, password)
            
            print(f"Login result: {result}")  # Debug logging
            
            if isinstance(result, dict) and result.get("success"):
                self._session_token = result.get("session_token")
                print(f"Login successful, got session token: {self._session_token}")  # Debug logging
                return True
                
            # Show specific error message from auth service
            error_msg = result.get("message", "Login failed!")
            print(f"Login failed: {error_msg}")  # Debug logging
            self.show_error(error_msg)
            return False
            
        except Exception as e:
            print(f"Authentication error: {e}")
            self.show_error("Login failed! Please try again.")
            return False
            
        finally:
            # Re-enable login button
            self.ui.loginButton.setEnabled(True)
            self.ui.loginButton.setText("Login")
    
    def show_error(self, message: str):
        """Show error message in red"""
        self.ui.errorLabel.setStyleSheet("color: red; font-weight: bold;")
        self.ui.errorLabel.setText(message)
    
    def show_success(self, message: str):
        """Show success message in green"""
        self.ui.errorLabel.setStyleSheet("color: green; font-weight: bold;")
        self.ui.errorLabel.setText(message)
