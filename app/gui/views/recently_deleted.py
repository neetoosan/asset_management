from PySide6.QtWidgets import QDialog, QTableWidgetItem
from PySide6.QtCore import Qt
from ..ui.recently_deleted_ui import Ui_RecentlyDeleted
from ...core.database import get_db
from ...core.models import User, Asset, AssetStatus
from ...services.user_service import UserService
from ...services.asset_service import AssetService
from ...services.audit_service import set_global_audit_user
from PySide6.QtWidgets import QMessageBox

class RecentlyDeletedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_RecentlyDeleted()
        self.ui.setupUi(self)
        self.ui.closeBtn.clicked.connect(self.accept)
        self.ui.restoreBtn.clicked.connect(self.restore_selected)
        # Permanent deletion is restricted to admins via UI access control.
        # Connect the delete button to the permanent delete handler.
        try:
            self.ui.deleteBtn.clicked.connect(self.delete_selected)
        except Exception:
            pass
        # Show deletion reason when an asset row is clicked
        try:
            self.ui.assetsTable.cellClicked.connect(self._on_asset_row_clicked)
        except Exception:
            pass
        # Also allow right-click context menu on asset rows to view audit entry
        try:
            from PySide6.QtCore import Qt as _Qt
            self.ui.assetsTable.setContextMenuPolicy(_Qt.CustomContextMenu)
            self.ui.assetsTable.customContextMenuRequested.connect(self._on_asset_table_context)
        except Exception:
            pass
        self.user_service = UserService()
        self.asset_service = AssetService()
        # If dialog was created from MainWindow, propagate current user context
        # Attempt to discover current user id/name by walking the parent chain
        try:
            def _discover_user_from_ancestors(w):
                """Walk widget/dialog ancestors to find a session or methods exposing current user."""
                cur = w
                tried = set()
                while cur is not None and id(cur) not in tried:
                    tried.add(id(cur))
                    # Direct methods on MainWindow
                    if hasattr(cur, 'get_user_id') and hasattr(cur, 'get_username'):
                        try:
                            uid = cur.get_user_id()
                            uname = cur.get_username()
                            if uid is not None:
                                return uid, uname
                        except Exception:
                            pass
                    # Common pattern: admin screen stores parent_window pointing to main window
                    try:
                        pw = getattr(cur, 'parent_window', None)
                        if pw and hasattr(pw, 'get_user_id'):
                            try:
                                uid = pw.get_user_id()
                                uname = pw.get_username()
                                if uid is not None:
                                    return uid, uname
                            except Exception:
                                pass
                    except Exception:
                        pass

                    # session_service may be attached to parent objects
                    try:
                        ss = getattr(cur, 'session_service', None)
                        if ss and hasattr(ss, 'get_user_id'):
                            try:
                                # session_service.get_user_id may be instance method
                                uid = ss.get_user_id() if callable(ss.get_user_id) else None
                                uname = ss.get_username() if hasattr(ss, 'get_username') and callable(ss.get_username) else None
                                if uid is not None:
                                    return uid, uname
                            except Exception:
                                pass
                    except Exception:
                        pass

                    # climb to parent widget
                    try:
                        cur = cur.parent()
                    except Exception:
                        break
                return None, None

            if parent is not None:
                uid, uname = _discover_user_from_ancestors(parent)
                if uid is not None:
                    try:
                        self.asset_service.set_current_user(uid or 0, uname or 'System')
                    except Exception:
                        pass
                    try:
                        self.user_service.set_current_user(uid or 0, uname or 'System')
                    except Exception:
                        pass
                    try:
                        set_global_audit_user(uid or 0, uname or 'System')
                    except Exception:
                        pass
        except Exception:
            pass
        self.load_data()

    def load_data(self):
        # Load deactivated users
        try:
            with get_db() as session:
                users = session.query(User).filter(User.deleted_at != None).order_by(User.deleted_at.desc()).all()
                self.ui.usersTable.setRowCount(0)
                for u in users:
                    r = self.ui.usersTable.rowCount()
                    self.ui.usersTable.insertRow(r)
                    item0 = QTableWidgetItem(u.email or "")
                    item0.setData(Qt.UserRole, getattr(u, 'id', None))
                    self.ui.usersTable.setItem(r, 0, item0)
                    item1 = QTableWidgetItem(u.name or "")
                    self.ui.usersTable.setItem(r, 1, item1)
                    role_text = u.role.name.value if getattr(u, 'role', None) else 'Unknown'
                    item2 = QTableWidgetItem(role_text)
                    self.ui.usersTable.setItem(r, 2, item2)
                    deleted_text = u.deleted_at.strftime('%Y-%m-%d %H:%M:%S') if getattr(u, 'deleted_at', None) else ''
                    item3 = QTableWidgetItem(deleted_text)
                    self.ui.usersTable.setItem(r, 3, item3)

                # Load assets considered "deleted" (Retired or Disposed)
                assets = session.query(Asset).filter(Asset.status.in_([AssetStatus.RETIRED, AssetStatus.DISPOSED])).order_by(Asset.updated_at.desc()).all()
                self.ui.assetsTable.setRowCount(0)
                for a in assets:
                    r = self.ui.assetsTable.rowCount()
                    self.ui.assetsTable.insertRow(r)
                    item0 = QTableWidgetItem(a.asset_id or "")
                    # Store DB id in UserRole and deletion reason in a secondary role
                    item0.setData(Qt.UserRole, getattr(a, 'id', None))
                    # Fetch latest audit log entry for this asset deletion to show reason
                    try:
                        from ...core.models import AuditLog
                        log = session.query(AuditLog).filter(
                            AuditLog.table_name == 'assets',
                            AuditLog.record_id == str(getattr(a, 'id', None)),
                            AuditLog.action.in_(['ASSET_SOFT_DELETED', 'ASSET_PERMANENTLY_DELETED'])
                        ).order_by(AuditLog.timestamp.desc()).first()
                        reason_text = log.description if log and getattr(log, 'description', None) else ''
                    except Exception:
                        reason_text = ''
                    item0.setData(Qt.UserRole + 1, reason_text)
                    self.ui.assetsTable.setItem(r, 0, item0)
                    item1 = QTableWidgetItem(a.name or "")
                    self.ui.assetsTable.setItem(r, 1, item1)
                    item2 = QTableWidgetItem(a.status.value if a.status else "")
                    self.ui.assetsTable.setItem(r, 2, item2)
                    updated_text = a.updated_at.strftime('%Y-%m-%d %H:%M:%S') if getattr(a, 'updated_at', None) else ''
                    item3 = QTableWidgetItem(updated_text)
                    self.ui.assetsTable.setItem(r, 3, item3)
        except Exception as e:
            print(f"Error loading recently deleted data: {e}")

    def restore_selected(self):
        """Restore selected users or assets depending on active tab."""
        try:
            current = self.ui.tabWidget.currentIndex()
            # Determine the active table and restore all rows in that table
            if current == 0:
                # Users tab: restore all users shown
                table = self.ui.usersTable
                row_count = table.rowCount()
                if row_count == 0:
                    QMessageBox.information(self, 'Restore', 'No user to restore')
                    return
                restored = 0
                for r in range(row_count):
                    item = table.item(r, 0)
                    if not item:
                        continue
                    user_id = item.data(Qt.UserRole)
                    if user_id:
                        res = self.user_service.restore_user(user_id)
                        if res.get('success'):
                            restored += 1
                QMessageBox.information(self, 'Restore', f'Restored {restored} user(s)')
                self.load_data()
            elif current == 1:
                # Assets tab: restore all assets shown
                table = self.ui.assetsTable
                row_count = table.rowCount()
                if row_count == 0:
                    QMessageBox.information(self, 'Restore', 'No asset to restore')
                    return
                restored = 0
                for r in range(row_count):
                    item = table.item(r, 0)
                    if not item:
                        continue
                    asset_id = item.data(Qt.UserRole)
                    if asset_id:
                        res = self.asset_service.restore_asset(asset_id)
                        if res.get('success'):
                            restored += 1
                QMessageBox.information(self, 'Restore', f'Restored {restored} asset(s)')
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to restore: {e}')

    def delete_selected(self):
        """Permanently delete selected assets from the database.

        This action cannot be undone. Only available to users with
        appropriate admin permissions (UI should restrict access).
        """
        try:
            # Clear (permanently delete) all items in the active tab
            current = self.ui.tabWidget.currentIndex()
            if current == 0:
                # Users tab: permanently delete all users shown
                table = self.ui.usersTable
                row_count = table.rowCount()
                if row_count == 0:
                    QMessageBox.information(self, 'Clear', 'No user to delete')
                    return
                # confirm bulk permanent delete
                confirm = QMessageBox.question(self, 'Confirm Clear', f'Permanently delete {row_count} user(s)? This cannot be undone.',
                                                   QMessageBox.Yes | QMessageBox.No)
                if confirm != QMessageBox.Yes:
                    return
                deleted = 0
                for r in range(row_count):
                    item = table.item(r, 0)
                    if not item:
                        continue
                    user_id = item.data(Qt.UserRole)
                    if user_id:
                        res = self.user_service.permanently_delete_user(user_id)
                        if res.get('success'):
                            deleted += 1
                QMessageBox.information(self, 'Clear', f'Deleted {deleted} user(s) permanently')
                self.load_data()
            elif current == 1:
                # Assets tab: permanently delete all assets shown
                table = self.ui.assetsTable
                row_count = table.rowCount()
                if row_count == 0:
                    QMessageBox.information(self, 'Clear', 'No asset to delete')
                    return
                # confirm bulk permanent delete
                confirm = QMessageBox.question(self, 'Confirm Clear', f'Permanently delete {row_count} asset(s)? This cannot be undone.',
                                                   QMessageBox.Yes | QMessageBox.No)
                if confirm != QMessageBox.Yes:
                    return
                deleted = 0
                for r in range(row_count):
                    item = table.item(r, 0)
                    if not item:
                        continue
                    asset_id = item.data(Qt.UserRole)
                    if asset_id:
                        res = self.asset_service.delete_asset(asset_id, reason='Permanent clear by admin', permanent=True)
                        if res.get('success'):
                            deleted += 1
                QMessageBox.information(self, 'Clear', f'Deleted {deleted} asset(s) permanently')
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to delete: {e}')

    def _on_asset_row_clicked(self, row: int, column: int):
        """Show the full audit entry for the clicked asset row using a UI dialog."""
        try:
            item = self.ui.assetsTable.item(row, 0)
            if not item:
                return
            asset_id = item.data(Qt.UserRole)
            if not asset_id:
                return

            # Query latest audit log for this asset deletion and convert to primitives
            who = 'Unknown'
            when = ''
            action = 'Deletion'
            description = ''
            try:
                from ...core.models import AuditLog
                try:
                    with get_db() as session:
                        log = session.query(AuditLog).filter(
                            AuditLog.table_name == 'assets',
                            AuditLog.record_id == str(asset_id),
                            AuditLog.action.in_(['ASSET_SOFT_DELETED', 'ASSET_PERMANENTLY_DELETED'])
                        ).order_by(AuditLog.timestamp.desc()).first()
                        if log:
                            # Extract needed fields while session is open to avoid DetachedInstanceError later
                            who = getattr(log, 'username', None) or (getattr(log, 'user_id', None) and str(getattr(log, 'user_id')) ) or 'Unknown'
                            ts = getattr(log, 'timestamp', None)
                            if ts:
                                try:
                                    when = ts.strftime('%Y-%m-%d %H:%M:%S')
                                except Exception:
                                    when = str(ts)
                            action = getattr(log, 'action', None) or ''
                            description = getattr(log, 'description', None) or ''
                except Exception:
                    # DB read failed; leave fallbacks
                    pass
            except Exception:
                pass
            else:
                # Fallback to the reason we attached earlier (if any)
                reason = item.data(Qt.UserRole + 1)
                who = 'Unknown'
                when = ''
                action = 'Deletion'
                description = reason or 'No deletion reason recorded.'

            # Show UI-based dialog with full info
            try:
                from ..dialogs.audit_entry_dialog import AuditEntryDialog
                dlg = AuditEntryDialog(who=str(who), when=str(when), action=str(action), description=str(description), asset_id=asset_id, parent=self)
                dlg.exec()
            except Exception as e:
                # Fallback to message box if dialog fails
                QMessageBox.information(self, 'Deletion Reason', description)

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to show deletion reason: {e}')

    def _on_asset_table_context(self, point):
        """Handle right-click on assets table to open the audit entry dialog for that row."""
        try:
            row = self.ui.assetsTable.rowAt(point.y())
            if row is None or row < 0:
                return
            # reuse the row-click handler
            self._on_asset_row_clicked(row, 0)
        except Exception:
            pass
