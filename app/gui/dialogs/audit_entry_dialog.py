from PySide6.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt
from ..ui.audit_entry_dialog_ui import Ui_AuditEntryDialog
from ...core.database import get_db, get_db_session
from ...core.models import AuditLog


class AuditEntryDialog(QDialog):
    def __init__(self, who: str, when: str, action: str, description: str, asset_id: int = None, parent=None):
        """Dialog to show a single audit entry.

        If asset_id is provided, the dialog exposes Restore and Delete actions
        that will call the parent dialog's services when available, or fall
        back to creating service instances.
        """
        super().__init__(parent)
        self.ui = Ui_AuditEntryDialog()
        self.ui.setupUi(self)

        self.asset_id = asset_id

        # Populate fields
        self.ui.whoValue.setText(who or '')
        self.ui.whenValue.setText(when or '')
        self.ui.actionValue.setText(action or '')
        self.ui.descriptionValue.setPlainText(description or '')

        # Connect buttons if present
        try:
            self.ui.restoreBtn.clicked.connect(self._on_restore)
        except Exception:
            pass
        try:
            self.ui.deleteBtn.clicked.connect(self._on_delete)
        except Exception:
            pass
        try:
            self.ui.closeBtn.clicked.connect(self.reject)
        except Exception:
            pass

        # Make dialog modal
        self.setWindowModality(Qt.ApplicationModal)

        # If an asset_id was provided, load audit entries and convert to plain dicts.
        # Using plain dicts prevents DetachedInstanceError without keeping the
        # DB session open for the dialog lifetime.
        self._audit_entries = []
        try:
            if self.asset_id is not None:
                try:
                    with get_db() as session:
                        logs = (session.query(AuditLog)
                                .filter(AuditLog.table_name == 'assets', AuditLog.record_id == str(self.asset_id))
                                .order_by(AuditLog.timestamp.desc())
                                .all())
                        for l in logs:
                            entry = {
                                'id': getattr(l, 'id', None),
                                'username': getattr(l, 'username', None),
                                'user_id': getattr(l, 'user_id', None),
                                'timestamp': getattr(l, 'timestamp', None),
                                'action': getattr(l, 'action', None),
                                'description': getattr(l, 'description', None),
                                # Include minimal user info if safe
                                'user': None
                            }
                            try:
                                u = getattr(l, 'user', None)
                                if u is not None:
                                    entry['user'] = {
                                        'id': getattr(u, 'id', None),
                                        'name': getattr(u, 'name', None),
                                        'email': getattr(u, 'email', None)
                                    }
                            except Exception:
                                entry['user'] = None

                            self._audit_entries.append(entry)
                            # Create list item label using timestamp and action
                            label = ''
                            try:
                                ts = entry.get('timestamp')
                                if ts is not None:
                                    label = ts.strftime('%Y-%m-%d %H:%M:%S') + ' - '
                            except Exception:
                                label = ''
                            label = label + (entry.get('action') or 'Audit')
                            it = QListWidgetItem(label)
                            it.setData(Qt.UserRole, len(self._audit_entries) - 1)
                            try:
                                self.ui.auditList.addItem(it)
                            except Exception:
                                pass
                except Exception:
                    # ignore DB load errors; fall back to provided data
                    pass
        except Exception:
            pass

        # Wire selection change on the audit list to update details
        try:
            if hasattr(self.ui, 'auditList'):
                self.ui.auditList.currentRowChanged.connect(self._on_audit_selected)
                # Select first entry if present
                if len(self._audit_entries) > 0:
                    try:
                        self.ui.auditList.setCurrentRow(0)
                    except Exception:
                        pass
        except Exception:
            pass

    def _get_asset_service(self):
        """Return an AssetService instance, preferring parent's service if available."""
        svc = None
        try:
            if self.parent() is not None and hasattr(self.parent(), 'asset_service'):
                svc = getattr(self.parent(), 'asset_service')
        except Exception:
            svc = None
        if svc is None:
            try:
                from ...services.asset_service import AssetService

                svc = AssetService()
                # Try to propagate current user context to the newly created service by
                # walking parent ancestors for a session or get_user_id/get_username methods.
                try:
                    cur = self.parent()
                    tried = set()
                    while cur is not None and id(cur) not in tried:
                        tried.add(id(cur))
                        if hasattr(cur, 'get_user_id') and hasattr(cur, 'get_username'):
                            try:
                                uid = cur.get_user_id()
                                uname = cur.get_username()
                                if uid is not None:
                                    svc.set_current_user(uid or 0, uname or 'System')
                                    break
                            except Exception:
                                pass
                        try:
                            pw = getattr(cur, 'parent_window', None)
                            if pw and hasattr(pw, 'get_user_id'):
                                try:
                                    uid = pw.get_user_id()
                                    uname = pw.get_username()
                                    if uid is not None:
                                        svc.set_current_user(uid or 0, uname or 'System')
                                        break
                                except Exception:
                                    pass
                        except Exception:
                            pass
                        try:
                            ss = getattr(cur, 'session_service', None)
                            if ss and hasattr(ss, 'get_user_id'):
                                try:
                                    uid = ss.get_user_id() if callable(ss.get_user_id) else None
                                    uname = ss.get_username() if hasattr(ss, 'get_username') and callable(ss.get_username) else None
                                    if uid is not None:
                                        svc.set_current_user(uid or 0, uname or 'System')
                                        break
                                except Exception:
                                    pass
                        except Exception:
                            pass
                        try:
                            cur = cur.parent()
                        except Exception:
                            break
                except Exception:
                    pass
            except Exception:
                svc = None
        return svc

    def _on_audit_selected(self, index: int):
        """Populate the detail fields from the selected audit entry index."""
        try:
            if index is None or index < 0:
                return
            if index >= len(self._audit_entries):
                return
            entry = self._audit_entries[index]
            who = entry.get('username') or (entry.get('user_id') and str(entry.get('user_id'))) or 'Unknown'
            when_val = ''
            try:
                ca = entry.get('timestamp')
                if ca is not None:
                    try:
                        when_val = ca.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception:
                        when_val = str(ca)
            except Exception:
                when_val = ''
            action = entry.get('action') or ''
            description = entry.get('description') or ''

            try:
                self.ui.whoValue.setText(str(who))
            except Exception:
                pass
            try:
                self.ui.whenValue.setText(str(when_val))
            except Exception:
                pass
            try:
                self.ui.actionValue.setText(str(action))
            except Exception:
                pass
            try:
                self.ui.descriptionValue.setPlainText(str(description))
            except Exception:
                pass
        except Exception:
            pass

    def closeEvent(self, event):
        """Ensure we close the audit DB session when dialog closes."""
        try:
            if getattr(self, '_audit_session', None) is not None:
                try:
                    self._audit_session.close()
                except Exception:
                    pass
                self._audit_session = None
        except Exception:
            pass
        try:
            super().closeEvent(event)
        except Exception:
            event.accept()


    def _on_restore(self):
        if not self.asset_id:
            QMessageBox.information(self, 'Restore', 'No asset selected to restore')
            return
        svc = self._get_asset_service()
        if svc is None:
            QMessageBox.critical(self, 'Restore', 'Asset service unavailable')
            return
        try:
            res = svc.restore_asset(self.asset_id)
        except Exception as e:
            QMessageBox.critical(self, 'Restore', f'Failed to restore asset: {e}')
            return
        if res.get('success'):
            QMessageBox.information(self, 'Restore', 'Asset restored')
            try:
                if self.parent() is not None and hasattr(self.parent(), 'load_data'):
                    self.parent().load_data()
            except Exception:
                pass
            self.accept()
        else:
            QMessageBox.warning(self, 'Restore', res.get('error') or 'Restore failed')

    def _on_delete(self):
        if not self.asset_id:
            QMessageBox.information(self, 'Delete', 'No asset selected to delete')
            return
        confirm = QMessageBox.question(self, 'Confirm Delete', 'Permanently delete this asset? This cannot be undone.',
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return
        svc = self._get_asset_service()
        if svc is None:
            QMessageBox.critical(self, 'Delete', 'Asset service unavailable')
            return
        try:
            reason = self.ui.descriptionValue.toPlainText() if hasattr(self.ui, 'descriptionValue') else 'Deleted from audit dialog'
            res = svc.delete_asset(self.asset_id, reason=reason, permanent=True)
        except Exception as e:
            QMessageBox.critical(self, 'Delete', f'Failed to delete asset: {e}')
            return
        if res.get('success'):
            QMessageBox.information(self, 'Delete', 'Asset permanently deleted')
            try:
                if self.parent() is not None and hasattr(self.parent(), 'load_data'):
                    self.parent().load_data()
            except Exception:
                pass
            self.accept()
        else:
            QMessageBox.warning(self, 'Delete', res.get('error') or 'Delete failed')
