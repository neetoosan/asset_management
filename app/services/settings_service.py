import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..core.database import get_db
from ..core.models import SystemConfiguration, User
from .audit_service import AuditService


class SettingsService:
    def __init__(self):
        self.audit_service = AuditService()
        self._initialize_default_settings()

    def _initialize_default_settings(self):
        """Initialize default system settings if they don't exist."""
        default_settings = [
            # CRUD Restrictions
            {
                'category': 'CRUD_RESTRICTIONS',
                'key': 'allow_asset_creation',
                'value': 'true',
                'data_type': 'boolean',
                'description': 'Allow users to create new assets',
                'default_value': 'true'
            },
            {
                'category': 'CRUD_RESTRICTIONS',
                'key': 'allow_asset_editing',
                'value': 'true',
                'data_type': 'boolean',
                'description': 'Allow users to edit existing assets',
                'default_value': 'true'
            },
            {
                'category': 'CRUD_RESTRICTIONS',
                'key': 'allow_asset_deletion',
                'value': 'true',
                'data_type': 'boolean',
                'description': 'Allow users to delete assets (except admins)',
                'default_value': 'true'
            },
            {
                'category': 'CRUD_RESTRICTIONS',
                'key': 'require_approval_for_high_value_assets',
                'value': 'false',
                'data_type': 'boolean',
                'description': 'Flag assets above threshold for review (non-blocking)',
                'default_value': 'false'
            },
            {
                'category': 'CRUD_RESTRICTIONS',
                'key': 'high_value_asset_threshold',
                'value': '10000.00',
                'data_type': 'float',
                'description': 'Threshold amount to flag high-value assets (non-blocking)',
                'default_value': '10000.00'
            },
            {
                'category': 'CRUD_RESTRICTIONS',
                'key': 'allow_bulk_operations',
                'value': 'false',
                'data_type': 'boolean',
                'description': 'Allow bulk create/update/delete operations',
                'default_value': 'false'
            },
            {
                'category': 'CRUD_RESTRICTIONS',
                'key': 'max_assets_per_user',
                'value': '100',
                'data_type': 'integer',
                'description': 'Maximum number of assets a user can be assigned',
                'default_value': '100'
            },
            
            # User Management Restrictions
            {
                'category': 'USER_MANAGEMENT',
                'key': 'allow_self_password_change',
                'value': 'true',
                'data_type': 'boolean',
                'description': 'Allow users to change their own passwords',
                'default_value': 'true'
            },
            {
                'category': 'USER_MANAGEMENT',
                'key': 'password_expiry_days',
                'value': '90',
                'data_type': 'integer',
                'description': 'Number of days before password expires',
                'default_value': '90'
            },
            {
                'category': 'USER_MANAGEMENT',
                'key': 'min_password_length',
                'value': '8',
                'data_type': 'integer',
                'description': 'Minimum password length requirement',
                'default_value': '8'
            },
            {
                'category': 'USER_MANAGEMENT',
                'key': 'session_timeout_hours',
                'value': '24',
                'data_type': 'integer',
                'description': 'Session timeout in hours',
                'default_value': '24'
            },
            
            # System Settings
            {
                'category': 'SYSTEM_SETTINGS',
                'key': 'enable_audit_logging',
                'value': 'true',
                'data_type': 'boolean',
                'description': 'Enable comprehensive audit logging',
                'default_value': 'true',
                'is_system': 'true'
            },
            {
                'category': 'SYSTEM_SETTINGS',
                'key': 'audit_log_retention_days',
                'value': '365',
                'data_type': 'integer',
                'description': 'Number of days to retain audit logs',
                'default_value': '365'
            },
            {
                'category': 'SYSTEM_SETTINGS',
                'key': 'backup_frequency_days',
                'value': '7',
                'data_type': 'integer',
                'description': 'How often to perform system backups (days)',
                'default_value': '7'
            },
            {
                'category': 'SYSTEM_SETTINGS',
                'key': 'default_currency',
                'value': 'NGN',
                'data_type': 'string',
                'description': 'Default currency for asset values',
                'default_value': 'NGN'
            },
            
            # Report Settings
            {
                'category': 'REPORT_SETTINGS',
                'key': 'max_report_records',
                'value': '10000',
                'data_type': 'integer',
                'description': 'Maximum number of records in a single report',
                'default_value': '10000'
            },
            {
                'category': 'REPORT_SETTINGS',
                'key': 'report_cache_hours',
                'value': '1',
                'data_type': 'integer',
                'description': 'Hours to cache report data',
                'default_value': '1'
            },
            {
                'category': 'REPORT_SETTINGS',
                'key': 'auto_generate_monthly_reports',
                'value': 'true',
                'data_type': 'boolean',
                'description': 'Automatically generate monthly summary reports',
                'default_value': 'true'
            }
        ]

        try:
            with get_db() as session:
                for setting in default_settings:
                    existing = session.query(SystemConfiguration).filter(
                        SystemConfiguration.category == setting['category'],
                        SystemConfiguration.key == setting['key']
                    ).first()
                    
                    if not existing:
                        config = SystemConfiguration(**setting)
                        session.add(config)
                
                session.commit()
                # Ensure high-value approval is disabled for all users if user intends to remove the threshold
                try:
                    hv = session.query(SystemConfiguration).filter(
                        SystemConfiguration.category == 'CRUD_RESTRICTIONS',
                        SystemConfiguration.key == 'require_approval_for_high_value_assets'
                    ).first()
                    if hv and hv.value.lower() in ('true', '1', 'yes', 'on'):
                        hv.value = 'false'
                        hv.default_value = 'false'
                        session.commit()
                except Exception:
                    # non-fatal
                    pass
        except Exception as e:
            print(f"Error initializing default settings: {e}")

    def get_setting(self, category: str, key: str, default_value: Any = None) -> Any:
        """Get a specific setting value."""
        try:
            with get_db() as session:
                setting = session.query(SystemConfiguration).filter(
                    SystemConfiguration.category == category,
                    SystemConfiguration.key == key
                ).first()
                
                if not setting:
                    return default_value
                
                return self._convert_value(setting.value, setting.data_type)
        except Exception:
            return default_value

    def set_setting(self, category: str, key: str, value: Any, 
                   updated_by_id: int, description: str = None) -> Dict[str, Any]:
        """Set a specific setting value."""
        try:
            with get_db() as session:
                setting = session.query(SystemConfiguration).filter(
                    SystemConfiguration.category == category,
                    SystemConfiguration.key == key
                ).first()
                
                old_value = None
                if setting:
                    old_value = setting.value
                    setting.value = str(value)
                    setting.updated_at = datetime.utcnow()
                    setting.updated_by_id = updated_by_id
                    if description:
                        setting.description = description
                else:
                    # Create new setting
                    setting = SystemConfiguration(
                        category=category,
                        key=key,
                        value=str(value),
                        description=description or f"{key} setting",
                        updated_by_id=updated_by_id
                    )
                    session.add(setting)
                
                session.commit()
                
                # Log the change
                user = session.query(User).filter(User.id == updated_by_id).first()
                self.audit_service.log_action(
                    action="SETTING_CHANGED",
                    description=f"Setting {category}.{key} changed from '{old_value}' to '{value}'",
                    table_name="system_configuration",
                    record_id=str(setting.id),
                    old_values={'value': old_value} if old_value else None,
                    new_values={'value': str(value)},
                    user_id=updated_by_id,
                    username=user.name if user else None
                )
                
                return {"success": True, "message": "Setting updated successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error updating setting: {str(e)}"}

    def get_settings_by_category(self, category: str) -> Dict[str, Any]:
        """Get all settings for a specific category."""
        try:
            with get_db() as session:
                settings = session.query(SystemConfiguration).filter(
                    SystemConfiguration.category == category
                ).all()
                
                result = {}
                for setting in settings:
                    result[setting.key] = {
                        'value': self._convert_value(setting.value, setting.data_type),
                        'data_type': setting.data_type,
                        'description': setting.description,
                        'default_value': setting.default_value,
                        'is_system': setting.is_system == 'true',
                        'updated_at': setting.updated_at.isoformat() if setting.updated_at else None
                    }
                
                return result
        except Exception as e:
            print(f"Error getting settings for category {category}: {e}")
            return {}

    def get_all_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get all system settings organized by category."""
        try:
            with get_db() as session:
                settings = session.query(SystemConfiguration).all()
                
                result = {}
                for setting in settings:
                    if setting.category not in result:
                        result[setting.category] = {}
                    
                    result[setting.category][setting.key] = {
                        'value': self._convert_value(setting.value, setting.data_type),
                        'data_type': setting.data_type,
                        'description': setting.description,
                        'default_value': setting.default_value,
                        'is_system': setting.is_system == 'true',
                        'updated_at': setting.updated_at.isoformat() if setting.updated_at else None
                    }
                
                return result
        except Exception as e:
            print(f"Error getting all settings: {e}")
            return {}

    def reset_setting_to_default(self, category: str, key: str, 
                                updated_by_id: int) -> Dict[str, Any]:
        """Reset a setting to its default value."""
        try:
            with get_db() as session:
                setting = session.query(SystemConfiguration).filter(
                    SystemConfiguration.category == category,
                    SystemConfiguration.key == key
                ).first()
                
                if not setting or not setting.default_value:
                    return {"success": False, "message": "Setting not found or no default value"}
                
                old_value = setting.value
                setting.value = setting.default_value
                setting.updated_at = datetime.utcnow()
                setting.updated_by_id = updated_by_id
                
                session.commit()
                
                # Log the change
                user = session.query(User).filter(User.id == updated_by_id).first()
                self.audit_service.log_action(
                    action="SETTING_RESET",
                    description=f"Setting {category}.{key} reset to default value '{setting.default_value}'",
                    table_name="system_configuration",
                    record_id=str(setting.id),
                    old_values={'value': old_value},
                    new_values={'value': setting.default_value},
                    user_id=updated_by_id,
                    username=user.name if user else None
                )
                
                return {"success": True, "message": "Setting reset to default successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error resetting setting: {str(e)}"}

    def _convert_value(self, value: str, data_type: str) -> Any:
        """Convert string value to appropriate data type."""
        if not value:
            return None
            
        try:
            if data_type == 'boolean':
                return value.lower() in ('true', '1', 'yes', 'on')
            elif data_type == 'integer':
                return int(value)
            elif data_type == 'float':
                return float(value)
            elif data_type == 'json':
                return json.loads(value)
            else:  # string
                return value
        except (ValueError, json.JSONDecodeError):
            return value

    # Convenience methods for common CRUD restrictions
    def can_create_asset(self) -> bool:
        """Check if asset creation is allowed."""
        return self.get_setting('CRUD_RESTRICTIONS', 'allow_asset_creation', True)

    def can_edit_asset(self) -> bool:
        """Check if asset editing is allowed."""
        return self.get_setting('CRUD_RESTRICTIONS', 'allow_asset_editing', True)

    def can_delete_asset(self) -> bool:
        """Check if asset deletion is allowed."""
        return self.get_setting('CRUD_RESTRICTIONS', 'allow_asset_deletion', True)

    def requires_high_value_approval(self) -> bool:
        """Check if high-value assets require approval.

        NOTE: This setting is kept for backward compatibility. The application
        currently treats high-value flagging as informational/non-blocking by
        default. The method returns the stored setting (default False).
        """
        return self.get_setting('CRUD_RESTRICTIONS', 'require_approval_for_high_value_assets', False)

    def get_high_value_threshold(self) -> float:
        """Get the threshold for high-value assets."""
        return self.get_setting('CRUD_RESTRICTIONS', 'high_value_asset_threshold', 10000.0)

    def can_bulk_operate(self) -> bool:
        """Check if bulk operations are allowed."""
        return self.get_setting('CRUD_RESTRICTIONS', 'allow_bulk_operations', False)

    def get_max_assets_per_user(self) -> int:
        """Get maximum assets per user."""
        return self.get_setting('CRUD_RESTRICTIONS', 'max_assets_per_user', 100)

    def get_session_timeout_hours(self) -> int:
        """Get session timeout in hours."""
        return self.get_setting('USER_MANAGEMENT', 'session_timeout_hours', 24)

    def get_min_password_length(self) -> int:
        """Get minimum password length."""
        return self.get_setting('USER_MANAGEMENT', 'min_password_length', 8)

    def is_audit_logging_enabled(self) -> bool:
        """Check if audit logging is enabled."""
        return self.get_setting('SYSTEM_SETTINGS', 'enable_audit_logging', True)

    def export_settings(self) -> Dict[str, Any]:
        """Export all settings for backup purposes."""
        try:
            settings = self.get_all_settings()
            return {
                'export_timestamp': datetime.utcnow().isoformat(),
                'settings': settings
            }
        except Exception as e:
            return {'error': str(e)}

    def import_settings(self, settings_data: Dict[str, Any], 
                       updated_by_id: int) -> Dict[str, Any]:
        """Import settings from backup data."""
        try:
            if 'settings' not in settings_data:
                return {"success": False, "message": "Invalid settings data format"}
            
            imported_count = 0
            errors = []
            
            for category, category_settings in settings_data['settings'].items():
                for key, setting_data in category_settings.items():
                    if isinstance(setting_data, dict) and 'value' in setting_data:
                        result = self.set_setting(
                            category, key, setting_data['value'], 
                            updated_by_id, setting_data.get('description')
                        )
                        if result['success']:
                            imported_count += 1
                        else:
                            errors.append(f"{category}.{key}: {result['message']}")
            
            return {
                "success": True,
                "message": f"Imported {imported_count} settings",
                "errors": errors
            }
        except Exception as e:
            return {"success": False, "message": f"Error importing settings: {str(e)}"}
