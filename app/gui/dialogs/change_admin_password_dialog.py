"""
Change Admin Password Dialog
Allows the admin user to change their credentials securely
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                               QLineEdit, QPushButton, QLabel, QMessageBox, 
                               QGroupBox, QCheckBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from app.services.config_service import ConfigService
from app.services.session_service import SessionService


class ChangeAdminPasswordDialog(QDialog):
    """
    Dialog for changing admin credentials
    """
    
    # Signal emitted when credentials are successfully changed
    credentialsChanged = Signal()
    
    def __init__(self, session_service: SessionService, parent=None):
        super().__init__(parent)
        self.session_service = session_service
        self.config_service = ConfigService()
        
        self.setWindowTitle("Change Admin Credentials")
        self.setModal(True)
        self.setFixedSize(500, 400)
        
        self.setup_ui()
        self.load_current_info()
    
    def setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Change Admin Credentials")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Warning if using defaults
        self.warning_label = QLabel()
        self.warning_label.setWordWrap(True)
        self.warning_label.setStyleSheet("color: red; font-weight: bold; padding: 10px; background-color: #ffe6e6; border: 1px solid #ff9999; border-radius: 5px;")
        layout.addWidget(self.warning_label)
        
        # Current info group
        current_group = QGroupBox("Current Admin Information")
        current_layout = QFormLayout(current_group)
        
        self.current_email_label = QLabel()
        self.current_email_label.setStyleSheet("font-weight: bold;")
        current_layout.addRow("Current Email:", self.current_email_label)
        
        self.default_status_label = QLabel()
        current_layout.addRow("Status:", self.default_status_label)
        
        layout.addWidget(current_group)
        
        # New credentials group
        new_group = QGroupBox("New Admin Credentials")
        form_layout = QFormLayout(new_group)
        
        # Current password
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Current Password*:", self.current_password_input)
        
        # New email
        self.new_email_input = QLineEdit()
        self.new_email_input.setPlaceholderText("Enter new admin email")
        form_layout.addRow("New Email*:", self.new_email_input)
        
        # New password
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Enter new password")
        form_layout.addRow("New Password*:", self.new_password_input)
        
        # Confirm password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        form_layout.addRow("Confirm Password*:", self.confirm_password_input)
        
        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show passwords")
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        form_layout.addRow("", self.show_password_checkbox)
        
        layout.addWidget(new_group)
        
        # Password requirements
        requirements_label = QLabel(
            "Password Requirements:\\n"
            "• Minimum 8 characters\\n"
            "• At least one uppercase letter\\n"
            "• At least one lowercase letter\\n"
            "• At least one digit\\n"
            "• At least one special character"
        )
        requirements_label.setStyleSheet("color: #666; font-size: 10px; padding: 5px;")
        layout.addWidget(requirements_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setStyleSheet("QPushButton { background-color: #007acc; color: white; padding: 8px 16px; border-radius: 4px; }")
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("QPushButton { background-color: #6c757d; color: white; padding: 8px 16px; border-radius: 4px; }")
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def load_current_info(self):
        """Load current admin information"""
        try:
            # Get current admin credentials
            admin_creds = self.config_service.get_admin_credentials()
            self.current_email_label.setText(admin_creds["email"])
            
            # Set current email as default for new email
            self.new_email_input.setText(admin_creds["email"])
            
            # Check if using default credentials
            if self.config_service.is_using_default_credentials():
                self.warning_label.setText(
                    "⚠️ WARNING: You are currently using default admin credentials. "
                    "This is a security risk. Please change them immediately!"
                )
                self.warning_label.show()
                self.default_status_label.setText("Using Default Credentials")
                self.default_status_label.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.warning_label.hide()
                self.default_status_label.setText("Custom Credentials")
                self.default_status_label.setStyleSheet("color: green; font-weight: bold;")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load current admin information: {str(e)}")
    
    def toggle_password_visibility(self, checked):
        """Toggle password visibility"""
        if checked:
            self.current_password_input.setEchoMode(QLineEdit.Normal)
            self.new_password_input.setEchoMode(QLineEdit.Normal)
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.current_password_input.setEchoMode(QLineEdit.Password)
            self.new_password_input.setEchoMode(QLineEdit.Password)
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
    
    def validate_input(self) -> tuple[bool, str]:
        """Validate input fields"""
        current_password = self.current_password_input.text().strip()
        new_email = self.new_email_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        # Check required fields
        if not current_password:
            return False, "Current password is required"
        
        if not new_email:
            return False, "New email is required"
        
        if not new_password:
            return False, "New password is required"
        
        if not confirm_password:
            return False, "Password confirmation is required"
        
        # Validate email format
        if "@" not in new_email or "." not in new_email:
            return False, "Please enter a valid email address"
        
        # Check password confirmation
        if new_password != confirm_password:
            return False, "New password and confirmation do not match"
        
        # Validate current password
        admin_creds = self.config_service.get_admin_credentials()
        if current_password != admin_creds["password"]:
            return False, "Current password is incorrect"
        
        # Validate new password strength
        validation_result = self.config_service.validate_password_strength(new_password)
        if not validation_result["valid"]:
            return False, "\\n".join(validation_result["errors"])
        
        return True, ""
    
    def save_changes(self):
        """Save the new admin credentials"""
        try:
            # Validate input
            is_valid, error_message = self.validate_input()
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", error_message)
                return
            
            new_email = self.new_email_input.text().strip()
            new_password = self.new_password_input.text().strip()
            
            # Confirm the change
            reply = QMessageBox.question(
                self, 
                "Confirm Changes",
                f"Are you sure you want to change the admin credentials to:\\n\\nEmail: {new_email}\\n\\nThis will log you out and you'll need to login again with the new credentials.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # Save new credentials
            success = self.config_service.set_admin_credentials(new_email, new_password)
            
            if success:
                QMessageBox.information(
                    self, 
                    "Success",
                    "Admin credentials have been changed successfully!\\n\\nYou will be logged out. Please login again with your new credentials."
                )
                
                # Emit signal and close
                self.credentialsChanged.emit()
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Error", 
                    "Failed to save new credentials. Please try again."
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while changing credentials: {str(e)}")
    
    def closeEvent(self, event):
        """Handle dialog close event"""
        # Clear password fields for security
        self.current_password_input.clear()
        self.new_password_input.clear()
        self.confirm_password_input.clear()
        super().closeEvent(event)