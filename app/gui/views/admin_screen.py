from PySide6.QtWidgets import (QWidget, QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox,
                             QCheckBox, QRadioButton, QButtonGroup, QTableWidgetItem,
                             QGroupBox, QScrollArea, QTableWidget)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QColor, QBrush, QKeySequence, QAction
from ..ui.admin_screen_ui import Ui_AdminScreen
from ..dialogs.add_user_dialog import AddUserDialog
from ...core.models import UserRole, PermissionType, User, Role, RolePermission, Permission
from ...core.database import get_db
from ...services.user_service import UserService
from ...services.role_service import RoleService
from ...services.auth_service import AuthService
from ...services.audit_service import AuditService
from datetime import datetime
from .admin_screen_methods import AdminScreenMethods
from .recently_deleted import RecentlyDeletedDialog
import logging

logger = logging.getLogger(__name__)


class AdminScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AdminScreen()
        self.ui.setupUi(self)
        
        # Initialize services
        self.user_service = UserService()
        self.role_service = RoleService()
        # Prefer to use the parent window's session/auth context when available
        self.parent_window = parent
        try:
            self.session_service = parent.session_service if parent and hasattr(parent, 'session_service') else None
        except Exception:
            self.session_service = None
        # Fallback auth service only if no session context is available
        self.auth_service = AuthService() if self.session_service is None else None
        
        # Initialize state
        self.current_selected_user = None
        self.permission_checkboxes = {}
        self.role_radio_buttons = {}
        self.role_button_group = QButtonGroup()
        # Audit service for admin notifications
        self.audit_service = AuditService()
        # If we have a session service, pass current user context to audit service
        try:
            if self.session_service and self.session_service.is_authenticated():
                self.audit_service.set_current_user(self.session_service.get_user_id(), self.session_service.get_username())
        except Exception:
            pass
        
        # Setup UI components
        self.setup_tables()
        self.setup_connections()
        self.setup_roles()
        
        # Check admin permissions first
        has_admin_access = self.check_admin_permission()
        
        if has_admin_access:
            print("DEBUG: Admin access granted, loading data")
            # Load initial data
            self.load_users()
            self.load_audit_logs()
            self.load_notifications()
        else:
            print("DEBUG: Admin access denied, disabling features")
            self.disable_admin_features()
            QMessageBox.warning(
                self,
                "Access Denied",
                "You don't have admin permissions to access this screen."
            )

    def setup_tables(self):
        """Setup the tables with proper columns and configuration"""
        # Setup users table
        self.ui.usersTable.setColumnWidth(0, 150)  # Username
        self.ui.usersTable.setColumnWidth(1, 200)  # Full Name
        self.ui.usersTable.setColumnWidth(2, 100)  # Role
        self.ui.usersTable.setColumnWidth(3, 100)  # Status
        self.ui.usersTable.setColumnWidth(4, 150)  # Actions
        
        # Setup audit logs table
        self.ui.auditLogsTable.setColumnWidth(0, 100)  # Date
        self.ui.auditLogsTable.setColumnWidth(1, 100)  # User
        self.ui.auditLogsTable.setColumnWidth(2, 200)  # Action

    def setup_connections(self):
        """Setup signal/slot connections"""
        # User management connections
        self.ui.addUserBtn.clicked.connect(self.show_add_user_dialog)
        self.ui.usersTable.itemSelectionChanged.connect(self.on_user_selected)
        self.ui.savePermissionsBtn.clicked.connect(self.save_user_permissions)

        # Register Alt+R action to show Recently Deleted screen
        try:
            action = QAction(self)
            action.setShortcut(QKeySequence("Alt+R"))
            action.triggered.connect(self.show_recently_deleted)
            # Add to widget so shortcut is active
            self.addAction(action)
        except Exception:
            pass
        # Connect recycle button (top-right) to open Recently Deleted dialog
        try:
            if hasattr(self.ui, 'recycleBtn'):
                self.ui.recycleBtn.clicked.connect(self.show_recently_deleted)
        except Exception:
            pass

    def show_recently_deleted(self):
        """Open the Recently Deleted dialog (users and assets)."""
        try:
            # Prefer passing the main window as parent so dialogs can inherit session context
            parent_to_use = getattr(self, 'parent_window', None) or self
            dlg = RecentlyDeletedDialog(parent_to_use)
            dlg.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Recently Deleted: {str(e)}")

    def setup_roles(self):
        """Setup roles in the permissions section"""
        self.role_radio_buttons = {}  # <-- Ensure fresh dict
        self.role_button_group = QButtonGroup()  # <-- Ensure fresh group
        for role in UserRole:
            radio_btn = QRadioButton(role.value)
            # Connect to a handler that updates permissions based on selected radio
            radio_btn.clicked.connect(self.handle_role_changed)
            self.role_button_group.addButton(radio_btn)
            self.role_radio_buttons[role.value] = radio_btn
            self.ui.roleLayout.addWidget(radio_btn)
        
        # Setup permission checkboxes
        for permission in PermissionType:
            checkbox = QCheckBox(permission.value)
            self.permission_checkboxes[permission.value] = checkbox
            self.ui.permissionsCheckboxLayout.addWidget(checkbox)
        
        # Initially disable permissions controls
        self.enable_permissions_controls(False)
    
    def setup_permission_checkboxes(self):
        """Setup permission checkboxes based on PermissionType enum"""
        layout = QVBoxLayout()
        
        # Clear existing checkboxes
        self.permission_checkboxes.clear()
        
        # Create a checkbox for each permission type
        for perm in PermissionType:
            checkbox = QCheckBox(perm.value)
            self.permission_checkboxes[perm.value] = checkbox
            layout.addWidget(checkbox)
        
        # Set the layout
        if self.ui.permissionsScrollArea.widget():
            self.ui.permissionsScrollArea.widget().deleteLater()
        
        widget = QWidget()
        widget.setLayout(layout)
        self.ui.permissionsScrollArea.setWidget(widget)
    
    @Slot()
    def on_role_changed(self, index):
        """Handle role selection change from the role combo box"""
        role_id = self.ui.roleComboBox.itemData(index)
        if role_id:
            # Get permissions for selected role
            permissions = self.role_service.get_role_permissions(role_id)
            
            # Update checkboxes
            for perm_name, checkbox in self.permission_checkboxes.items():
                checkbox.setChecked(perm_name in permissions)
    
    def load_notifications(self):
        """Load system notifications into the notifications list"""
        try:
            self.ui.notificationsList.clear()

            # Show recent successful login events to admin (non-sensitive)
            try:
                logs = self.audit_service.get_audit_logs(limit=50, filters={'action': 'LOGIN_SUCCESS'})
            except Exception:
                logs = []

            if not logs:
                # Fallback friendly message
                self.ui.notificationsList.addItem('No recent login activity')
                return

            for log in logs:
                ts = log.get('timestamp')
                time_str = ''
                if ts:
                    try:
                        t = ts
                        if isinstance(t, str) and t.endswith('Z'):
                            t = t.replace('Z', '+00:00')
                        dt = datetime.fromisoformat(t)
                        time_str = dt.strftime('%Y-%m-%d %H:%M')
                    except Exception:
                        time_str = str(ts)

                username = log.get('username') or (log.get('user') or {}).get('name') or 'Unknown'
                ip = log.get('ip_address')
                item_text = f"{username} logged in at {time_str}"
                if ip:
                    item_text = f"{item_text} ({ip})"
                self.ui.notificationsList.addItem(item_text)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load notifications: {str(e)}")

    @Slot()
    def show_add_user_dialog(self):
        """Show dialog to add a new user"""
        dialog = AddUserDialog(self)
        if dialog.exec():
            self.load_users()  # Refresh the users list

    @Slot()
    def on_user_selected(self):
        """Forwarding wrapper for table selection; actual logic lives in _on_table_user_selected.

        This indirection ensures a single entry point for selection handling and
        avoids duplicate method definitions interfering with Qt auto-connect.
        """
        try:
            self._on_table_user_selected()
        except Exception as e:
            print(f"Error in on_user_selected wrapper: {e}")
    
    def check_admin_permission(self) -> bool:
        """Check if current user has admin permissions"""
        try:
            # Prefer to use the parent window's session token and session service if available
            if hasattr(self, 'parent_window') and self.parent_window is not None:
                try:
                    # Fast check: admin token on main window
                    token = getattr(self.parent_window, '_session_token', None)
                    if isinstance(token, str) and token.startswith('admin-'):
                        return True

                    user_id = None
                    try:
                        user_id = self.parent_window.get_user_id()
                    except Exception:
                        pass

                    username = None
                    try:
                        username = self.parent_window.get_username()
                    except Exception:
                        pass

                    if user_id == 0 or (username and username == "System Admin"):
                        return True

                    if user_id and user_id != 0:
                        return self.role_service.check_permission(user_id, PermissionType.MANAGE_USERS.value)
                except Exception:
                    pass

            # Fallback: use local auth_service if session context not available
            if self.auth_service:
                current_user = self.auth_service.get_current_user()
                if current_user:
                    if (hasattr(current_user, 'id') and current_user.id == 0) or \
                       (hasattr(current_user, 'email') and current_user.email == "admin@company.com"):
                        return True
                    if isinstance(current_user, dict) and current_user.get('email') == "admin@company.com":
                        return True
                user_id = self.auth_service.get_current_user_id()
                if user_id and user_id != 0:
                    return self.role_service.check_permission(user_id, PermissionType.MANAGE_USERS.value)

            return False
        except Exception as e:
            print(f"Permission check error: {e}")
            return False

    def disable_admin_features(self):
        """Disable admin features if user doesn't have permission"""
        self.ui.addUserBtn.setEnabled(False)
        self.ui.usersTable.setEnabled(False)
        self.ui.permissionsScrollArea.setEnabled(False)
        self.ui.savePermissionsBtn.setEnabled(False)

    # Compatibility slots for Qt auto-connect: forwarders to strongly-typed handlers
    @Slot()
    def on_role_changed(self):
        """Compatibility wrapper when Qt tries to auto-connect without index argument."""
        try:
            # Delegate to the handler that reads radio buttons
            self.handle_role_changed()
        except Exception as e:
            print(f"on_role_changed compatibility wrapper error: {e}")

    @Slot('QVariant')
    def on_user_created(self, user_data):
        try:
            # If user_data is a dict-like, forward to our implementation
            if isinstance(user_data, dict):
                return self.handle_user_created(user_data)
            # Otherwise ignore or attempt to coerce
            return self.handle_user_created(dict(user_data))
        except Exception as e:
            print(f"on_user_created compatibility wrapper error: {e}")

    @Slot('QVariant')
    def on_user_updated(self, user_data):
        try:
            if isinstance(user_data, dict):
                return self.handle_user_updated(user_data)
            return self.handle_user_updated(dict(user_data))
        except Exception as e:
            print(f"on_user_updated compatibility wrapper error: {e}")

    def get_audit_logs(self):
        """Get audit logs from the database"""
        # TODO: Implement actual audit log retrieval
        return [
            {'date': datetime.now().strftime('%Y-%m-%d %H:%M'), 'user': 'System', 'action': 'System Started'},
            {'date': datetime.now().strftime('%Y-%m-%d %H:%M'), 'user': 'Admin', 'action': 'User Login'}
        ]

    def get_notifications(self):
        """Get system notifications"""
        # TODO: Implement actual notification retrieval
        return [
            "Welcome to the Admin Dashboard",
            "System is running normally",
            "Database backup completed successfully"
        ]
        self.ui.usersTable.setColumnWidth(4, 150)  # Actions
        
        # Setup audit logs table
        self.ui.auditLogsTable.setColumnWidth(0, 100)  # Date
        self.ui.auditLogsTable.setColumnWidth(1, 100)  # User
        self.ui.auditLogsTable.setColumnWidth(2, 200)  # Action

    def load_users(self):
        """Load users from database"""
        try:
                
            # Clear existing items
            self.ui.usersTable.setRowCount(0)
            
            # Get all users using user service
            result = self.user_service.get_all_users()
            
            if not result:
                # No users found or error occurred
                QMessageBox.warning(self, "Warning", "No users found in the database. Try creating a new user.")
                return
            
            # Get available roles
            roles = self.role_service.get_all_roles()
            
            for user_data in result:
                try:
                    row = self.ui.usersTable.rowCount()
                    self.ui.usersTable.insertRow(row)
                    # Add user data with safe defaults
                    email_item = QTableWidgetItem(str(user_data.get('email', 'N/A')))
                    # Store user id in the email item using Qt.UserRole for retrieval later
                    try:
                        email_item.setData(Qt.UserRole, user_data.get('id'))
                    except Exception:
                        pass
                    self.ui.usersTable.setItem(row, 0, email_item)

                    self.ui.usersTable.setItem(row, 1, QTableWidgetItem(str(user_data.get('name', 'N/A'))))
                    
                    # Add role with combo box
                    role_combo = QComboBox()
                    for role in roles:
                        role_combo.addItem(role["name"], role["id"])
                        if role.get("id") == user_data.get('role_id'):
                            role_combo.setCurrentText(role["name"])

                    # Capture the role_combo and user_id for the lambda to avoid late binding issues
                    user_id_for_cb = user_data.get('id')
                    def _on_role_index_changed(idx, combo=role_combo, uid=user_id_for_cb):
                        role_id = combo.itemData(idx)
                        if uid is not None and role_id is not None:
                            self.update_user_role(uid, role_id)

                    role_combo.currentIndexChanged.connect(_on_role_index_changed)
                    self.ui.usersTable.setCellWidget(row, 2, role_combo)
                    
                    # Status
                    self.ui.usersTable.setItem(row, 3, QTableWidgetItem(str(user_data.get('is_active', 'Active'))))
                    
                    # Style inactive users
                    if user_data.get('is_active') != "Active":
                        for col in range(4):
                            if item := self.ui.usersTable.item(row, col):
                                item.setBackground(QBrush(QColor("#ffebee")))
                    
                    # Add action buttons
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout()
                    
                    edit_btn = QPushButton("Edit")
                    delete_btn = QPushButton("Deactivate")
                    reset_pwd_btn = QPushButton("Reset Password")
                    
                    edit_btn.clicked.connect(lambda checked, u=user_data: self.show_edit_user_dialog(u))
                    delete_btn.clicked.connect(lambda checked, u=user_data: self.delete_user(u))
                    reset_pwd_btn.clicked.connect(lambda checked, u=user_data: self.reset_password(u))
                    
                    actions_layout.addWidget(edit_btn)
                    actions_layout.addWidget(delete_btn)
                    actions_layout.addWidget(reset_pwd_btn)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    
                    actions_widget.setLayout(actions_layout)
                    self.ui.usersTable.setCellWidget(row, 4, actions_widget)
                except Exception as row_error:
                    print(f"Error loading user row: {row_error}")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {str(e)}")
            
    def load_audit_logs(self):
        """Load audit logs from database"""
        try:
            # Clear existing items
            self.ui.auditLogsTable.setRowCount(0)
            
            # TODO: Create AuditLog model and implement actual audit logging
            # For now, we'll show some basic information about users
            with get_db() as session:
                users = session.query(User).order_by(User.created_at.desc()).limit(50)
                
                for user in users:
                    row = self.ui.auditLogsTable.rowCount()
                    self.ui.auditLogsTable.insertRow(row)
                    
                    # Format the timestamp
                    timestamp = user.created_at.strftime("%Y-%m-%d %H:%M")
                    
                    self.ui.auditLogsTable.setItem(row, 0, QTableWidgetItem(timestamp))
                    self.ui.auditLogsTable.setItem(row, 1, QTableWidgetItem("System"))
                    self.ui.auditLogsTable.setItem(row, 2, QTableWidgetItem(f"Created user: {user.name}"))
            # The following lines seem to reference an undefined 'log', so they are commented out or removed.
            # self.ui.auditLogsTable.setItem(row, 1, QTableWidgetItem(log["user"]))
            # self.ui.auditLogsTable.setItem(row, 2, QTableWidgetItem(log["action"]))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load audit logs: {str(e)}")

    def show_deactivated_users_dialog(self):
        # Deprecated: replaced by Recently Deleted dialog (use show_recently_deleted)
        return

    @Slot()
    def show_add_user_dialog(self):
        """Show the add user dialog"""
        dialog = AddUserDialog(self)
        dialog.user_created.connect(self.on_user_created)
        dialog.exec()
        # Refresh the users list after dialog closes
        self.load_users()
    
    def show_edit_user_dialog(self, user_data):
        """Show the edit user dialog with existing user data"""
        # Accept both dict and ORM-like user_data inputs
        edit_data = {}
        if isinstance(user_data, dict):
            edit_data['id'] = user_data.get('id')
            edit_data['name'] = user_data.get('name') or user_data.get('fullname')
            edit_data['email'] = user_data.get('email') or (user_data.get('username', '') + '@company.com')
            edit_data['department'] = user_data.get('department')
            edit_data['position'] = user_data.get('position')
            edit_data['role'] = user_data.get('role')
            edit_data['status'] = user_data.get('is_active') or user_data.get('status')
        else:
            # ORM-like object
            edit_data['id'] = getattr(user_data, 'id', None)
            edit_data['name'] = getattr(user_data, 'name', None)
            edit_data['email'] = getattr(user_data, 'email', None)
            edit_data['department'] = getattr(user_data, 'department', None)
            edit_data['position'] = getattr(user_data, 'position', None)
            # Try to get role name from relationship or role_id
            edit_data['role'] = getattr(user_data, 'role', None)
            if hasattr(edit_data['role'], 'name'):
                edit_data['role'] = edit_data['role'].name.value if hasattr(edit_data['role'].name, 'value') else str(edit_data['role'].name)
            edit_data['status'] = getattr(user_data, 'is_active', None) or getattr(user_data, 'status', None)

        dialog = AddUserDialog(self, edit_data)
        # Connect update signal (AddUserDialog emits user_updated on edit)
        try:
            dialog.user_updated.connect(self.on_user_updated)
        except Exception:
            dialog.user_created.connect(self.on_user_updated)
        dialog.exec()
    
    @Slot(dict)
    def on_user_created(self, user_data):
        """Handle new user creation"""
        try:
            with get_db() as session:
                # Get the role
                role = session.query(Role).filter(Role.name == UserRole(user_data['role'])).first()
                if not role:
                    raise ValueError(f"Invalid role: {user_data['role']}")
                
                # Create new user
                new_user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    department=user_data['department'],
                    position=user_data['position'],
                    role_id=role.id,
                    is_active="Active"
                )
                
                session.add(new_user)
                session.commit()
                
                QMessageBox.information(self, "Success", "User created successfully!")
                self.load_users()  # Refresh the table
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create user: {str(e)}")
    
    @Slot(dict)
    def on_user_updated(self, user_data):
        """Handle user update"""
        try:
            with get_db() as session:
                # Get the user to update
                user = session.query(User).filter(User.id == user_data['id']).first()
                if not user:
                    raise ValueError(f"User not found with ID: {user_data['id']}")
                
                # Get the role
                role = session.query(Role).filter(Role.name == UserRole(user_data['role'])).first()
                if not role:
                    raise ValueError(f"Invalid role: {user_data['role']}")
                
                # Update user
                user.name = user_data['name']
                user.email = user_data['email']
                user.department = user_data['department']
                user.position = user_data['position']
                user.role_id = role.id
                # Normalize status input: support both 'status' and 'is_active'
                status_val = None
                if 'is_active' in user_data:
                    status_val = user_data.get('is_active')
                elif 'status' in user_data:
                    status_val = user_data.get('status')

                # Ensure a default if missing
                if status_val is None:
                    status_val = 'Active'

                # Convert boolean True/False to string values if needed
                if isinstance(status_val, bool):
                    status_val = 'Active' if status_val else 'Inactive'

                user.is_active = status_val
                
                session.commit()
                
                QMessageBox.information(self, "Success", "User updated successfully!")
                self.load_users()  # Refresh the table
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update user: {str(e)}")  # Refresh the table

    def delete_user(self, user_data):
        reply = QMessageBox.question(
            self,
            "Confirm Deactivate",
            f"Are you sure you want to deactivate user {user_data['email']}? This will disable login but preserve audit history.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Use UserService to perform a soft-delete (deactivation)
                res = self.user_service.delete_user(user_data.get('id'))
                if res.get('success'):
                    QMessageBox.information(self, "Success", "User deactivated successfully!")
                    self.load_users()  # Refresh the table
                else:
                    QMessageBox.warning(self, "Warning", res.get('message', 'Failed to deactivate user'))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to deactivate user: {str(e)}")

    def reset_password(self, user_data):
        reply = QMessageBox.question(
            self,
            "Confirm Reset",
            f"Are you sure you want to reset the password for {user_data['email']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with get_db() as session:
                    user = session.query(User).filter(User.id == user_data['id']).first()
                    if user:
                        # TODO: Implement actual password reset mechanism
                        # For now, just show success message
                        QMessageBox.information(self, "Success", "Password has been reset successfully.")
                    else:
                        QMessageBox.warning(self, "Warning", "User not found in database.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to reset password: {str(e)}")
            QMessageBox.information(
                self,
                "Success",
                f"Password has been reset for user {user_data['username']}"
            )
    
    def setup_permissions_frame(self):
        """Setup the permissions frame with role selection and permission checkboxes"""
        # Clear existing widgets
        self.clear_layout(self.ui.roleLayout)
        self.clear_layout(self.ui.checkboxLayout)
        
        # Setup role selection radio buttons
        self.role_button_group = QButtonGroup()
        self.role_radio_buttons = {}
        
        for role in UserRole:
            radio_btn = QRadioButton(role.value)
            radio_btn.clicked.connect(self.on_role_changed)
            self.role_button_group.addButton(radio_btn)
            self.role_radio_buttons[role.value] = radio_btn
            self.ui.roleLayout.addWidget(radio_btn)
        
        # Setup permission checkboxes
        self.permission_checkboxes = {}
        for permission in PermissionType:
            checkbox = QCheckBox(permission.value)
            self.permission_checkboxes[permission.value] = checkbox
            self.ui.checkboxLayout.addWidget(checkbox)
        
        # Initially disable all controls until a user is selected
        self.enable_permissions_controls(False)
    
    def clear_layout(self, layout):
        """Clear all widgets from a layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def enable_permissions_controls(self, enabled):
        """Enable or disable all permission controls"""
        # Role radio buttons
        for radio_btn in self.role_radio_buttons.values():
            radio_btn.setEnabled(enabled)
        
        # Permission checkboxes
        for checkbox in self.permission_checkboxes.values():
            checkbox.setEnabled(enabled)
        
        # Save button
        self.ui.savePermissionsBtn.setEnabled(enabled)
    
    def _on_table_user_selected(self):
        """Unified handler that safely extracts text or widget values from the users table."""
        selected_items = self.ui.usersTable.selectedItems()
        if not selected_items:
            self.current_selected_user = None
            self.ui.selectedUserLabel.setText("Select a user to edit permissions")
            self.enable_permissions_controls(False)
            return

        row = selected_items[0].row()

        def _cell_text(r, c):
            item = self.ui.usersTable.item(r, c)
            if item:
                return item.text()
            widget = self.ui.usersTable.cellWidget(r, c)
            # Common widget used in role column is QComboBox
            try:
                from PySide6.QtWidgets import QComboBox
                if isinstance(widget, QComboBox):
                    return widget.currentText()
            except Exception:
                pass
            return ''

        # Try to retrieve user id stored in the first column's user role data
        user_id = None
        id_item = self.ui.usersTable.item(row, 0)
        if id_item is not None:
            try:
                user_id = id_item.data(Qt.UserRole)
            except Exception:
                user_id = None

        username = _cell_text(row, 0)
        fullname = _cell_text(row, 1)
        role = _cell_text(row, 2)
        status = _cell_text(row, 3)

        self.current_selected_user = {
            'id': user_id,
            'username': username,
            'fullname': fullname,
            'role': role,
            'status': status
        }

        # Update the selected user label
        self.ui.selectedUserLabel.setText(f"Editing permissions for: {fullname} ({username})")

        # Enable controls and load user permissions
        self.enable_permissions_controls(True)
        self.load_user_permissions()
    
    def load_user_permissions(self):
        """Load the permissions for the currently selected user"""
        if not self.current_selected_user:
            return
        
        user_role = self.current_selected_user['role']
        
        # Set the role radio button
        if user_role in self.role_radio_buttons:
            self.role_radio_buttons[user_role].setChecked(True)
        
        # Set default permissions based on role
        self.update_permissions_for_role(user_role)
    
    def update_permissions_for_role(self, role):
        """Update permission checkboxes based on the selected role"""
        # Define default permissions for each role
        role_permissions = {
            'Admin': [perm.value for perm in PermissionType],  # All permissions
            'User': [
                PermissionType.VIEW_ASSET.value,
                PermissionType.CREATE_ASSET.value,
                PermissionType.EDIT_ASSET.value
            ],
            'Viewer': [
                PermissionType.VIEW_ASSET.value,
                PermissionType.VIEW_REPORTS.value
            ]
        }
        
        # Update checkboxes
        for perm_name, checkbox in self.permission_checkboxes.items():
            checkbox.setChecked(perm_name in role_permissions.get(role, []))
    
    @Slot()
    def handle_role_changed(self):
        """Handle role change - update permissions accordingly"""
        # Find which role is selected
        selected_role = None
        for role_name, radio_btn in self.role_radio_buttons.items():
            if radio_btn.isChecked():
                selected_role = role_name
                break
        
        if selected_role:
            self.update_permissions_for_role(selected_role)
    
    @Slot(dict)
    def handle_user_created(self, user_data: dict):
        """Handle when a new user is created"""
        self.load_users()
    
    @Slot(dict)
    def handle_user_updated(self, user_data: dict):
        """Handle when a user is updated"""
        self.load_users()
    
    @Slot()
    def handle_user_selected(self):
        """Handle when a user is selected in the table"""
        selected_items = self.ui.usersTable.selectedItems()
        if not selected_items:
            self.current_selected_user = None
            self.enable_permissions_controls(False)
            return
            
        row = selected_items[0].row()
        # Read internal id stored in Qt.UserRole on the email item (column 0)
        email_item = self.ui.usersTable.item(row, 0)
        user_id = None
        try:
            user_id = email_item.data(Qt.UserRole) if email_item is not None else None
        except Exception:
            user_id = None

        self.current_selected_user = {
            'id': user_id,
            'email': email_item.text() if email_item is not None else None,
            'name': self.ui.usersTable.item(row, 1).text(),
            'role': self.ui.usersTable.item(row, 2).text(),
            'status': self.ui.usersTable.item(row, 3).text()
        }
        self.enable_permissions_controls(True)
        self.load_user_permissions()
    
    @Slot()
    def save_user_permissions(self):
        """Save the current user's role and permissions to the database"""
        if not self.current_selected_user:
            return
            
        try:
            with get_db() as session:
                # Find the user
                user = session.query(User).filter(User.id == self.current_selected_user['id']).first()
                if not user:
                    raise ValueError("Selected user not found in database")
                
                # Get selected role
                selected_role = None
                for role_name, radio_btn in self.role_radio_buttons.items():
                    if radio_btn.isChecked():
                        selected_role = session.query(Role).filter(Role.name == UserRole(role_name)).first()
                        break
                        
                if not selected_role:
                    raise ValueError("No role selected")
                
                # Update user's role
                user.role_id = selected_role.id

                # Ensure Permission rows exist and update/create RolePermission entries
                for perm_enum in PermissionType:
                    # Ensure a Permission row exists for this PermissionType
                    perm = session.query(Permission).filter(Permission.name == perm_enum).first()
                    if not perm:
                        perm = Permission(name=perm_enum)
                        session.add(perm)
                        session.flush()

                    # Find existing RolePermission for this role/permission
                    rp = session.query(RolePermission).filter(
                        RolePermission.role_id == selected_role.id,
                        RolePermission.permission_id == perm.id
                    ).first()

                    checked = False
                    try:
                        checked = self.permission_checkboxes[perm_enum.value].isChecked()
                    except Exception:
                        checked = False

                    if rp:
                        rp.granted = "true" if checked else "false"
                    else:
                        # Create a new RolePermission
                        rp = RolePermission(
                            role_id=selected_role.id,
                            permission_id=perm.id,
                            granted="true" if checked else "false"
                        )
                        session.add(rp)

                session.commit()
                # Debug: print role permissions that were saved for verification
                try:
                    rps = session.query(RolePermission).filter(RolePermission.role_id == selected_role.id).all()
                    perms_debug = []
                    for rp in rps:
                        perm_row = session.query(Permission).filter(Permission.id == rp.permission_id).first()
                        pname = perm_row.name.value if perm_row and hasattr(perm_row.name, 'value') else str(getattr(perm_row, 'name', None))
                        perms_debug.append((pname, rp.granted))
                    logger.info("Saved RolePermissions for role %r: %s", selected_role.id, perms_debug)
                    print(f"Saved RolePermissions for role {selected_role.id}: {perms_debug}")
                except Exception as ex:
                    logger.exception("Failed to dump role permissions after save: %s", ex)

                QMessageBox.information(self, "Success", "User permissions updated successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save permissions: {str(e)}")
            return False
            
        return True
        """Save the current user's permissions"""
        if not self.current_selected_user:
            return
        
        # Get selected role
        selected_role = None
        for role_name, radio_btn in self.role_radio_buttons.items():
            if radio_btn.isChecked():
                selected_role = role_name
                break
        
        # Get selected permissions
        selected_permissions = []
        for perm_name, checkbox in self.permission_checkboxes.items():
            if checkbox.isChecked():
                selected_permissions.append(perm_name)
        
        # TODO: Save to database
        # For now, just update the display
        QMessageBox.information(
            self,
            "Success",
            f"Permissions saved for {self.current_selected_user['fullname']}\n"
            f"Role: {selected_role}\n"
            f"Permissions: {', '.join(selected_permissions)}"
        )
        
        # Update the user's role in the table if it changed
        if selected_role != self.current_selected_user['role']:
            selected_items = self.ui.usersTable.selectedItems()
            if selected_items:
                row = selected_items[0].row()
                self.ui.usersTable.setItem(row, 2, QTableWidgetItem(selected_role))
                self.current_selected_user['role'] = selected_role
