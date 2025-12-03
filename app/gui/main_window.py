from typing import Optional
from datetime import datetime
from PySide6.QtWidgets import QMainWindow, QMessageBox, QDialog
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut, QPixmap
from .ui.main_window_ui import Ui_MainWindow
from .dialogs.asset_dialog import AssetDialog
from .views.asset_table_view import AssetTableView
from ..services.asset_service import AssetService
from ..services.session_service import SessionService
from ..services.user_service import UserService
from ..services.audit_service import set_global_audit_user

class MainWindow(QMainWindow):
    # Signal emitted when logout is requested
    logoutRequested = Signal()
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Configure responsive window sizing
        try:
            from PySide6.QtGui import QGuiApplication
            screen = QGuiApplication.primaryScreen()
            if screen:
                avail = screen.availableGeometry()
                
                # Set window to 85% of available screen space
                default_width = int(avail.width() * 0.85)
                default_height = int(avail.height() * 0.85)
                
                # Ensure minimum window size
                min_width = 1000
                min_height = 700
                
                # Set actual size
                actual_width = max(min_width, min(default_width, avail.width() - 40))
                actual_height = max(min_height, min(default_height, avail.height() - 80))
                
                # Set window size and position (centered on screen)
                self.resize(actual_width, actual_height)
                center_x = avail.x() + (avail.width() - actual_width) // 2
                center_y = avail.y() + (avail.height() - actual_height) // 2
                self.move(center_x, center_y)
                
                # Allow window to be resized and maximized
                self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
                self.setAttribute(Qt.WA_AlwaysStackOnTop, False)
        except Exception as e:
            print(f"Warning: Could not configure window geometry: {e}")
            # Fallback to default sizing
            self.resize(1400, 850)
        
        self.asset_service = AssetService()
        self.user_service = UserService()
        self.session_service = SessionService()
        
    def initialize_session(self, session_token):
        """Initialize the session with the provided token"""
        if not session_token:
            print("No session token provided")  # Debug logging
            raise ValueError("Session token is required")
            
        print(f"Initializing session with token: {session_token}")  # Debug logging
            
        # Store the session token
        self._session_token = session_token
        
        # Set session token in session service
        self.session_service._session_token = session_token
        
        # Verify and activate the session
        if not self.session_service.validate_session(session_token):
            print("Session validation failed")  # Debug logging
            raise ValueError("Invalid session token")

        # Populate session_service current user context where possible so
        # other components using the main window's session_service (dialogs, services)
        # can access current user information (especially for admin- tokens)
        try:
            from ..services.auth_service import AuthService
            auth = AuthService()
            user_data = auth.validate_session(session_token)
            if user_data:
                # auth.validate_session returns a dict for DB users
                self.session_service._current_user = user_data
                self.session_service._login_time = getattr(self.session_service, '_login_time', None) or datetime.utcnow()
                self.session_service._last_activity = getattr(self.session_service, '_last_activity', None) or datetime.utcnow()
            else:
                # For admin tokens, construct minimal admin user context
                if isinstance(session_token, str) and session_token.startswith('admin-'):
                    self.session_service._current_user = {
                        'id': 0,
                        'name': 'System Admin',
                        'email': 'admin@company.com',
                        'role': 'Admin',
                        'is_active': 'Active'
                    }
                    self.session_service._login_time = datetime.utcnow()
                    self.session_service._last_activity = datetime.utcnow()
        except Exception:
            # Non-fatal: if we cannot populate current_user, components will fallback to token checks
            pass
        
        # Initialize UI state
        self.is_asset_menu_expanded = False
        
        # Hide asset submenu initially
        self.ui.assetScrollArea.hide()
        
        # Configure scrolling behavior for asset scroll area
        self.ui.assetScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.assetScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.assetScrollArea.setMaximumHeight(400)  # Limit maximum height
        self.ui.assetScrollArea.setMinimumHeight(100)  # Ensure minimum height
        
        # Setup the base UI
        self.setup_logo()
        
        # Set up base connections
        self.setup_connections()
        
        # Set up the interface after session is verified
        self.setup_ui_post_auth()
        # Ensure services know who the current user is for audit/permission checks
        try:
            uid = self.get_user_id()
            uname = self.get_username()
            if uid is not None:
                try:
                    # Propagate current user to services for permission checks and audit
                    self.asset_service.set_current_user(uid or 0, uname or 'System')
                except Exception:
                    pass
                try:
                    self.user_service.set_current_user(uid or 0, uname or 'System')
                except Exception:
                    pass
                try:
                    # Set the module-level global for AuditService so new instances
                    # created elsewhere will inherit the current user context.
                    set_global_audit_user(uid or 0, uname or 'System')
                except Exception:
                    pass
        except Exception:
            pass
        
    def is_authenticated(self) -> bool:
        """Check if the current session is authenticated"""
        return hasattr(self, '_session_token') and bool(self._session_token)
        
    def get_user_id(self) -> Optional[int]:
        """Get the current user's ID from the session"""
        if hasattr(self, '_session_token'):
            # For admin session
            if self._session_token.startswith('admin-'):
                return 0
            # For regular user session
            session_data = self.session_service.get_session_data(self._session_token)
            return session_data.get('user_id') if session_data else None
        return None
        
    def get_username(self) -> Optional[str]:
        """Get the current user's username from the session"""
        if hasattr(self, '_session_token'):
            # For admin session
            if self._session_token.startswith('admin-'):
                return "System Admin"
            # For regular user session
            session_data = self.session_service.get_session_data(self._session_token)
            return session_data.get('username') if session_data else None
        return None
        

        
    def setup_ui_post_auth(self):
        """Set up the UI after authentication is confirmed"""
        # Set initial page
        self.show_dashboard()

    def setup_logo(self):
        """Setup and scale the logo properly"""
        try:
            import os
            
            # Ensure logoLabel exists and is visible
            if not hasattr(self.ui, 'logoLabel'):
                print("Error: logoLabel not found in UI")
                return
            
            # Make sure the label is visible
            self.ui.logoLabel.show()
            
            # Construct absolute path from the config base directory
            logo_path = os.path.join(self.config.BASE_DIR, "app", "static", "images", "logo.png")
            
            # Verify file exists before attempting to load
            if not os.path.exists(logo_path):
                print(f"[Logo] File not found at: {logo_path}")
                self.ui.logoLabel.setText("RHV")
                self.ui.logoLabel.setAlignment(Qt.AlignCenter)
                return
            
            print(f"[Logo] Attempting to load from: {logo_path}")
            original_pixmap = QPixmap(logo_path)
            
            if original_pixmap.isNull():
                print(f"[Logo] Failed to load pixmap (null) from: {logo_path}")
                self.ui.logoLabel.setText("RHV")
                self.ui.logoLabel.setAlignment(Qt.AlignCenter)
                return
            
            print(f"[Logo] Original pixmap size: {original_pixmap.width()}x{original_pixmap.height()}")
            
            # Get the logo frame size
            frame_width = 170   # Available width in logo frame
            frame_height = 45   # Available height in logo frame
            
            # Scale the logo to fit within the frame while maintaining aspect ratio
            scaled_pixmap = original_pixmap.scaledToHeight(
                frame_height,
                Qt.SmoothTransformation
            )
            
            print(f"[Logo] Scaled pixmap size: {scaled_pixmap.width()}x{scaled_pixmap.height()}")
            
            # Set the pixmap with explicit properties
            self.ui.logoLabel.setPixmap(scaled_pixmap)
            self.ui.logoLabel.setAlignment(Qt.AlignCenter)
            self.ui.logoLabel.setScaledContents(False)
            
            # Ensure minimum height for label
            self.ui.logoLabel.setMinimumHeight(40)
            
            print(f"[Logo] Successfully loaded and displayed")
                
        except Exception as e:
            import traceback
            print(f"[Logo] Error loading logo: {e}")
            traceback.print_exc()
            try:
                # Fallback text on error
                self.ui.logoLabel.setText("RHV")
                self.ui.logoLabel.setAlignment(Qt.AlignCenter)
            except Exception as e2:
                print(f"[Logo] Error setting fallback text: {e2}")

    def setup_connections(self):
        # Connect nav buttons
        self.ui.dashboardBtn.clicked.connect(self.show_dashboard)
        self.ui.assetsBtn.clicked.connect(self.toggle_asset_menu)
        self.ui.reportsBtn.clicked.connect(self.show_reports)
        self.ui.adminBtn.clicked.connect(self.show_admin)
        self.ui.notificationsBtn.clicked.connect(self.show_notifications)
        self.ui.settingsBtn.clicked.connect(self.show_settings)
        
        # Connect "All Assets" button
        self.ui.allAssetsBtn.clicked.connect(lambda: self.show_asset_category("all"))
        
        # Connect asset management buttons
        self.ui.addAssetBtn.clicked.connect(self.show_add_asset_dialog)
        
        # Connect logout button and shortcut
        self.ui.logoutBtn.clicked.connect(self.logout)
        logout_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        logout_shortcut.activated.connect(self.logout)
        
        # Load dynamic category buttons
        self.load_category_buttons()
    
    def load_category_buttons(self):
        """Load category buttons dynamically from database"""
        try:
            # Clear existing category buttons (keep All Assets button)
            layout = self.ui.assetSubMenu.layout()
            while layout.count() > 1:  # Keep first item (All Assets button)
                item = layout.takeAt(1)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Load categories from database
            with self.asset_service.get_session() as session:
                categories = self.asset_service.get_all_categories(session)
                
                # Add category buttons
                for category in categories:
                    category_name = category.get('name', '')
                    btn = self._create_category_button(category_name)
                    layout.addWidget(btn)
        except Exception as e:
            print(f"Error loading category buttons: {e}")
    
    def _create_category_button(self, category_name: str):
        """Create a category button with the given name"""
        from PySide6.QtWidgets import QPushButton
        
        btn = QPushButton(category_name)
        btn.setStyleSheet("color: white; text-align: left; padding: 8px;")
        btn.clicked.connect(lambda: self.show_asset_category(category_name))
        return btn

    @Slot()
    def show_dashboard(self):
        from .views.dashboard_screen import DashboardScreen
        
        # Clear any existing widgets in the dashboard page
        while self.ui.dashboardPage.layout() and self.ui.dashboardPage.layout().count():
            child = self.ui.dashboardPage.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create and add the dashboard screen
        dashboard_screen = DashboardScreen(self)
        if not self.ui.dashboardPage.layout():
            from PySide6.QtWidgets import QVBoxLayout
            self.ui.dashboardPage.setLayout(QVBoxLayout())
        self.ui.dashboardPage.layout().addWidget(dashboard_screen)
        
        # Show the dashboard page
        self.ui.contentStack.setCurrentIndex(0)
        self.update_nav_style(0)

    @Slot()
    def toggle_asset_menu(self):
        self.is_asset_menu_expanded = not self.is_asset_menu_expanded
        self.ui.assetScrollArea.setVisible(self.is_asset_menu_expanded)
        self.ui.assetsBtn.setText("Assets ▼" if not self.is_asset_menu_expanded else "Assets ▲")
        
        # Adjust scroll area height based on content
        if self.is_asset_menu_expanded:
            content_height = self.ui.assetSubMenu.sizeHint().height()
            viewport_height = min(400, content_height)  # Max height of 400px
            self.ui.assetScrollArea.setFixedHeight(viewport_height)

    @Slot(str)
    def show_asset_category(self, category):
        self.ui.contentStack.setCurrentIndex(1)
        self.update_nav_style(1)
        
        # Clear any existing widgets in the assets page
        while self.ui.assetsPage.layout() and self.ui.assetsPage.layout().count():
            child = self.ui.assetsPage.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Use category name directly from database
        display_name = 'All Assets' if category == 'all' else category
        
        # Create and add the asset table view
        table_view = AssetTableView(display_name, category, self)
        if not self.ui.assetsPage.layout():
            from PySide6.QtWidgets import QVBoxLayout
            self.ui.assetsPage.setLayout(QVBoxLayout())
        self.ui.assetsPage.layout().addWidget(table_view)
        
        # Load assets from database
        self.load_assets_for_category(table_view, category)

    @Slot()
    def show_notifications(self):
        from .views.notification_screen import NotificationScreen
        
        # Clear any existing widgets in the notifications page
        while self.ui.notificationsPage.layout() and self.ui.notificationsPage.layout().count():
            child = self.ui.notificationsPage.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create and add the notification screen
        notification_screen = NotificationScreen(self)
        if not self.ui.notificationsPage.layout():
            from PySide6.QtWidgets import QVBoxLayout
            self.ui.notificationsPage.setLayout(QVBoxLayout())
        self.ui.notificationsPage.layout().addWidget(notification_screen)
        
        # Show the notifications page
        self.ui.contentStack.setCurrentIndex(2)
        self.update_nav_style(4)  # Update to highlight the notifications button

    @Slot()
    def show_settings(self):
        from .views.setting_screen import SettingScreen
        
        # Clear any existing widgets in the settings page
        while self.ui.settingsPage.layout() and self.ui.settingsPage.layout().count():
            child = self.ui.settingsPage.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create and add the settings screen
        settings_screen = SettingScreen(self)
        if not self.ui.settingsPage.layout():
            from PySide6.QtWidgets import QVBoxLayout
            self.ui.settingsPage.setLayout(QVBoxLayout())
        self.ui.settingsPage.layout().addWidget(settings_screen)
        
        # Show the settings page
        self.ui.contentStack.setCurrentIndex(3)
        self.update_nav_style(5)  # Update to highlight the settings button
        
    def load_assets_for_category(self, table_view, category):
        """Load assets from database for the specified category"""
        try:
            if category == 'all':
                assets = self.asset_service.get_all_assets()
            else:
                # Query assets by category name directly
                assets = self.asset_service.get_assets_by_category_name(category)
            
            # Convert database assets to format expected by table view
            asset_data = []
            for asset in assets:
                # support both dicts (from service) and ORM objects
                if isinstance(asset, dict):
                    acq = asset.get('acquisition_date')
                    date_registered = ''
                    if acq:
                        try:
                            if isinstance(acq, str):
                                date_registered = datetime.fromisoformat(acq).strftime('%Y-%m-%d')
                            elif isinstance(acq, datetime):
                                date_registered = acq.strftime('%Y-%m-%d')
                            else:
                                date_registered = str(acq)
                        except Exception:
                            date_registered = str(acq)

                    asset_data.append({
                        'id': asset.get('id'),
                        'asset_id': asset.get('asset_id'),
                        'name': asset.get('name'),
                        'model_number': asset.get('model_number'),
                        'serial_number': asset.get('serial_number'),
                        'location': asset.get('location'),
                        # Use location as the value displayed in the table's
                        # department column (location is the combo selection).
                        'department': asset.get('location') or asset.get('department') or 'Not Assigned',
                        'category': asset.get('category_name') or asset.get('category') or 'Unknown',
                        'date_registered': date_registered,
                        'expiry_date': asset.get('expiry_date') or self.calculate_expiry_date(asset),
                        'value': float(asset.get('total_cost', 0)),
                        'status': asset.get('status') if asset.get('status') else 'Unknown'
                    })
                else:
                    # For ORM objects, use expiry_date from database if available, else calculate
                    expiry = getattr(asset, 'expiry_date', None)
                    if expiry:
                        expiry_str = expiry.strftime('%Y-%m-%d') if hasattr(expiry, 'strftime') else str(expiry)
                    else:
                        expiry_str = self.calculate_expiry_date(asset)
                    
                    asset_data.append({
                        'id': asset.id,  # Database ID for edit/delete operations
                        'asset_id': asset.asset_id,  # User-defined asset ID for display
                        'name': asset.name,
                        'model_number': getattr(asset, 'model_number', '') if hasattr(asset, 'model_number') else '',
                        'serial_number': getattr(asset, 'serial_number', '') if hasattr(asset, 'serial_number') else '',
                        'location': getattr(asset, 'location', '') if hasattr(asset, 'location') else '',
                        # Prefer location (combo selection) for the table column
                        'department': (getattr(asset, 'location', None) or asset.department or 'Not Assigned'),
                        'category': asset.category.name if asset.category else 'Unknown',
                        'date_registered': asset.acquisition_date.strftime('%Y-%m-%d') if asset.acquisition_date else '',
                        'expiry_date': expiry_str,
                        'value': float(asset.total_cost or 0),
                        'status': asset.status.value if asset.status else 'Unknown'
                    })
            
            table_view.load_assets(asset_data)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load assets: {str(e)}")
    
    def calculate_expiry_date(self, asset):
        """Calculate expiry date based on acquisition date and useful life"""
        # Support both dicts and ORM objects
        acq_date = None
        useful_life = None
        if isinstance(asset, dict):
            acq_date = asset.get('acquisition_date')
            useful_life = asset.get('useful_life')
        else:
            acq_date = getattr(asset, 'acquisition_date', None)
            useful_life = getattr(asset, 'useful_life', None)

        if acq_date and useful_life:
            from datetime import timedelta
            try:
                expiry_date = acq_date + timedelta(days=useful_life * 365)
                return expiry_date.strftime('%Y-%m-%d')
            except Exception:
                pass
        return ''

    @Slot()
    def show_add_asset_dialog(self):
        # Use the main window's session service so dialogs share the authenticated context
        session_service = getattr(self, 'session_service', None)
        if session_service is None:
            from ..services.session_service import SessionService
            session_service = SessionService()

        dialog = AssetDialog(session_service, None, self)  # None for new asset
        if dialog.exec():
            try:
                # Refresh current asset view if showing assets
                if self.ui.contentStack.currentIndex() == 1:  # Assets page
                    # Find the current table view and refresh it
                    layout = self.ui.assetsPage.layout()
                    if layout and layout.count() > 0:
                        table_view = layout.itemAt(0).widget()
                        if isinstance(table_view, AssetTableView):
                            # Get the current category from the table view
                            current_category = getattr(table_view, 'category', 'all')
                            self.load_assets_for_category(table_view, current_category)
                            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to refresh asset view: {str(e)}")
    
    def show_edit_asset_dialog(self, asset_id: int):
        """Show dialog to edit an existing asset"""
        try:
            # Use existing session service from main window if available
            session_service = getattr(self, 'session_service', None)
            if session_service is None:
                from ..services.session_service import SessionService
                session_service = SessionService()

            # Get the asset from database
            # Pass the asset id directly; the dialog will fetch a fresh copy to avoid
            # passing detached ORM instances or stale objects across sessions.
            dialog = AssetDialog(session_service, asset_id, self)
            if dialog.exec():
                # Refresh current asset view if showing assets
                self.refresh_current_asset_view()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit asset: {str(e)}")
    
    def delete_asset(self, asset_id: int, asset_name: str, permanent: bool = False):
        """Delete an asset with confirmation

        By default this performs a soft-delete (retire). If `permanent=True`
        the asset will be permanently removed. Calls into AssetService which
        handles permission checks and audit logging.
        """
        try:
            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete asset '{asset_name}'?\n\n"
                f"This action cannot be undone if performed permanently.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Ask for deletion reason via dialog
                try:
                    from .dialogs.asset_delete_reason_dialog import AssetDeleteReasonDialog
                except Exception:
                    # Fallback: import from package path
                    from app.gui.dialogs.asset_delete_reason_dialog import AssetDeleteReasonDialog

                reason_dialog = AssetDeleteReasonDialog(self)
                if reason_dialog.exec() != QDialog.Accepted:
                    QMessageBox.information(self, "Cancelled", "Deletion cancelled")
                    return
                reason = reason_dialog.get_reason()
                if not reason:
                    QMessageBox.warning(self, "Reason Required", "You must provide a reason for deleting an asset.")
                    return

                # Delete the asset with reason
                # Ensure the asset service knows who is performing the action
                try:
                    uid = self.get_user_id()
                    uname = self.get_username()
                    if uid is not None:
                        try:
                            self.asset_service.set_current_user(uid or 0, uname or 'System')
                        except Exception:
                            pass
                        try:
                            self.user_service.set_current_user(uid or 0, uname or 'System')
                        except Exception:
                            pass
                except Exception:
                    pass

                # Ensure we pass through the requested permanence flag so
                # callers (like Recently Deleted) can perform permanent
                # deletes, while deletes from the main asset table default
                # to soft-delete.
                result = self.asset_service.delete_asset(asset_id, reason=reason, permanent=permanent)

                if result["success"]:
                    QMessageBox.information(self, "Success", result["message"])
                    # Refresh current asset view. Use a direct reload of the
                    # active table view to ensure retired assets are removed
                    # from the main listing immediately and appear in Recently Deleted.
                    try:
                        if self.ui.contentStack.currentIndex() == 1:  # Assets page
                            layout = self.ui.assetsPage.layout()
                            if layout and layout.count() > 0:
                                table_view = layout.itemAt(0).widget()
                                if isinstance(table_view, AssetTableView):
                                    current_category = getattr(table_view, 'category', 'all')
                                    # Load assets for this category (forces fresh DB read)
                                    self.load_assets_for_category(table_view, current_category)
                                else:
                                    # Fallback to generic refresh
                                    self.refresh_current_asset_view()
                            else:
                                self.refresh_current_asset_view()
                        else:
                            self.refresh_current_asset_view()
                    except Exception as e:
                        print(f"Error refreshing asset view after delete: {e}")
                else:
                    QMessageBox.warning(self, "Error", result["message"])
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete asset: {str(e)}")
    
    def refresh_current_asset_view(self):
        """Refresh the current asset table view"""
        try:
            # If the assets page is active, force a full reload of the assets
            # page to ensure any status changes (soft-deletes) are reflected.
            if self.ui.contentStack.currentIndex() == 1:  # Assets page
                layout = self.ui.assetsPage.layout()
                if layout and layout.count() > 0:
                    table_view = layout.itemAt(0).widget()
                    if isinstance(table_view, AssetTableView):
                        current_category = getattr(table_view, 'category', 'all')
                        # Recreate the assets page for a clean refresh. This
                        # avoids stale widget state and forces the service to
                        # re-query the database for current rows.
                        try:
                            self.show_asset_category(current_category)
                            return
                        except Exception:
                            # Fallback to the previous behavior if recreation fails
                            self.load_assets_for_category(table_view, current_category)
        except Exception as e:
            print(f"Error refreshing asset view: {e}")

    @Slot()
    def show_reports(self):
        from .views.report_screen import ReportScreen
        
        # Clear any existing widgets in the reports page
        while self.ui.reportsPage.layout() and self.ui.reportsPage.layout().count():
            child = self.ui.reportsPage.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create and add the report screen
        report_screen = ReportScreen(self)
        if not self.ui.reportsPage.layout():
            from PySide6.QtWidgets import QVBoxLayout
            self.ui.reportsPage.setLayout(QVBoxLayout())
        self.ui.reportsPage.layout().addWidget(report_screen)
        
        # Show the reports page
        self.ui.contentStack.setCurrentIndex(4)  # Reports page index
        self.update_nav_style(2)  # Update to highlight the reports button
    
    @Slot()
    def show_admin(self):
        from .views.admin_screen import AdminScreen
        
        # Clear any existing widgets in the admin page
        while self.ui.adminPage.layout() and self.ui.adminPage.layout().count():
            child = self.ui.adminPage.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create and add the admin screen
        admin_screen = AdminScreen(self)
        if not self.ui.adminPage.layout():
            from PySide6.QtWidgets import QVBoxLayout
            self.ui.adminPage.setLayout(QVBoxLayout())
        self.ui.adminPage.layout().addWidget(admin_screen)
        
        # Show the admin page
        self.ui.contentStack.setCurrentIndex(5)  # Admin page index
        self.update_nav_style(3)  # Update to highlight the admin button
    
    @Slot()
    def logout(self):
        """Handle logout functionality"""
        reply = QMessageBox.question(
            self, 
            "Logout", 
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.logoutRequested.emit()
            self.hide()
    
    def update_nav_style(self, active_index):
        buttons = [
            self.ui.dashboardBtn,
            self.ui.assetsBtn,
            self.ui.reportsBtn,
            self.ui.adminBtn,
            self.ui.notificationsBtn,
            self.ui.settingsBtn
        ]
        for i, btn in enumerate(buttons):
            if i == active_index:
                btn.setStyleSheet("""
                    background-color: #34495e;
                    color: white;
                    padding: 10px;
                    text-align: left;
                    border-left: 3px solid #3498db;
                """)
            else:
                btn.setStyleSheet("""
                    color: white;
                    padding: 10px;
                    text-align: left;
                    border: none;
                """)