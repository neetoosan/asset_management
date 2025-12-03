from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QColor
from ..ui.asset_table_view_ui import Ui_AssetTableView
from ...services.asset_service import AssetService
from ...services.expiry_calculator import ExpiryCalculator
from datetime import datetime, timedelta
from ..dialogs.asset_details import AssetDetailsDialog

class AssetTableView(QWidget):
    def __init__(self, category_name, category=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_AssetTableView()
        self.ui.setupUi(self)
        self.category = category  # Store category for refreshing
        
        # Set category name in header
        self.ui.categoryLabel.setText(category_name)
        
        # Setup the table
        self.setup_table()
        
        # Store asset data for editing/deleting
        self.asset_data = []
        
        # Connect signals
        self.ui.searchInput.textChanged.connect(self.filter_assets)
        # Install event filter on the table to capture Ctrl+E / Ctrl+D when table has focus
        self.ui.assetTable.installEventFilter(self)
        # Open details on single left click
        try:
            self.ui.assetTable.cellClicked.connect(self._on_cell_clicked)
        except Exception:
            pass
        
    def setup_table(self):
        # Setup summary frames styling
        frames = [
            self.ui.categoryAssetsFrame,
            self.ui.totalAssetsFrame,
            self.ui.categoryValueFrame,
            self.ui.depreciatableAssetsFrame,
            self.ui.depreciatedAssetsFrame,
            self.ui.highestValueFrame
        ]
        
        for frame in frames:
            frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                }
                QLabel {
                    font-size: 13px;
                    padding: 4px;
                    border: none;
                }
            """)
            
        # Set styles for value labels
        value_widgets = [
            self.ui.categoryAssetsValue,
            self.ui.totalAssetsValue,
            self.ui.categoryValueAmount,
            self.ui.depreciatableAssetsValue,
            self.ui.depreciatedAssetsValue,
            self.ui.highestValueAmount
        ]
        
        for widget in value_widgets:
            widget.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #0066cc;
            """)
        
        # Set column widths for the 10 columns defined in UI
        self.ui.assetTable.setColumnWidth(0, 100)  # Asset ID
        self.ui.assetTable.setColumnWidth(1, 180)  # Name
        self.ui.assetTable.setColumnWidth(2, 120)  # Model Number
        self.ui.assetTable.setColumnWidth(3, 120)  # Serial Number
        self.ui.assetTable.setColumnWidth(4, 140)  # Department
        self.ui.assetTable.setColumnWidth(5, 140)  # Category
        self.ui.assetTable.setColumnWidth(6, 110)  # Date Registered
        self.ui.assetTable.setColumnWidth(7, 110)  # Expiry Date
        self.ui.assetTable.setColumnWidth(8, 100)  # Value
        self.ui.assetTable.setColumnWidth(9, 90)   # Status
        
    def update_summary(self, assets):
        """Update the summary section with current asset statistics"""
        # Calculate category assets count
        category_count = len(assets)
        self.ui.categoryAssetsValue.setText(str(category_count))
        
        # Calculate total value for this category
        category_value = sum(asset.get('value', 0) for asset in assets)
        self.ui.categoryValueAmount.setText(f"₦{category_value:,.2f}")
        
        # Find highest value asset
        if assets:
            # support dicts or ORM objects
            def _get_value(a):
                if isinstance(a, dict):
                    return float(a.get('value', 0) or 0)
                return float(getattr(a, 'total_cost', 0) or 0)

            def _get_name(a):
                return a.get('name') if isinstance(a, dict) else getattr(a, 'name', 'N/A')

            highest_value_asset = max(assets, key=_get_value)
            self.ui.highestValueAmount.setText(f"₦{_get_value(highest_value_asset):,.2f}")
            self.ui.highestValueName.setText(_get_name(highest_value_asset) or 'N/A')
        
        # Calculate depreciatable (within 30 days) and deprecated (fully depreciated) assets
        today = datetime.now()
        depreciation_window = timedelta(days=30)  # Assets reaching end of life within 30 days
        
        depreciatable_count = 0
        depreciated_count = 0
        
        for asset in assets:
            try:
                # Use expiry_date from the new column
                exp_str = asset.get('expiry_date') if isinstance(asset, dict) else getattr(asset, 'expiry_date', None)
                if not exp_str:
                    # Fallback to exp_date for compatibility
                    exp_str = asset.get('exp_date') if isinstance(asset, dict) else getattr(asset, 'exp_date', None)
                if not exp_str:
                    continue
                if isinstance(exp_str, str):
                    exp_date = datetime.strptime(exp_str, '%Y-%m-%d')
                else:
                    exp_date = exp_str if isinstance(exp_str, datetime) else None
                if exp_date and exp_date < today:
                    depreciated_count += 1
                elif exp_date and today <= exp_date <= (today + depreciation_window):
                    depreciatable_count += 1
            except (ValueError, TypeError):
                continue
                
        self.ui.depreciatableAssetsValue.setText(str(depreciatable_count))
        self.ui.depreciatedAssetsValue.setText(str(depreciated_count))
        
        # Get total assets count from database
        try:
            asset_service = AssetService()
            summary = asset_service.get_asset_summary()
            total_assets = summary.get('total', 0)
            self.ui.totalAssetsValue.setText(str(total_assets))
        except Exception:
            self.ui.totalAssetsValue.setText("N/A")

    def load_assets(self, assets):
        """Load assets into the table"""
        # Store asset data for actions
        self.asset_data = assets
        
        # Update summary first
        self.update_summary(assets)
        
        # Then populate the table
        self.ui.assetTable.setRowCount(len(assets))
        
        for row, asset in enumerate(assets):
            # support dict or ORM object
            if isinstance(asset, dict):
                aid = asset.get('asset_id', '')
                name = asset.get('name', '')
                model = asset.get('model_number', '')
                serial = asset.get('serial_number', '')
                dept = asset.get('department', '')
                cat = asset.get('category') or asset.get('category_name') or ''
                date_reg = asset.get('date_registered', '')
                # Use expiry_date from new database column
                expiry = asset.get('expiry_date', '')
            else:
                aid = getattr(asset, 'asset_id', '')
                name = getattr(asset, 'name', '')
                model = getattr(asset, 'model_number', '') if hasattr(asset, 'model_number') else ''
                serial = getattr(asset, 'serial_number', '') if hasattr(asset, 'serial_number') else ''
                dept = getattr(asset, 'department', '')
                cat = asset.category.name if getattr(asset, 'category', None) else ''
                date_reg = getattr(asset, 'acquisition_date', '')
                date_reg = date_reg.strftime('%Y-%m-%d') if date_reg else ''
                # Use expiry_date from new database column
                expiry = getattr(asset, 'expiry_date', None)
                if expiry:
                    expiry = expiry.strftime('%Y-%m-%d') if hasattr(expiry, 'strftime') else str(expiry)
                else:
                    expiry = ''

            # Create item for Asset ID and store the internal DB id in UserRole so shortcuts can reference it
            asset_id_internal = asset.get('id', 0) if isinstance(asset, dict) else getattr(asset, 'id', 0)
            item0 = QTableWidgetItem(aid)
            item0.setData(Qt.UserRole, asset_id_internal)
            self.ui.assetTable.setItem(row, 0, item0)
            self.ui.assetTable.setItem(row, 1, QTableWidgetItem(name))
            # model and serial
            self.ui.assetTable.setItem(row, 2, QTableWidgetItem(model))
            self.ui.assetTable.setItem(row, 3, QTableWidgetItem(serial))
            self.ui.assetTable.setItem(row, 4, QTableWidgetItem(dept))
            self.ui.assetTable.setItem(row, 5, QTableWidgetItem(cat))
            self.ui.assetTable.setItem(row, 6, QTableWidgetItem(date_reg))
            
            # Column 7: Display end of useful life date calculated using Dec 31 logic
            acq_date_str = asset.get('acquisition_date') if isinstance(asset, dict) else (getattr(asset, 'acquisition_date', None))
            useful_life_val = asset.get('useful_life') if isinstance(asset, dict) else getattr(asset, 'useful_life', None)
            
            expiry_display = ''
            if acq_date_str and useful_life_val:
                try:
                    # Parse acquisition_date
                    from datetime import date as date_obj
                    if isinstance(acq_date_str, str):
                        acq_date_obj = date_obj.fromisoformat(acq_date_str.split('T')[0]) if 'T' in acq_date_str else date_obj.fromisoformat(acq_date_str)
                    else:
                        acq_date_obj = acq_date_str if isinstance(acq_date_str, date_obj) else None
                    
                    if acq_date_obj:
                        # Calculate expiry using Dec 31 logic
                        expiry_calculated = ExpiryCalculator.calculate_expiry_date(acq_date_obj, useful_life_val)
                        expiry_display = expiry_calculated.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"Error calculating expiry: {e}")
                    expiry_display = str(expiry) if expiry else ''
            else:
                expiry_display = str(expiry) if expiry else ''
            
            expiry_item = QTableWidgetItem(expiry_display)
            if expiry_display:
                try:
                    exp_dt = datetime.strptime(str(expiry_display), '%Y-%m-%d')
                    today = datetime.now()
                    if exp_dt < today:
                        expiry_item.setForeground(QColor('#F44336'))  # Red - expired
                    elif exp_dt < today + timedelta(days=30):
                        expiry_item.setForeground(QColor('#FFC107'))  # Yellow - expiring soon
                    else:
                        expiry_item.setForeground(QColor('#4CAF50'))  # Green - valid
                except:
                    pass
            self.ui.assetTable.setItem(row, 7, expiry_item)
            
            # Column 8: Format value with currency symbol and thousands separator
            val_num = (float(asset.get('value', 0)) if isinstance(asset, dict) else float(getattr(asset, 'total_cost', 0) or 0))
            value = f"₦{val_num:,.2f}"
            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.ui.assetTable.setItem(row, 8, value_item)
            
            # Column 9: Set status with appropriate styling
            status_text = asset.get('status') if isinstance(asset, dict) else (getattr(asset, 'status').value if getattr(asset, 'status', None) else '')
            status_item = QTableWidgetItem(status_text)
            status_colors = {
                'Available': QColor('#4CAF50'),
                'In Use': QColor('#2196F3'),
                'Under Maintenance': QColor('#FFC107'),
                'Disposed': QColor('#F44336')
            }
            status_item.setForeground(status_colors.get(asset.get('status', ''), QColor('#757575')))
            self.ui.assetTable.setItem(row, 9, status_item)
    
    # action buttons removed; keyboard shortcuts will control edit/delete of selected row
    
    def edit_asset(self, asset_id: int):
        """Handle edit asset action"""
        try:
            # Get parent main window and call its edit method
            main_window = self.parent()
            while main_window and not hasattr(main_window, 'show_edit_asset_dialog'):
                main_window = main_window.parent()
            
            if main_window:
                main_window.show_edit_asset_dialog(asset_id)
            else:
                QMessageBox.warning(self, "Error", "Unable to access main window for editing")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit asset: {str(e)}")
    
    def delete_asset(self, asset_id: int, asset_name: str, permanent: bool = False):
        """Handle delete asset action"""
        try:
            # Get parent main window and call its delete method
            main_window = self.parent()
            while main_window and not hasattr(main_window, 'delete_asset'):
                main_window = main_window.parent()
            
            if main_window:
                # Always request a soft-delete from the asset table view UI.
                # Permanence is reserved for the Recently Deleted view.
                main_window.delete_asset(asset_id, asset_name, permanent=permanent)
            else:
                QMessageBox.warning(self, "Error", "Unable to access main window for deletion")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete asset: {str(e)}")
            
    def filter_assets(self, text):
        """Filter table rows based on search text"""
        for row in range(self.ui.assetTable.rowCount()):
            show_row = False
            for col in range(self.ui.assetTable.columnCount()):
                item = self.ui.assetTable.item(row, col)
                if item and text.lower() in item.text().lower():
                    show_row = True
                    break
            self.ui.assetTable.setRowHidden(row, not show_row)

    def _shortcut_get_selected(self):
        """Return (row, internal_id, name) for the first selected row or (None, None, None)."""
        selected = self.ui.assetTable.selectionModel().selectedRows()
        if not selected:
            return None, None, None
        row = selected[0].row()
        # internal id stored in column 0 user role
        item0 = self.ui.assetTable.item(row, 0)
        internal_id = item0.data(Qt.UserRole) if item0 is not None else None
        # name in column 1
        name_item = self.ui.assetTable.item(row, 1)
        name = name_item.text() if name_item is not None else ''
        return row, internal_id, name

    def _on_cell_clicked(self, row: int, column: int):
        """Open Asset Details dialog when a row is clicked (left click)."""
        try:
            item0 = self.ui.assetTable.item(row, 0)
            if item0 is None:
                return
            internal_id = item0.data(Qt.UserRole)
            if internal_id is None:
                return
            # Open the dialog
            dlg = AssetDetailsDialog(internal_id, parent=self)
            dlg.exec()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open asset details: {e}")

    def _shortcut_edit_selected(self):
        row, internal_id, _name = self._shortcut_get_selected()
        if internal_id is None:
            QMessageBox.information(self, "No selection", "Please select an asset row to edit.")
            return
        self.edit_asset(internal_id)

    def _shortcut_delete_selected(self):
        row, internal_id, name = self._shortcut_get_selected()
        if internal_id is None:
            QMessageBox.information(self, "No selection", "Please select an asset row to delete.")
            return
        # Ask user for confirmation then call delete_asset
        reply = QMessageBox.question(self, "Confirm Delete", f"Delete asset '{name}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Prefer calling the main window's delete_asset so the centralized
            # deletion flow (including the required reason prompt) is always used.
            main_window = self.parent()
            while main_window and not hasattr(main_window, 'delete_asset'):
                main_window = main_window.parent()

            if main_window:
                try:
                    # Explicitly request soft-delete (permanent=False)
                    main_window.delete_asset(internal_id, name, permanent=False)
                except Exception:
                    # Fall back to local handler if something goes wrong
                    self.delete_asset(internal_id, name, permanent=False)
            else:
                # No main window found, call local handler which will attempt
                # to find the main window itself.
                self.delete_asset(internal_id, name, permanent=False)

    def eventFilter(self, watched, event):
        """Capture Ctrl+E and Ctrl+D when the asset table has focus."""
        # Only handle key presses on the asset table
        if watched is self.ui.assetTable and event.type() == QEvent.KeyPress:
            key_event = event
            ctrl = key_event.modifiers() & Qt.ControlModifier
            # Qt.Key_E / Qt.Key_D
            if ctrl and key_event.key() == Qt.Key_E:
                self._shortcut_edit_selected()
                return True
            if ctrl and key_event.key() == Qt.Key_D:
                self._shortcut_delete_selected()
                return True
        return super().eventFilter(watched, event)
