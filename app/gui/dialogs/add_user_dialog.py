from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal
from ..ui.add_user_dialog_ui import Ui_AddUserDialog
from ...core.models import UserRole
from ...services.user_service import UserService


class AddUserDialog(QDialog):
    # Signals for user operations
    user_created = Signal(object)  # QVariantMap in Qt
    user_updated = Signal(object)  # QVariantMap in Qt
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.ui = Ui_AddUserDialog()
        self.ui.setupUi(self)
        
        # Store user data for edit mode
        self.user_data = user_data
        self.is_edit_mode = user_data is not None
        
        # Initialize user service
        self.user_service = UserService()
        
        # Setup the dialog
        self.setup_dialog()
        
        # Connect signals
        self.ui.saveButton.clicked.connect(self.save_user)
        self.ui.cancelButton.clicked.connect(self.reject)
        
        # Populate data if in edit mode
        if self.is_edit_mode:
            self.populate_user_data()
    
    def setup_dialog(self):
        """Setup the dialog for add or edit mode"""
        if self.is_edit_mode:
            self.setWindowTitle("Edit User")
            self.ui.titleLabel.setText("Edit User")
            # In edit mode, password is optional
            self.ui.passwordLineEdit.setPlaceholderText("Leave blank to keep current password")
            self.ui.confirmPasswordLineEdit.setPlaceholderText("Leave blank to keep current password")
        else:
            self.setWindowTitle("Add User")
            self.ui.titleLabel.setText("Add New User")
    
    def populate_user_data(self):
        """Populate form fields with existing user data"""
        if not self.user_data:
            return
            
        self.ui.nameLineEdit.setText(self.user_data.get('name', ''))
        self.ui.emailLineEdit.setText(self.user_data.get('email', ''))
        self.ui.departmentLineEdit.setText(self.user_data.get('department', ''))
        self.ui.positionLineEdit.setText(self.user_data.get('position', ''))
        
        # Set role
        role = self.user_data.get('role', 'User')
        index = self.ui.roleComboBox.findText(role)
        if index >= 0:
            self.ui.roleComboBox.setCurrentIndex(index)
        
        # Set status
        status = self.user_data.get('status', 'Active')
        index = self.ui.statusComboBox.findText(status)
        if index >= 0:
            self.ui.statusComboBox.setCurrentIndex(index)
    
    def validate_form(self):
        """Validate form inputs"""
        # Check required fields
        if not self.ui.nameLineEdit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Full Name is required.")
            self.ui.nameLineEdit.setFocus()
            return False
        
        if not self.ui.emailLineEdit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Email is required.")
            self.ui.emailLineEdit.setFocus()
            return False
        
        # Basic email validation
        email = self.ui.emailLineEdit.text().strip()
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid email address.")
            self.ui.emailLineEdit.setFocus()
            return False
        
        # Password validation (only for new users or if password is entered in edit mode)
        password = self.ui.passwordLineEdit.text()
        confirm_password = self.ui.confirmPasswordLineEdit.text()
        
        if not self.is_edit_mode:  # New user must have password
            if not password:
                QMessageBox.warning(self, "Validation Error", "Password is required.")
                self.ui.passwordLineEdit.setFocus()
                return False
            
            if len(password) < 6:
                QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters long.")
                self.ui.passwordLineEdit.setFocus()
                return False
        
        # If password is entered (new user or edit with new password), validate confirmation
        if password:
            if password != confirm_password:
                QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
                self.ui.confirmPasswordLineEdit.setFocus()
                return False
        
        return True
    
    def get_user_data(self):
        """Get user data from form"""
        user_data = {
            'name': self.ui.nameLineEdit.text().strip(),
            'email': self.ui.emailLineEdit.text().strip(),
            'department': self.ui.departmentLineEdit.text().strip(),
            'position': self.ui.positionLineEdit.text().strip(),
            'role': self.ui.roleComboBox.currentText(),
            'status': self.ui.statusComboBox.currentText(),
            # Provide service-friendly key name as well to avoid mismatches
            'is_active': self.ui.statusComboBox.currentText(),
        }
        
        # Only include password if it's entered
        password = self.ui.passwordLineEdit.text()
        if password:
            user_data['password'] = password
        
        # Include user ID if in edit mode
        if self.is_edit_mode and self.user_data:
            # support both dict and ORM-like objects
            try:
                # dict-like
                user_data['id'] = self.user_data.get('id')
            except Exception:
                # object with attribute
                user_data['id'] = getattr(self.user_data, 'id', None)
        
        return user_data
    
    def save_user(self):
        """Save user data"""
        if not self.validate_form():
            return
        
        try:
            user_data = self.get_user_data()
            
            if self.is_edit_mode:
                # Update existing user
                result = self.user_service.update_user(user_data['id'], user_data)
                if result.get('success'):
                    # Emit updated signal for consumers
                    try:
                        self.user_updated.emit(result['user'])
                    except Exception:
                        # Fallback: some consumers may be connected to user_created
                        self.user_created.emit(result['user'])
                    QMessageBox.information(self, "Success", "User updated successfully!")
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", result.get('message', 'Failed to update user'))
            else:
                # Create new user
                result = self.user_service.create_user(user_data)
                if result.get('success'):
                    self.user_created.emit(result['user'])
                    QMessageBox.information(self, "Success", "User created successfully!")
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", result.get('message', 'Failed to create user'))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Enter key saves the user
            self.save_user()
        else:
            super().keyPressEvent(event)
