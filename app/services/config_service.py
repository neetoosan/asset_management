"""
Secure Configuration Management Service
Handles secure storage and retrieval of configuration values, including sensitive credentials
"""

import os
import json
import keyring
from typing import Optional, Dict, Any, List
from pathlib import Path
from cryptography.fernet import Fernet
import base64

from ..core.database import get_db
from ..core.models import SystemConfiguration


class ConfigService:
    """
    Secure configuration management service
    Handles both database and system-level configuration with encryption for sensitive data
    """
    
    def __init__(self):
        self.app_name = "AssetManagementSystem"
        self._encryption_key = None
        self._config_cache = {}
    
    def _get_encryption_key(self) -> bytes:
        """Get or create encryption key for sensitive data"""
        if self._encryption_key is not None:
            return self._encryption_key
        
        try:
            # Try to get existing key from keyring
            key_b64 = keyring.get_password(self.app_name, "encryption_key")
            if key_b64:
                self._encryption_key = base64.b64decode(key_b64)
            else:
                # Generate new key and store it securely
                self._encryption_key = Fernet.generate_key()
                key_b64 = base64.b64encode(self._encryption_key).decode()
                keyring.set_password(self.app_name, "encryption_key", key_b64)
            
            return self._encryption_key
            
        except Exception as e:
            print(f"Warning: Could not access keyring for encryption key: {e}")
            # Fallback to a session-only key (not persistent)
            self._encryption_key = Fernet.generate_key()
            return self._encryption_key
    
    def _encrypt_value(self, value: str) -> str:
        """Encrypt a sensitive value"""
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            encrypted_value = fernet.encrypt(value.encode())
            return base64.b64encode(encrypted_value).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return value  # Return unencrypted as fallback
    
    def _decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt a sensitive value"""
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            encrypted_bytes = base64.b64decode(encrypted_value.encode())
            decrypted_value = fernet.decrypt(encrypted_bytes)
            return decrypted_value.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_value  # Return as-is if decryption fails
    
    def get_database_url(self) -> str:
        """Get database URL from environment or secure storage"""
        # First check environment variable
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url
        
        # Check secure storage
        try:
            encrypted_url = keyring.get_password(self.app_name, "database_url")
            if encrypted_url:
                return self._decrypt_value(encrypted_url)
        except Exception as e:
            print(f"Could not retrieve database URL from secure storage: {e}")
        
        # Fallback to default (for development only)
        default_url = "postgresql://asset_management_6rk8_user:NmCuRP2LGcBfKRrOknhy7mH27tARHlu3@dpg-d33mc2vdiees739mg4v0-a.oregon-postgres.render.com/asset_management_6rk8"
        print("WARNING: Using default database URL. Set DATABASE_URL environment variable or configure secure storage.")
        return default_url
    
    def set_database_url(self, database_url: str) -> bool:
        """Store database URL securely"""
        try:
            encrypted_url = self._encrypt_value(database_url)
            keyring.set_password(self.app_name, "database_url", encrypted_url)
            return True
        except Exception as e:
            print(f"Could not store database URL securely: {e}")
            return False
    
    def get_admin_credentials(self) -> Dict[str, str]:
        """Get admin credentials from secure storage or environment"""
        # Check environment variables first
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        if admin_email and admin_password:
            return {"email": admin_email, "password": admin_password}
        
        # Check secure storage
        try:
            stored_email = keyring.get_password(self.app_name, "admin_email")
            stored_password = keyring.get_password(self.app_name, "admin_password")
            
            if stored_email and stored_password:
                return {
                    "email": self._decrypt_value(stored_email),
                    "password": self._decrypt_value(stored_password)
                }
        except Exception as e:
            print(f"Could not retrieve admin credentials: {e}")
        
        # Return default credentials (should be changed after first use)
        print("WARNING: Using default admin credentials. Please change them after first login.")
        return {
            "email": "admin@company.com",
            "password": "admin123"
        }
    
    def set_admin_credentials(self, email: str, password: str) -> bool:
        """Store admin credentials securely"""
        try:
            encrypted_email = self._encrypt_value(email)
            encrypted_password = self._encrypt_value(password)
            
            keyring.set_password(self.app_name, "admin_email", encrypted_email)
            keyring.set_password(self.app_name, "admin_password", encrypted_password)
            
            return True
        except Exception as e:
            print(f"Could not store admin credentials: {e}")
            return False
    
    def is_using_default_credentials(self) -> bool:
        """Check if system is still using default admin credentials"""
        creds = self.get_admin_credentials()
        return creds["email"] == "admin@company.com" and creds["password"] == "admin123"
    
    def get_system_config(self, category: str, key: str, default=None) -> Any:
        """Get system configuration value"""
        cache_key = f"{category}:{key}"
        
        # Check cache first
        if cache_key in self._config_cache:
            return self._config_cache[cache_key]
        
        try:
            with get_db() as session:
                config = session.query(SystemConfiguration).filter(
                    SystemConfiguration.category == category,
                    SystemConfiguration.key == key
                ).first()
                
                if config:
                    value = self._parse_config_value(config.value, config.data_type)
                    self._config_cache[cache_key] = value
                    return value
                
        except Exception as e:
            print(f"Error getting system config {category}:{key}: {e}")
        
        return default
    
    def set_system_config(self, category: str, key: str, value: Any, 
                         data_type: str = "string", description: str = "", 
                         is_system: bool = False, user_id: Optional[int] = None) -> bool:
        """Set system configuration value"""
        try:
            with get_db() as session:
                config = session.query(SystemConfiguration).filter(
                    SystemConfiguration.category == category,
                    SystemConfiguration.key == key
                ).first()
                
                if config:
                    # Update existing
                    config.value = self._serialize_config_value(value, data_type)
                    config.data_type = data_type
                    config.updated_by_id = user_id
                else:
                    # Create new
                    config = SystemConfiguration(
                        category=category,
                        key=key,
                        value=self._serialize_config_value(value, data_type),
                        data_type=data_type,
                        description=description,
                        is_system="true" if is_system else "false",
                        updated_by_id=user_id
                    )
                    session.add(config)
                
                session.commit()
                
                # Update cache
                cache_key = f"{category}:{key}"
                self._config_cache[cache_key] = value
                
                return True
                
        except Exception as e:
            print(f"Error setting system config {category}:{key}: {e}")
            return False
    
    def _parse_config_value(self, value: str, data_type: str) -> Any:
        """Parse configuration value based on data type"""
        try:
            if data_type == "boolean":
                return value.lower() in ("true", "1", "yes", "on")
            elif data_type == "integer":
                return int(value)
            elif data_type == "float":
                return float(value)
            elif data_type == "json":
                return json.loads(value)
            else:  # string
                return value
        except Exception:
            return value  # Return as string if parsing fails
    
    def _serialize_config_value(self, value: Any, data_type: str) -> str:
        """Serialize configuration value for storage"""
        try:
            if data_type == "json":
                return json.dumps(value)
            elif data_type == "boolean":
                return "true" if value else "false"
            else:
                return str(value)
        except Exception:
            return str(value)
    
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security-related settings"""
        return {
            "min_password_length": self.get_system_config("SECURITY", "min_password_length", 8),
            "password_complexity_required": self.get_system_config("SECURITY", "password_complexity_required", True),
            "session_timeout_minutes": self.get_system_config("SECURITY", "session_timeout_minutes", 1440),  # 24 hours
            "inactivity_timeout_minutes": self.get_system_config("SECURITY", "inactivity_timeout_minutes", 30),
            "max_login_attempts": self.get_system_config("SECURITY", "max_login_attempts", 5),
            "lockout_duration_minutes": self.get_system_config("SECURITY", "lockout_duration_minutes", 15),
            "require_password_change_on_first_login": self.get_system_config("SECURITY", "require_password_change_first_login", True),
        }
    
    def initialize_default_security_settings(self, user_id: Optional[int] = None) -> bool:
        """Initialize default security settings"""
        try:
            settings = self.get_security_settings()
            
            # Set defaults if they don't exist
            defaults = {
                ("SECURITY", "min_password_length", 8, "integer", "Minimum required password length"),
                ("SECURITY", "password_complexity_required", True, "boolean", "Require password complexity"),
                ("SECURITY", "session_timeout_minutes", 1440, "integer", "Session timeout in minutes (24 hours)"),
                ("SECURITY", "inactivity_timeout_minutes", 30, "integer", "Inactivity timeout in minutes"),
                ("SECURITY", "max_login_attempts", 5, "integer", "Maximum failed login attempts before lockout"),
                ("SECURITY", "lockout_duration_minutes", 15, "integer", "Account lockout duration in minutes"),
                ("SECURITY", "require_password_change_first_login", True, "boolean", "Require password change on first login"),
            }
            
            for category, key, default_value, data_type, description in defaults:
                if self.get_system_config(category, key) is None:
                    self.set_system_config(category, key, default_value, data_type, description, True, user_id)
            
            return True
            
        except Exception as e:
            print(f"Error initializing default security settings: {e}")
            return False
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength based on security settings"""
        settings = self.get_security_settings()
        
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check minimum length
        min_length = settings["min_password_length"]
        if len(password) < min_length:
            result["valid"] = False
            result["errors"].append(f"Password must be at least {min_length} characters long")
        
        # Check complexity if required
        if settings["password_complexity_required"]:
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
            
            if not has_upper:
                result["errors"].append("Password must contain at least one uppercase letter")
                result["valid"] = False
            
            if not has_lower:
                result["errors"].append("Password must contain at least one lowercase letter")
                result["valid"] = False
            
            if not has_digit:
                result["errors"].append("Password must contain at least one digit")
                result["valid"] = False
            
            if not has_special:
                result["errors"].append("Password must contain at least one special character")
                result["valid"] = False
        
        # Check for common weak passwords
        weak_passwords = ["password", "123456", "password123", "admin", "admin123"]
        if password.lower() in weak_passwords:
            result["valid"] = False
            result["errors"].append("Password is too common and easily guessed")
        
        return result
    
    def clear_cache(self):
        """Clear configuration cache"""
        self._config_cache.clear()
    
    def export_non_sensitive_config(self) -> Dict[str, Any]:
        """Export non-sensitive configuration for backup"""
        try:
            with get_db() as session:
                configs = session.query(SystemConfiguration).filter(
                    SystemConfiguration.is_system == "false"
                ).all()
                
                export_data = {}
                for config in configs:
                    category_key = f"{config.category}:{config.key}"
                    export_data[category_key] = {
                        "value": config.value,
                        "data_type": config.data_type,
                        "description": config.description,
                        "created_at": config.created_at.isoformat() if config.created_at else None,
                        "updated_at": config.updated_at.isoformat() if config.updated_at else None
                    }
                
                return export_data
                
        except Exception as e:
            print(f"Error exporting configuration: {e}")
            return {}