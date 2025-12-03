from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QCheckBox, QMessageBox, QComboBox)
from PySide6.QtCore import Slot
from ...core.models import PermissionType
from ...services.role_service import RoleService
from ...services.auth_service import AuthService


class AdminScreenMethods:
    def setup_roles_frame(self):
        """Setup the roles management frame"""
        if not hasattr(self, 'role_service'):
            self.role_service = RoleService()
            
        # Clear existing items
        while self.ui.roleComboBox.count():
            self.ui.roleComboBox.removeItem(0)
            
        # Add roles to combo box
        roles = self.role_service.get_all_roles()
        for role in roles:
            self.ui.roleComboBox.addItem(role["name"], role["id"])
            
        # Setup permission checkboxes
        self.setup_permission_checkboxes()
    
    def setup_permission_checkboxes(self):
        """Setup permission checkboxes based on PermissionType enum"""
        # Create a container widget for the scroll area if it doesn't exist
        if not hasattr(self, 'permissions_widget'):
            self.permissions_widget = QWidget()
            self.permissions_layout = QVBoxLayout(self.permissions_widget)
        else:
            # Clear existing layout
            while self.permissions_layout.count():
                item = self.permissions_layout.takeAt(0)
                if widget := item.widget():
                    widget.deleteLater()
        
        # Clear existing checkboxes dictionary
        if not hasattr(self, 'permission_checkboxes'):
            self.permission_checkboxes = {}
        self.permission_checkboxes.clear()
        
        # Create a checkbox for each permission type
        for perm in PermissionType:
            checkbox = QCheckBox(perm.value)
            self.permission_checkboxes[perm.value] = checkbox
            self.permissions_layout.addWidget(checkbox)
        
        # Add stretch to align checkboxes at the top
        self.permissions_layout.addStretch()
        
        # Set the widget in scroll area
        self.ui.permissionsScrollArea.setWidget(self.permissions_widget)
    
    @Slot()
    def on_role_changed(self, index):
        """Handle role selection change"""
        role_id = self.ui.roleComboBox.itemData(index)
        if role_id:
            # Get permissions for selected role
            permissions = self.role_service.get_role_permissions(role_id)
            
            # Update checkboxes
            for perm_name, checkbox in self.permission_checkboxes.items():
                checkbox.setChecked(perm_name in permissions)
    
    @Slot()
    def save_user_permissions(self):
        """Save permissions for the selected role"""
        role_id = self.ui.roleComboBox.currentData()
        if not role_id:
            return
            
        # Get selected permissions
        selected_permissions = [
            perm_name
            for perm_name, checkbox in self.permission_checkboxes.items()
            if checkbox.isChecked()
        ]
        
        # Update role permissions
        if self.role_service.update_role_permissions(role_id, selected_permissions):
            QMessageBox.information(
                self,
                "Success",
                "Role permissions updated successfully!"
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to update role permissions."
            )
    
    def update_user_role(self, user_id: int, role_id: int):
        """Update a user's role"""
        if self.role_service.update_user_role(user_id, role_id):
            self.load_users()  # Refresh the users table
            QMessageBox.information(
                self,
                "Success",
                "User role updated successfully!"
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to update user role."
            )
    
    def check_admin_permission(self) -> bool:
        """Check if current user has admin permissions"""
        current_session = self.auth_service.get_current_session()
        if not current_session:
            return False
            
        return self.role_service.check_permission(
            current_session.user_id,
            PermissionType.MANAGE_USERS.value
        )