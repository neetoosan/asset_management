from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QScrollArea
from PySide6.QtCore import Qt
from ..ui.notification_screen_ui import Ui_NotificationScreen
from datetime import datetime, timedelta

# Try to import the real AuditService; if unavailable, provide a lightweight fallback
try:
    # Prefer absolute import if project package is available
    from app.services.audit_service import AuditService  # type: ignore
except Exception:
    try:
        # Try a relative import (depending on package layout)
        from ..services.audit_service import AuditService  # type: ignore
    except Exception:
        # Fallback stub to avoid NameError during development or tests
        class AuditService:
            def __init__(self, *args, **kwargs):
                pass

            def get_table_changes(self, table_name, limit=100):
                # Return an empty list when the real audit service is not present
                return []

class NotificationScreen(QWidget):
    """Notification screen widget for the asset management system"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_NotificationScreen()
        self.ui.setupUi(self)
        
        # Initialize notifications data
        self.notifications_data = {
            'today': [],
            'yesterday': [],
            'last_week': [],
            'all': []
        }
        
        # Audit service to pull notifications from DB
        self.audit_service = AuditService()
        
        # Connect tab change signal
        self.ui.notificationTabs.currentChanged.connect(self.on_tab_changed)
        
        # Load notifications
        self.load_notifications()
        
        # Show today's notifications by default
        self.show_notifications_for_tab('today')
    
    def load_notifications(self):
        """Load notifications from database or service"""
        # TODO: Replace with actual notification service call
        # For now, we'll create some sample notifications
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)
        
        sample_notifications = [
            {
                'id': 1,
                'title': 'Asset Due for Maintenance',
                'message': 'Computer Equipment (ID: CMP001) is due for scheduled maintenance.',
                'timestamp': now - timedelta(hours=2),
                'type': 'maintenance',
                'read': False
            },
            {
                'id': 2,
                'title': 'Asset Expiry Warning',
                'message': 'Software License (ID: SW001) will expire in 30 days.',
                'timestamp': now - timedelta(hours=5),
                'type': 'warning',
                'read': False
            },
            {
                'id': 3,
                'title': 'New Asset Added',
                'message': 'Office Chair (ID: OF012) has been successfully added to the system.',
                'timestamp': yesterday - timedelta(hours=3),
                'type': 'info',
                'read': True
            },
            {
                'id': 4,
                'title': 'Asset Transfer Completed',
                'message': 'Laptop (ID: LPT005) has been transferred to IT Department.',
                'timestamp': yesterday - timedelta(hours=8),
                'type': 'success',
                'read': True
            },
            {
                'id': 5,
                'title': 'Depreciation Alert',
                'message': 'Vehicle (ID: VH003) has reached 80% depreciation.',
                'timestamp': last_week - timedelta(hours=12),
                'type': 'warning',
                'read': True
            }
        ]
        
        # Categorize notifications by date
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = last_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        for notification in sample_notifications:
            self.notifications_data['all'].append(notification)
            
            if notification['timestamp'] >= today_start:
                self.notifications_data['today'].append(notification)
            elif notification['timestamp'] >= yesterday_start:
                self.notifications_data['yesterday'].append(notification)
            elif notification['timestamp'] >= week_start:
                self.notifications_data['last_week'].append(notification)
        
        # Pull recent asset-related audit logs and build notifications
        try:
            logs = self.audit_service.get_table_changes('assets', limit=200)
        except Exception as e:
            print(f"Error fetching audit logs for notifications: {e}")
            logs = []

        # Reset
        self.notifications_data = {k: [] for k in self.notifications_data}

        # Helper to parse timestamp strings returned by AuditService
        def _parse_ts(ts):
            if not ts:
                return datetime.now()
            try:
                # AuditService returns ISO timestamp string
                if isinstance(ts, str):
                    # Support trailing Z
                    if ts.endswith('Z'):
                        ts = ts.replace('Z', '+00:00')
                    return datetime.fromisoformat(ts)
                if isinstance(ts, datetime):
                    return ts
            except Exception:
                pass
            return datetime.now()

        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)

        for log in logs:
            # Build a user-facing notification from audit log
            action = (log.get('action') or '').upper()
            title = None
            ntype = 'info'
            asset_name = None
            asset_external_id = None

            # Try to get asset info from new_values or old_values
            vals = log.get('new_values') or log.get('old_values') or {}
            if isinstance(vals, dict):
                asset_name = vals.get('name')
                asset_external_id = vals.get('asset_id') or vals.get('assetId')

            if action in ('ASSET_CREATED', 'CREATE'):
                title = f"Asset added: {asset_name or 'Unknown'}"
                ntype = 'success'
                message = f"{asset_name or ''} (ID: {asset_external_id or log.get('record_id')}) was added."
            elif action in ('ASSET_UPDATED', 'UPDATE'):
                title = f"Asset updated: {asset_name or 'Unknown'}"
                ntype = 'maintenance'
                message = f"{asset_name or ''} (ID: {asset_external_id or log.get('record_id')}) was updated."
            elif action in ('ASSET_DELETED', 'DELETE'):
                title = f"Asset deleted: {asset_name or 'Unknown'}"
                ntype = 'error'
                message = f"{asset_name or ''} (ID: {asset_external_id or log.get('record_id')}) was deleted."
            elif action in ('ASSET_RESTORED',):
                title = f"Asset restored: {asset_name or 'Unknown'}"
                ntype = 'success'
                message = f"{asset_name or ''} (ID: {asset_external_id or log.get('record_id')}) was restored."
            else:
                # Skip unrelated actions
                continue

            ts = _parse_ts(log.get('timestamp'))
            notif = {
                'id': log.get('id'),
                'title': title,
                'message': message,
                'timestamp': ts,
                'type': ntype,
                'read': False
            }

            self.notifications_data['all'].append(notif)
            if ts >= today_start:
                self.notifications_data['today'].append(notif)
            elif ts >= yesterday_start:
                self.notifications_data['yesterday'].append(notif)
            elif ts >= week_start:
                self.notifications_data['last_week'].append(notif)
    
    def on_tab_changed(self, index):
        """Handle tab change event"""
        tab_names = ['today', 'yesterday', 'last_week', 'all']
        if 0 <= index < len(tab_names):
            tab_name = tab_names[index]
            self.show_notifications_for_tab(tab_name)
    
    def show_notifications_for_tab(self, tab_name):
        """Show notifications for the specified tab"""
        notifications = self.notifications_data.get(tab_name, [])
        
        # Get the appropriate scroll content widget
        if tab_name == 'today':
            scroll_content = self.ui.todayScrollContent
            layout = self.ui.todayContentLayout
            placeholder = self.ui.todayPlaceholder
        elif tab_name == 'yesterday':
            scroll_content = self.ui.yesterdayScrollContent
            layout = self.ui.yesterdayContentLayout
            placeholder = self.ui.yesterdayPlaceholder
        elif tab_name == 'last_week':
            scroll_content = self.ui.lastWeekScrollContent
            layout = self.ui.lastWeekContentLayout
            placeholder = self.ui.lastWeekPlaceholder
        else:  # all
            scroll_content = self.ui.allScrollContent
            layout = self.ui.allContentLayout
            placeholder = self.ui.allPlaceholder
        
        # Clear existing notification widgets (but keep placeholder and spacer)
        self.clear_notifications_from_layout(layout, placeholder)
        
        if notifications:
            # Hide placeholder
            placeholder.hide()
            
            # Add notification widgets
            for notification in notifications:
                notification_widget = self.create_notification_widget(notification)
                # Insert before the spacer (which should be the last item)
                layout.insertWidget(layout.count() - 1, notification_widget)
        else:
            # Show placeholder
            placeholder.show()
    
    def clear_notifications_from_layout(self, layout, placeholder):
        """Clear notification widgets from layout, keeping placeholder and spacer"""
        items_to_remove = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget() and item.widget() != placeholder:
                widget = item.widget()
                if hasattr(widget, 'notification_id'):  # This is a notification widget
                    items_to_remove.append((i, widget))
        
        # Remove items in reverse order to maintain indices
        for i, widget in reversed(items_to_remove):
            layout.removeWidget(widget)
            widget.deleteLater()
    
    def get_notification_frame_style(self, notification):
        """Get the style for a notification frame based on its type and read status"""
        base_style = """
            QFrame {
                border: 1px solid #2974c4;
                border-radius: 8px;
                margin: 4px 0;
            }
            QFrame:hover {
                border-color: #bdc3c7;
            }
        """
        
        if not notification['read']:
            base_style = """
                QFrame {
                    border: 1px solid #2974c4;
                    border-radius: 8px;
                    margin: 4px 0;
                }
                QFrame:hover {
                    border-color: #2974c4;
                }
            """
        
        # Add left border color based on notification type
        type_colors = {
            'warning': '#f1c40f',
            'maintenance': '#3498db',
            'info': '#2ecc71',
            'success': '#27ae60',
            'error': '#e74c3c'
        }
        
        border_color = type_colors.get(notification['type'], '#95a5a6')
        return f"{base_style} QFrame {{ border-left: 4px solid {border_color}; }}"

    def create_notification_widget(self, notification):
        """Create a widget for displaying a single notification"""
        notification_frame = QFrame()
        notification_frame.notification_id = notification['id']
        notification_frame.setProperty("notification", True)
        notification_frame.setProperty("unread", not notification['read'])
        notification_frame.setProperty("type", notification['type'])
        
        layout = QVBoxLayout(notification_frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        
        # Title
        title_label = QLabel(notification['title'])
        title_label.setProperty("role", "notification-title")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(notification['message'])
        message_label.setProperty("role", "notification-message")
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Time and type info
        info_text = f"{self.format_timestamp(notification['timestamp'])} • {notification['type'].title()}"
        info_label = QLabel(info_text)
        info_label.setProperty("role", "notification-time")
        layout.addWidget(info_label)
        
        return notification_frame
    
    def format_timestamp(self, timestamp):
        """Format timestamp for display"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days == 0:
            if diff.seconds < 3600:  # Less than 1 hour
                minutes = diff.seconds // 60
                return f"{minutes}m ago" if minutes > 0 else "Just now"
            else:  # Less than 24 hours
                hours = diff.seconds // 3600
                return f"{hours}h ago"
        elif diff.days == 1:
            return "Yesterday " + timestamp.strftime("%H:%M")
        elif diff.days < 7:
            return f"{diff.days}d ago"
        else:
            return timestamp.strftime("%m/%d/%Y")
    
    def mark_notification_as_read(self, notification_id):
        """Mark a notification as read"""
        # TODO: Implement database update
        for category in self.notifications_data.values():
            for notification in category:
                if notification['id'] == notification_id:
                    notification['read'] = True
        
        # Refresh current tab
        current_tab_index = self.ui.notificationTabs.currentIndex()
        self.on_tab_changed(current_tab_index)
