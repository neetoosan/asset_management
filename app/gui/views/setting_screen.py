import os
import sys
import platform
import json
from pathlib import Path
from datetime import datetime
import traceback
import pandas as pd
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem, QApplication
from PySide6.QtCore import Qt, QSettings, QTimer, QCoreApplication, QLocale, QTranslator
from ..ui.setting_screen_ui import Ui_SettingScreen
from ...utils.theme_manager import ThemeManager, Theme
from ...core.database import get_db


class SettingScreen(QWidget):
    """Settings screen widget for the asset management system"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingScreen()
        self.ui.setupUi(self)
        
        # Initialize QSettings for data persistence
        self.settings = QSettings("AssetManagement", "Settings")

        # Initialize settings data structure
        self.default_settings = {
            # General settings
            'auto_start': False,
            'minimize_to_tray': False,
            'confirm_exit': True,
            'language': 'English',
            'date_format': 'DD/MM/YYYY',
            'currency': 'USD ($)',
            
            # Appearance settings
            'theme': 'Default',
            'font_size': 10,
            'show_tooltips': True,
            'show_icons': True,
            
        # Notification settings
            'enable_alerts': True,
            'maintenance_alerts': True,
            'depreciation_alerts': True,
            'alert_days_before': 30,
            'enable_email': False,
            'email_address': '',
            
            # Import settings
            'last_import_directory': str(Path.home() / "Documents"),
            'last_successful_import': None,

        }

        # Initialize theme manager
        self.theme_manager = ThemeManager()

        # Setup theme options
        self.setup_theme_options()

        # Setup connections and initialize
        self.setup_connections()
        self.load_settings()
        
    def setup_connections(self):
        """Setup signal connections for all UI elements"""
        
        # General tab connections
        self.ui.autoStartCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.minimizeToTrayCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.confirmExitCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.languageComboBox.currentTextChanged.connect(self.on_setting_changed)
        # Apply language immediately when changed
        self.ui.languageComboBox.currentTextChanged.connect(self.apply_language_settings)
        self.ui.dateFormatComboBox.currentTextChanged.connect(self.on_setting_changed)
        self.ui.currencyComboBox.currentTextChanged.connect(self.on_setting_changed)
        
        # Appearance tab connections
        self.ui.themeComboBox.currentTextChanged.connect(self.on_setting_changed)
        # Apply theme immediately when changed
        self.ui.themeComboBox.currentTextChanged.connect(self.apply_theme_settings)
        self.ui.fontSizeSpinBox.valueChanged.connect(self.on_setting_changed)
        self.ui.showToolTipsCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.showIconsCheckBox.toggled.connect(self.on_setting_changed)
        
        # Notifications tab connections
        self.ui.enableAlertsCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.maintenanceAlertsCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.deprecationAlertsCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.alertDaysSpinBox.valueChanged.connect(self.on_setting_changed)
        self.ui.enableEmailCheckBox.toggled.connect(self.on_setting_changed)
        self.ui.emailAddressLineEdit.textChanged.connect(self.on_setting_changed)
        
        # Import tab connections
        self.ui.browseImportBtn.clicked.connect(self.browse_import_file)
        self.ui.importDataBtn.clicked.connect(self.import_data)
        
        # Bottom button connections
        self.ui.saveBtn.clicked.connect(self.save_settings)
        self.ui.resetBtn.clicked.connect(self.reset_to_defaults)
        
        # Enable/disable email field based on checkbox
        self.ui.enableEmailCheckBox.toggled.connect(
            lambda checked: self.ui.emailAddressLineEdit.setEnabled(checked)
        )
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        # This can be used to mark settings as modified
        # For now, we'll just auto-save settings when changed
        pass
    
    def load_settings(self):
        """Load settings from persistent storage and populate UI"""
        
        # General settings
        self.ui.autoStartCheckBox.setChecked(
            self.settings.value('auto_start', self.default_settings['auto_start'], bool)
        )
        self.ui.minimizeToTrayCheckBox.setChecked(
            self.settings.value('minimize_to_tray', self.default_settings['minimize_to_tray'], bool)
        )
        self.ui.confirmExitCheckBox.setChecked(
            self.settings.value('confirm_exit', self.default_settings['confirm_exit'], bool)
        )
        
        language = self.settings.value('language', self.default_settings['language'])
        index = self.ui.languageComboBox.findText(language)
        if index >= 0:
            self.ui.languageComboBox.setCurrentIndex(index)
            
        date_format = self.settings.value('date_format', self.default_settings['date_format'])
        index = self.ui.dateFormatComboBox.findText(date_format)
        if index >= 0:
            self.ui.dateFormatComboBox.setCurrentIndex(index)
            
        currency = self.settings.value('currency', self.default_settings['currency'])
        index = self.ui.currencyComboBox.findText(currency)
        if index >= 0:
            self.ui.currencyComboBox.setCurrentIndex(index)
        
        # Appearance settings
        theme = self.settings.value('theme', self.default_settings['theme'])
        index = self.ui.themeComboBox.findText(theme)
        if index >= 0:
            self.ui.themeComboBox.setCurrentIndex(index)
            
        self.ui.fontSizeSpinBox.setValue(
            self.settings.value('font_size', self.default_settings['font_size'], int)
        )
        self.ui.showToolTipsCheckBox.setChecked(
            self.settings.value('show_tooltips', self.default_settings['show_tooltips'], bool)
        )
        self.ui.showIconsCheckBox.setChecked(
            self.settings.value('show_icons', self.default_settings['show_icons'], bool)
        )
        
        # Notification settings
        self.ui.enableAlertsCheckBox.setChecked(
            self.settings.value('enable_alerts', self.default_settings['enable_alerts'], bool)
        )
        self.ui.maintenanceAlertsCheckBox.setChecked(
            self.settings.value('maintenance_alerts', self.default_settings['maintenance_alerts'], bool)
        )
        self.ui.deprecationAlertsCheckBox.setChecked(
            self.settings.value('depreciation_alerts', self.default_settings['depreciation_alerts'], bool)
        )
        self.ui.alertDaysSpinBox.setValue(
            self.settings.value('alert_days_before', self.default_settings['alert_days_before'], int)
        )
        self.ui.enableEmailCheckBox.setChecked(
            self.settings.value('enable_email', self.default_settings['enable_email'], bool)
        )
        self.ui.emailAddressLineEdit.setText(
            self.settings.value('email_address', self.default_settings['email_address'])
        )
        
        # Update email field state based on checkbox
        self.ui.emailAddressLineEdit.setEnabled(self.ui.enableEmailCheckBox.isChecked())
        # Apply persisted language selection now
        try:
            self.apply_language_settings()
        except Exception:
            pass
    
    def save_settings(self):
        """Save current settings to persistent storage and apply theme"""
        try:
            # Apply and persist theme and language immediately (best-effort)
            try:
                self.apply_theme_settings()
            except Exception:
                pass
            try:
                self.apply_language_settings()
            except Exception:
                pass

            # General settings
            self.settings.setValue('auto_start', self.ui.autoStartCheckBox.isChecked())
            self.settings.setValue('minimize_to_tray', self.ui.minimizeToTrayCheckBox.isChecked())
            self.settings.setValue('confirm_exit', self.ui.confirmExitCheckBox.isChecked())
            self.settings.setValue('language', self.ui.languageComboBox.currentText())
            self.settings.setValue('date_format', self.ui.dateFormatComboBox.currentText())
            self.settings.setValue('currency', self.ui.currencyComboBox.currentText())

            # Appearance settings
            self.settings.setValue('theme', self.ui.themeComboBox.currentText())
            self.settings.setValue('font_size', self.ui.fontSizeSpinBox.value())
            self.settings.setValue('show_tooltips', self.ui.showToolTipsCheckBox.isChecked())
            self.settings.setValue('show_icons', self.ui.showIconsCheckBox.isChecked())

            # Notification settings
            self.settings.setValue('enable_alerts', self.ui.enableAlertsCheckBox.isChecked())
            self.settings.setValue('maintenance_alerts', self.ui.maintenanceAlertsCheckBox.isChecked())
            self.settings.setValue('depreciation_alerts', self.ui.deprecationAlertsCheckBox.isChecked())
            self.settings.setValue('alert_days_before', self.ui.alertDaysSpinBox.value())
            self.settings.setValue('enable_email', self.ui.enableEmailCheckBox.isChecked())
            self.settings.setValue('email_address', self.ui.emailAddressLineEdit.text())

            # Force sync to ensure settings are saved
            self.settings.sync()

            # Persist selected settings to DB using SettingsService
            try:
                from ...services.settings_service import SettingsService

                ss = SettingsService()
                # Determine current user id (best-effort)
                current_user_id = 0
                try:
                    parent = getattr(self, 'parent', None) or self.parent()
                    if parent and hasattr(parent, 'get_user_id'):
                        current_user_id = parent.get_user_id() or 0
                except Exception:
                    current_user_id = 0

                db_errors = []
                # default currency -> SYSTEM_SETTINGS.default_currency
                try:
                    cur = self.ui.currencyComboBox.currentText()
                    res = ss.set_setting('SYSTEM_SETTINGS', 'default_currency', cur, updated_by_id=current_user_id)
                    if not res.get('success'):
                        db_errors.append(res.get('message') or 'Failed to save default_currency')
                except Exception as e:
                    db_errors.append(str(e))

                # alert days -> NOTIFICATIONS.alert_days_before
                try:
                    days = self.ui.alertDaysSpinBox.value()
                    res = ss.set_setting('NOTIFICATIONS', 'alert_days_before', str(days), updated_by_id=current_user_id)
                    if not res.get('success'):
                        db_errors.append(res.get('message') or 'Failed to save alert_days_before')
                except Exception as e:
                    db_errors.append(str(e))

                # enable email -> NOTIFICATIONS.enable_email
                try:
                    enabled = 'true' if self.ui.enableEmailCheckBox.isChecked() else 'false'
                    res = ss.set_setting('NOTIFICATIONS', 'enable_email', enabled, updated_by_id=current_user_id)
                    if not res.get('success'):
                        db_errors.append(res.get('message') or 'Failed to save enable_email')
                except Exception as e:
                    db_errors.append(str(e))

                # Attempt to refresh the asset table view so saved changes that affect
                # the assets list will be reflected immediately.
                try:
                    parent = getattr(self, 'parent', None) or self.parent()
                    if parent and hasattr(parent, 'refresh_current_asset_view'):
                        parent.refresh_current_asset_view()
                except Exception:
                    # non-fatal if parent doesn't exist or method absent
                    pass

                # If there were DB errors, surface a non-blocking warning to user
                if db_errors:
                    try:
                        # show a non-modal warning and also set a status label if present
                        msg = "Some settings were not saved to the database: " + "; ".join(db_errors)
                        warn = QMessageBox(self)
                        warn.setIcon(QMessageBox.Warning)
                        warn.setWindowTitle("Settings DB Warning")
                        warn.setText(msg)
                        warn.setStandardButtons(QMessageBox.Ok)
                        warn.setModal(False)
                        warn.show()
                    except Exception:
                        print('Settings DB warning:', db_errors)

            except Exception as e:
                # Non-fatal: report but continue
                print('Failed to persist settings to DB:', e)

            QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
    
    def reset_to_defaults(self):
        """Reset all settings to their default values"""
        reply = QMessageBox.question(
            self, 
            "Reset Settings", 
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Clear all stored settings
            self.settings.clear()
            
            # Reload with defaults
            self.load_settings()
            
            QMessageBox.information(self, "Settings Reset", "All settings have been reset to default values!")
    

            
            # The following backup location logic is not implemented and references an undefined variable.
            # If backup functionality is needed, implement it here.
            # For now, this block is removed to prevent errors.

    def get_setting(self, key, default_value=None):
        """Get a specific setting value"""
        if default_value is None and key in self.default_settings:
            default_value = self.default_settings[key]
        return self.settings.value(key, default_value)
    
    def set_setting(self, key, value):
        """Set a specific setting value"""
        self.settings.setValue(key, value)
        self.settings.sync()
    
    def get_all_settings(self):
        """Get all current settings as a dictionary"""
        settings_dict = {}
        for key in self.default_settings.keys():
            settings_dict[key] = self.get_setting(key)
        return settings_dict
    
    def apply_theme_settings(self):
        """Apply the selected theme immediately"""
        """Apply the selected theme immediately and persist the choice.

        Stores the selected theme as a string in QSettings and asks ThemeManager
        to apply it. If Theme construction fails, attempts to match by value or
        name fallback to default.
        """
        selected = self.ui.themeComboBox.currentText()
        try:
            # persist as a simple string
            self.settings.setValue('theme', selected)
        except Exception:
            pass

        # Resolve Theme enum robustly
        try:
            theme = Theme(selected)
        except Exception:
            theme = None
            for t in Theme:
                if getattr(t, 'value', None) == selected or t.name == selected:
                    theme = t
                    break
            if theme is None:
                # final fallback to configured default
                try:
                    theme = Theme(self.default_settings.get('theme', 'Default'))
                except Exception:
                    # as last resort, pick first Theme
                    theme = list(Theme)[0]

        try:
            self.theme_manager.apply_theme(theme)
        except Exception as e:
            print(f"Failed to apply theme '{selected}': {e}")
        
    def setup_theme_options(self):
        """Setup theme combobox with available options"""
        self.ui.themeComboBox.clear()
        self.ui.themeComboBox.addItems([theme.value for theme in Theme])
        # Set current theme (stored as a string)
        current_theme = self.settings.value('theme', self.default_settings.get('theme', 'Default'))
        index = self.ui.themeComboBox.findText(current_theme)
        if index >= 0:
            self.ui.themeComboBox.setCurrentIndex(index)

        # Apply the current theme now (best-effort)
        try:
            self.apply_theme_settings()
        except Exception:
            pass
    
    def apply_language_settings(self):
        """Attempt to apply the selected language immediately.

        This will persist the selection in QSettings, set the QLocale default,
        and attempt to load a .qm translation file from the `i18n` directory
        located at the project root (i18n/<code>.qm). If a translator is
        successfully loaded it will be installed into the QCoreApplication.
        """
        lang_display = self.ui.languageComboBox.currentText()
        try:
            self.settings.setValue('language', lang_display)
        except Exception:
            pass

        # Simple display-name -> locale code mapping; extend as needed
        lang_map = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de'
        }
        locale_code = lang_map.get(lang_display, (lang_display[:2] or 'en').lower())

        try:
            QLocale.setDefault(QLocale(locale_code))
        except Exception:
            pass

        # Attempt to load translation files from project i18n directory
        try:
            translations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'i18n'))
            qm_file = f"{locale_code}.qm"
            translator = QTranslator()
            loaded = False
            if os.path.isdir(translations_dir):
                loaded = translator.load(qm_file, translations_dir)

            if loaded:
                # remove previous translator if present
                try:
                    if hasattr(self, 'translator') and isinstance(self.translator, QTranslator):
                        QCoreApplication.removeTranslator(self.translator)
                except Exception:
                    pass
                QCoreApplication.installTranslator(translator)
                self.translator = translator
            else:
                # No .qm found: do nothing further. The language choice is still persisted.
                pass
        except Exception as e:
            print(f"Failed to apply language '{lang_display}': {e}")
        
    def browse_import_file(self):
        """Open file dialog to select import file"""
        file_filter = "Data Files (*.csv *.xlsx);;CSV Files (*.csv);;Excel Files (*.xlsx)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Import",
            str(Path.home() / "Documents"),
            file_filter
        )
        
        if file_path:
            self.ui.importFilePathInput.setText(file_path)
            self.ui.importStatusLabel.clear()

    def import_data(self):
        """Import data from selected file with enhanced Excel support"""
        file_path = self.ui.importFilePathInput.text()
        if not file_path:
            QMessageBox.warning(self, "Import Error", "Please select a file to import.")
            return

        try:
            # Read the file based on its extension
            file_extension = Path(file_path).suffix.lower()
            has_header = self.ui.headerRowCheckBox.isChecked()

            if file_extension == '.csv':
                df = pd.read_csv(file_path, header=0 if has_header else None)
            elif file_extension in ['.xlsx', '.xls']:
                # Read Excel with better handling
                # First, try to detect if we need to skip empty rows
                if file_extension == '.xlsx':
                    df_raw = pd.read_excel(file_path, header=None, nrows=5, engine='openpyxl')
                else:
                    df_raw = pd.read_excel(file_path, header=None, nrows=5)
                
                # Skip completely empty rows from the beginning
                skip_rows = 0
                for idx, row in df_raw.iterrows():
                    if row.isna().all():
                        skip_rows += 1
                    else:
                        break
                
                # Now read the actual data
                if file_extension == '.xlsx':
                    df = pd.read_excel(file_path, header=0 if has_header else None, skiprows=skip_rows, engine='openpyxl')
                else:
                    df = pd.read_excel(file_path, header=0 if has_header else None, skiprows=skip_rows)
            else:
                QMessageBox.warning(self, "Import Error", "Unsupported file format. Please use CSV or Excel files.")
                return

            # If no header was specified, use default column names
            if not has_header:
                df.columns = [f'Column_{i}' for i in range(len(df.columns))]

            # Clean column names: strip whitespace and normalize
            df.columns = [str(col).strip() for col in df.columns]

            # Basic sanitization: drop completely empty rows
            df = df.dropna(how='all')
            
            # Remove rows where all string columns are empty/whitespace
            string_cols = df.select_dtypes(include=['object']).columns
            if len(string_cols) > 0:
                df = df[~df[string_cols].apply(lambda x: x.str.strip() if isinstance(x.iloc[0], str) else x).isna().all(axis=1)]

            total = len(df)
            if total == 0:
                QMessageBox.information(self, "Import", "No valid rows found in the selected file.")
                return

            # Populate preview table
            cols = [str(c) for c in df.columns]
            self.ui.importPreviewTable.clear()
            self.ui.importPreviewTable.setColumnCount(len(cols))
            self.ui.importPreviewTable.setHorizontalHeaderLabels(cols)
            preview_rows = min(200, total)
            self.ui.importPreviewTable.setRowCount(preview_rows)
            
            for r in range(preview_rows):
                for c, col in enumerate(cols):
                    try:
                        val = df.iloc[r, c]
                    except Exception:
                        val = ''
                    item = QTableWidgetItem(str(val) if not pd.isna(val) else '')
                    self.ui.importPreviewTable.setItem(r, c, item)

            # Prepare AssetService
            from ...services.asset_service import AssetService
            from ...services.settings_service import SettingsService
            
            asset_service = AssetService()
            settings_service = SettingsService()
            
            # Check if asset creation is allowed
            can_create = settings_service.can_create_asset()
            if not can_create:
                print("WARNING: Asset creation is disabled in system settings. Import may fail.")
                print("To enable imports, go to Settings and enable 'Allow Asset Creation'")
            
            # Set current user for audit trail
            try:
                parent = getattr(self, 'parent', None) or self.parent()
                if parent and hasattr(parent, 'get_user_id'):
                    uid = parent.get_user_id()
                    uname = parent.get_username()
                    if uid is not None:
                        asset_service.set_current_user(uid or 0, uname or 'System')
            except Exception:
                pass

            # Enhanced column mapping with more variations
            def col_lookup(name_variants):
                """Find column by matching any of the name variants (case-insensitive)"""
                name_variants = [v.lower() for v in name_variants]
                for c in cols:
                    if c:
                        col_lower = c.lower().strip()
                        # Exact match
                        if col_lower in name_variants:
                            return c
                        # Partial match (contains any variant)
                        if any(v in col_lower for v in name_variants):
                            return c
                return None

            # Get or create default category for imports
            from ...services.asset_service import AssetService as AS
            default_category = None
            try:
                with get_db() as temp_session:
                    from ...core.models import AssetCategory
                    default_category = temp_session.query(AssetCategory).filter(
                        AssetCategory.name == 'Imported Assets'
                    ).first()
                    if not default_category:
                        default_category = AssetCategory(name='Imported Assets', description='Assets imported from Excel files')
                        temp_session.add(default_category)
                        temp_session.commit()
                        temp_session.refresh(default_category)
                    default_category_id = default_category.id
            except Exception as e:
                print(f"Warning: Could not create default category: {e}")
                default_category_id = None
            
            # Comprehensive mapping based on your spreadsheet structure
            mappings = {
                'asset_id': col_lookup(['asset id', 'asset_id', 'assetid', 'id', 'asset no', 'asset number']),
                'name': col_lookup(['description', 'asset description', 'name', 'asset name', 'item']),
                'description': col_lookup(['description', 'notes', 'remarks', 'comments']),
                'serial_number': col_lookup(['serial', 'serial number', 'serial_number', 'serial no', 's/n']),
                'model_number': col_lookup(['model', 'model number', 'model_number', 'model no']),
                'department': col_lookup(['department', 'dept', 'location/dept', 'location - department']),
                'location': col_lookup(['location', 'loc', 'site', 'office', 'department', 'dept']),
                'category': col_lookup(['category', 'asset category', 'type', 'class']),
                'sub_category': col_lookup(['sub category', 'sub_category', 'subcategory', 'sub-category']),
                'total_cost': col_lookup(['total cost', 'total_cost', 'value', 'cost', 'price', 'amount']),
                'acquisition_date': col_lookup(['acquisition', 'acquistion', 'acquisition date', 'date registered', 'acquisition_date', 'purchase date', 'date']),
                'supplier': col_lookup(['supplier', 'vendor', 'supplier/vendor']),
                'status': col_lookup(['status', 'asset status', 'condition']),
                'quantity': col_lookup(['quantity', 'qty', 'units']),
                'unit_cost': col_lookup(['unit cost', 'unit_cost', 'unit price', 'price per unit']),
                'custodian': col_lookup(['custodian', 'user', 'assigned to', 'custodian/user']),
                'useful_life': col_lookup(['useful life', 'usefull life', 'useful_life', 'years', 'lifespan', 'useful life (years)']),
                'depreciation_method': col_lookup(['depreciation method', 'depreciation_method', 'method', 'depreciation']),
                'depreciation_percentage': col_lookup(['depreciation %', 'depreciation_percentage', 'dep %', 'depreciation percentage']),
                'depreciation_value': col_lookup(['depreciation', 'depreciation value', 'depreciation_value']),
                'scrap_value': col_lookup(['scrap value', 'scrap_value', 'salvage value']),
                'net_book_value': col_lookup(['net book value', 'netbook value', 'nbv', 'book value'])
            }

            success = 0
            failed = 0
            self.ui.importProgressBar.setValue(0)
            failed_rows = []
            
            # Process each row
            for idx in range(total):
                row = df.iloc[idx]
                asset_data = {}
                
                try:
                    # Extract data from row based on mappings
                    for field, col in mappings.items():
                        if not col or col not in df.columns:
                            continue
                        
                        val = row[col]
                        
                        # Skip empty/null values
                        if pd.isna(val):
                            continue
                        
                        # Convert to string and strip whitespace
                        val_str = str(val).strip()
                        if not val_str or val_str.lower() in ['nan', 'none', 'null', '']:
                            continue
                        
                        # Handle specific field types
                        if field in ['total_cost', 'unit_cost', 'depreciation_value', 'scrap_value', 'net_book_value']:
                            try:
                                # Remove currency symbols and commas
                                clean_val = val_str.replace(',', '').replace('$', '').replace('₦', '').replace('NGN', '').strip()
                                asset_data[field] = float(clean_val)
                            except (ValueError, AttributeError):
                                # If conversion fails, skip this field
                                pass
                        
                        elif field == 'quantity':
                            try:
                                asset_data[field] = int(float(val_str.replace(',', '')))
                            except (ValueError, AttributeError):
                                pass
                        
                        elif field == 'useful_life':
                            try:
                                asset_data[field] = int(float(val_str))
                            except (ValueError, AttributeError):
                                pass
                        
                        elif field == 'depreciation_percentage':
                            try:
                                # Remove % symbol if present
                                clean_val = val_str.replace('%', '').strip()
                                asset_data[field] = float(clean_val)
                            except (ValueError, AttributeError):
                                pass
                        
                        elif field == 'acquisition_date':
                            try:
                                if isinstance(val, (pd.Timestamp, datetime)):
                                    asset_data[field] = val
                                else:
                                    # Try to parse string dates
                                    asset_data[field] = pd.to_datetime(val_str, errors='coerce')
                            except Exception:
                                pass
                        
                        else:
                            # For text fields (depreciation_method, etc), just store as string
                            asset_data[field] = val_str

                    # Validate minimum required fields
                    if 'name' not in asset_data and 'asset_id' not in asset_data:
                        raise ValueError('Missing required fields: asset must have either a name or asset ID')
                    
                    # Log depreciation-related fields for debugging
                    if any(k in asset_data for k in ['useful_life', 'depreciation_percentage', 'depreciation_method']):
                        dep_info = {k: asset_data.get(k) for k in ['useful_life', 'depreciation_percentage', 'depreciation_method'] if k in asset_data}
                        print(f"Asset {asset_data.get('asset_id', 'N/A')}: Depreciation fields - {dep_info}")

                    # If only asset_id exists, use it as name
                    if 'asset_id' in asset_data and 'name' not in asset_data:
                        asset_data['name'] = asset_data['asset_id']

                    # IMPORTANT: Provide default description if none exists (NOT NULL constraint)
                    if 'description' not in asset_data or not asset_data.get('description'):
                        # Use a meaningful default: combine asset name and location if available
                        parts = []
                        if 'name' in asset_data:
                            parts.append(asset_data['name'])
                        if 'location' in asset_data and asset_data['location']:
                            parts.append(f"Located in {asset_data['location']}")
                        asset_data['description'] = ' - '.join(parts) if parts else 'Asset imported from Excel'
                    
                    # IMPORTANT: Provide category_id (NOT NULL foreign key constraint)
                    if 'category_id' not in asset_data or not asset_data.get('category_id'):
                        if default_category_id:
                            asset_data['category_id'] = default_category_id
                        else:
                            raise ValueError('No category available for import')
                    
                    # IMPORTANT: Provide location (NOT NULL constraint)
                    if 'location' not in asset_data or not asset_data.get('location'):
                        asset_data['location'] = asset_data.get('department', 'Unspecified Location')
                    
                    # IMPORTANT: Provide supplier (NOT NULL constraint)
                    if 'supplier' not in asset_data or not asset_data.get('supplier'):
                        asset_data['supplier'] = 'Not Specified'
                    
                    # IMPORTANT: Provide acquisition_date (NOT NULL constraint)
                    if 'acquisition_date' not in asset_data or not asset_data.get('acquisition_date'):
                        from datetime import datetime
                        asset_data['acquisition_date'] = datetime.now().date()
                    
                    # IMPORTANT: Provide unit_cost (NOT NULL constraint)
                    if 'unit_cost' not in asset_data or asset_data.get('unit_cost') is None:
                        total = asset_data.get('total_cost', 0)
                        qty = asset_data.get('quantity', 1)
                        asset_data['unit_cost'] = float(total) / float(qty) if qty else 0

                    # Create asset via service
                    result = asset_service.create_asset(asset_data)
                    
                    if result.get('success'):
                        success += 1
                    else:
                        failed += 1
                        error_msg = result.get('message', 'Unknown error')
                        print(f"Row {idx + 2} failed: {error_msg} | Asset: {asset_data.get('asset_id', 'N/A')}")
                        failed_rows.append({
                            'row_index': idx + 2,  # +2 because: 0-indexed + header row
                            'message': error_msg,
                            **{c: (str(row[c]) if c in row.index and not pd.isna(row[c]) else '') for c in cols}
                        })
                        
                except Exception as e:
                    failed += 1
                    failed_rows.append({
                        'row_index': idx + 2,
                        'message': str(e),
                        **{c: (str(row[c]) if c in row.index and not pd.isna(row[c]) else '') for c in cols}
                    })

                # Update progress UI
                percent = int((idx + 1) / total * 100)
                self.ui.importProgressBar.setValue(percent)
                self.ui.importSuccessLabel.setText(f"Success: {success}")
                self.ui.importFailedLabel.setText(f"Failed: {failed}")
                self.ui.importPercentLabel.setText(f"{percent}%")
                
                # Allow UI to update every 10 rows to improve performance
                if idx % 10 == 0:
                    QApplication.processEvents()

            # Import complete
            msg = f"Import complete — Successful: {success}, Failed: {failed}"
            if success > 0:
                msg += f"\nDepreciation fields processed where available"
            self.ui.importStatusLabel.setText(msg)
            self.ui.importStatusLabel.setStyleSheet(
                "color: green" if failed == 0 else "color: orange"
            )

            # Offer to export failed rows
            if failed_rows:
                try:
                    msg = f"{failed} rows failed to import. Would you like to export the failed rows for review?"
                    reply = QMessageBox.question(
                        self, 
                        "Export Failed Rows", 
                        msg, 
                        QMessageBox.Yes | QMessageBox.No, 
                        QMessageBox.Yes
                    )
                    
                    if reply == QMessageBox.Yes:
                        save_path, _ = QFileDialog.getSaveFileName(
                            self, 
                            "Save Failed Rows", 
                            str(Path.home() / "failed_imports.csv"), 
                            "CSV Files (*.csv)"
                        )
                        
                        if save_path:
                            fr_df = pd.DataFrame(failed_rows)
                            fr_df.to_csv(save_path, index=False)
                            QMessageBox.information(
                                self, 
                                "Export Saved", 
                                f"Failed rows exported to: {save_path}"
                            )
                except Exception as e:
                    print('Failed to export failed rows:', e)
                    QMessageBox.warning(
                        self, 
                        "Export Failed", 
                        f"Could not export failed rows: {e}"
                    )

            # Refresh the main asset table
            try:
                parent = getattr(self, 'parent', None) or self.parent()
                if parent and hasattr(parent, 'refresh_current_asset_view'):
                    parent.refresh_current_asset_view()
            except Exception:
                pass

            # Show success message
            if success > 0:
                QMessageBox.information(
                    self,
                    "Import Complete",
                    f"Successfully imported {success} assets!\n\n"
                    f"Success: {success}\n"
                    f"Failed: {failed}"
                )

        except Exception as e:
            error_detail = traceback.format_exc()
            print("Import Error Details:", error_detail)
            
            QMessageBox.critical(
                self, 
                "Import Error", 
                f"Failed to import data:\n\n{str(e)}\n\nCheck console for details."
            )
            self.ui.importStatusLabel.setText("Import failed!")
            self.ui.importStatusLabel.setStyleSheet("color: red")
