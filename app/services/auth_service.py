import secrets
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.models import User, UserSession, AuditLog, Role, UserRole
from .audit_service import AuditService
from .config_service import ConfigService
from passlib.context import CryptContext


class AuthService:
    def __init__(self):
        self.audit_service = AuditService()
        self.config_service = ConfigService()
        self._current_user = None
        self._current_session = None
        # Centralized password hashing configuration
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    def get_current_session(self) -> Optional[UserSession]:
        """Get the current active session"""
        if not self._current_session:
            return None
            
        with get_db() as session:
            # Get fresh session data
            current = session.query(UserSession).filter(
                UserSession.session_token == self._current_session.session_token,
                UserSession.is_active == "Active"
            ).first()
            
            if not current:
                self._current_session = None
                self._current_user = None
                
            return current

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash using bcrypt."""
        # Try to use bcrypt module directly (with truncation to 72 bytes) for compatibility
        try:
            import bcrypt
            pw_bytes = password.encode('utf-8')[:72]
            return bcrypt.checkpw(pw_bytes, password_hash.encode('utf-8'))
        except Exception:
            # Fallback to passlib (supports bcrypt_sha256 and bcrypt)
            try:
                pwd_ctx = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")
                return pwd_ctx.verify(password, password_hash)
            except Exception:
                # As a last resort, try truncated password with passlib
                try:
                    truncated = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
                    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
                    return pwd_ctx.verify(truncated, password_hash)
                except Exception:
                    return False

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt with length validation."""
        # Prefer to use bcrypt module directly to control truncation behavior
        try:
            import bcrypt
            pw_bytes = password.encode('utf-8')[:72]
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(pw_bytes, salt)
            return hashed.decode('utf-8')
        except Exception:
            # Fallback to passlib
            try:
                pwd_ctx = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")
                return pwd_ctx.hash(password)
            except Exception as e:
                # If passlib bcrypt fails due to long password, truncate and try bcrypt via passlib
                try:
                    truncated = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
                    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
                    return pwd_ctx.hash(truncated)
                except Exception as e2:
                    raise ValueError(f"Failed to hash password: {e2}")

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and create session.
        
        Returns:
            Dict with success status, message, user data, and session token
        """
        # Check for admin login using secure configuration
        admin_creds = self.config_service.get_admin_credentials()
        if email == admin_creds["email"] and password == admin_creds["password"]:
            # Create admin user object for session - use a simple class
            class DefaultAdminUser:
                def __init__(self):
                    self.id = 0
                    self.name = "System Admin"
                    self.email = "admin@company.com"
                    self.department = "Administration"
                    self.position = "System Administrator"
                    self.role = "Admin"
                    self.is_active = "Active"
                    self.last_login = datetime.utcnow()
            
            # Create admin user object
            admin_user = DefaultAdminUser()
            session_token = f"admin-{secrets.token_hex(16)}"
            
            # Create session object for admin (in-memory only)
            class AdminSession:
                def __init__(self):
                    self.session_token = session_token
                    self.is_active = "Active"
                    self.login_time = datetime.utcnow()
                    self.last_activity = datetime.utcnow()
                    self.user_id = 0  # Special admin user ID
            
            admin_session = AdminSession()
            
            # Store current user and session for later use
            self._current_user = admin_user
            self._current_session = admin_session
            
            # Create user data for response
            user_data = {
                "id": 0,
                "name": "System Admin",
                "email": admin_creds["email"],
                "department": "Administration",
                "position": "System Administrator",
                "role": "Admin",
                "is_active": "Active",
                "last_login": datetime.utcnow().isoformat(),
                "is_default_admin": self.config_service.is_using_default_credentials()
            }
            
            # Log successful admin login
            try:
                self.audit_service.log_action(
                    action="ADMIN_LOGIN",
                    description="Default admin login successful",
                    user_id=0
                )
            except Exception as e:
                print(f"Audit logging failed: {e}")  # Don't let audit logging failure block admin login
                
            return {
                "success": True,
                "message": "Login successful (System Admin)",
                "user": user_data,
                "session_token": session_token
            }
        
        with get_db() as session:
            try:
                # Find user by email
                user = session.query(User).filter(User.email == email).first()
                
                if not user:
                    # Log failed login attempt
                    self.audit_service.log_action(
                        action="LOGIN_FAILED",
                        description=f"Login attempt with non-existent email: {email}"
                    )
                    return {
                        "success": False,
                        "message": "Invalid email or password",
                        "user": None,
                        "session_token": None
                    }

                # Check if user is active
                if user.is_active != "Active":
                    self.audit_service.log_action(
                        action="LOGIN_BLOCKED",
                        description=f"Login attempt by inactive user: {user.email} (Status: {user.is_active})",
                        user_id=user.id,
                        username=user.name
                    )
                    return {
                        "success": False,
                        "message": f"Account is {user.is_active.lower()}. Please contact administrator.",
                        "user": None,
                        "session_token": None
                    }

                # Verify password
                if not self.verify_password(password, user.password_hash):
                    self.audit_service.log_action(
                        action="LOGIN_FAILED",
                        description=f"Invalid password for user: {user.email}",
                        user_id=user.id,
                        username=user.name
                    )
                    return {
                        "success": False,
                        "message": "Invalid email or password",
                        "user": None,
                        "session_token": None
                    }

                # Clean up old sessions
                old_sessions = session.query(UserSession).filter(
                    UserSession.user_id == user.id,
                    UserSession.is_active == "Active"
                ).all()
                for old_session in old_sessions:
                    old_session.is_active = "Expired"
                
                # Create new session
                session_token = secrets.token_urlsafe(64)
                user_session = UserSession(
                    user_id=user.id,
                    session_token=session_token,
                    is_active="Active"
                )
                session.add(user_session)

                # Get user role information before updating (while still in session)
                role_name = "Unknown"
                if user.role:
                    try:
                        # Handle both enum and direct string role names
                        if hasattr(user.role.name, 'value'):
                            role_name = user.role.name.value
                        else:
                            role_name = str(user.role.name)
                    except:
                        role_name = "Unknown"

                # Collect user data while still in session
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "department": user.department,
                    "position": user.position,
                    "role": role_name,
                    "is_active": user.is_active,
                }

                # Update user's last login
                user.last_login = datetime.utcnow()
                user_data["last_login"] = user.last_login.isoformat() if user.last_login else None
                
                session.commit()

                # Set current user and session (store plain dict to avoid keeping ORM instance across sessions)
                self._current_user = user_data
                self._current_session = user_session

                # Log successful login
                self.audit_service.log_action(
                    action="LOGIN_SUCCESS",
                    description=f"User logged in successfully: {user_data['email']}",
                    user_id=user_data['id'],
                    username=user_data['name']
                )

                return {
                    "success": True,
                    "message": "Login successful",
                    "user": user_data,
                    "session_token": session_token
                }

            except Exception as e:
                session.rollback()
                self.audit_service.log_action(
                    action="LOGIN_ERROR",
                    description=f"Login error for {email}: {str(e)}"
                )
                return {
                    "success": False,
                    "message": "An error occurred during login. Please try again.",
                    "user": None,
                    "session_token": None
                }

    def logout(self, session_token: str = None) -> Dict[str, Any]:
        """
        Logout user and invalidate session.
        """
        if not session_token and self._current_session:
            session_token = self._current_session.session_token

        with get_db() as session:
            try:
                user_session = session.query(UserSession).filter(
                    UserSession.session_token == session_token,
                    UserSession.is_active == "Active"
                ).first()

                if user_session:
                    user_session.logout_time = datetime.utcnow()
                    user_session.is_active = "Expired"
                    
                    user = session.query(User).filter(User.id == user_session.user_id).first()
                    
                    session.commit()

                    # Log logout
                    self.audit_service.log_action(
                        action="LOGOUT",
                        description=f"User logged out: {user.email if user else 'Unknown'}",
                        user_id=user.id if user else None,
                        username=user.name if user else None
                    )

                    # Clear current user and session
                    self._current_user = None
                    self._current_session = None

                    return {
                        "success": True,
                        "message": "Logged out successfully"
                    }
                else:
                    return {
                        "success": False,
                        "message": "Invalid session"
                    }

            except Exception as e:
                session.rollback()
                return {
                    "success": False,
                    "message": f"Logout error: {str(e)}"
                }

    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Validate session token and return user info if valid.
        """
        with get_db() as session:
            try:
                user_session = session.query(UserSession).filter(
                    UserSession.session_token == session_token,
                    UserSession.is_active == "Active"
                ).first()

                if not user_session:
                    return None

                # Check if session has expired (24 hours)
                if user_session.last_activity < datetime.utcnow() - timedelta(hours=24):
                    user_session.is_active = "Expired"
                    session.commit()
                    return None

                # Update last activity
                user_session.last_activity = datetime.utcnow()
                
                user = session.query(User).filter(User.id == user_session.user_id).first()
                
                if not user or user.is_active != "Active":
                    return None

                # Get user role information and collect all user data before committing
                role_name = "Unknown"
                if user.role:
                    try:
                        # Handle both enum and direct string role names
                        if hasattr(user.role.name, 'value'):
                            role_name = user.role.name.value
                        else:
                            role_name = str(user.role.name)
                    except:
                        role_name = "Unknown"

                # Collect user data while still in session
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "department": user.department,
                    "position": user.position,
                    "role": role_name,
                    "is_active": user.is_active,
                    "last_login": user.last_login.isoformat() if user.last_login else None
                }

                session.commit()

                # Set current user and session (store as plain dict)
                self._current_user = user_data
                self._current_session = user_session

                return user_data

            except Exception as e:
                session.rollback()
                return None

    def get_current_user(self) -> Optional[User]:
        """Get the currently logged in user.

        Returns a plain dict (not an ORM object) when a user is logged in.
        """
        return self._current_user

    def get_current_user_id(self) -> Optional[int]:
        """Get the current user's ID"""
        if not self._current_user:
            return None
        
        # Handle default admin user object
        if hasattr(self._current_user, 'id'):
            return self._current_user.id
        
        # Handle dictionary format (default admin case)
        if isinstance(self._current_user, dict):
            return self._current_user.get('id')
        
        return None

    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        return self._current_user is not None

    def has_permission(self, permission: str) -> bool:
        """Check if current user has specific permission."""
        if not self._current_user:
            return False

        # Handle default admin user (ID 0) - has all permissions
        if hasattr(self._current_user, 'id') and self._current_user.id == 0:
            return True
            
        # Handle default admin user by email
        admin_creds = self.config_service.get_admin_credentials()
        if hasattr(self._current_user, 'email') and self._current_user.email == admin_creds["email"]:
            return True

        # Handle dictionary format (shouldn't happen with new fix, but just in case)
        if isinstance(self._current_user, dict):
            if self._current_user.get('id') == 0 or self._current_user.get('email') == admin_creds["email"]:
                return True

        try:
            with get_db() as session:
                # For regular database users
                user_id = self.get_current_user_id()
                if user_id == 0:  # Default admin
                    return True
                    
                user = session.query(User).filter(User.id == user_id).first()
                if not user or not user.role:
                    return False

                # Admin has all permissions
                if user.role.name == UserRole.ADMIN:
                    return True

                # Check specific permission
                from ..core.models import PermissionType, RolePermission, Permission
                
                perm = session.query(Permission).filter(
                    Permission.name == PermissionType(permission)
                ).first()
                
                if not perm:
                    return False

                role_perm = session.query(RolePermission).filter(
                    RolePermission.role_id == user.role.id,
                    RolePermission.permission_id == perm.id,
                    RolePermission.granted == "true"
                ).first()

                return role_perm is not None

        except Exception as e:
            print(f"Permission check error: {e}")
            return False

    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password after verifying old password."""
        with get_db() as session:
            try:
                user = session.query(User).filter(User.id == user_id).first()
                
                if not user:
                    return {"success": False, "message": "User not found"}

                if not self.verify_password(old_password, user.password_hash):
                    self.audit_service.log_action(
                        action="PASSWORD_CHANGE_FAILED",
                        description=f"Invalid old password for user: {user.email}",
                        user_id=user.id,
                        username=user.name
                    )
                    return {"success": False, "message": "Invalid old password"}

                # Update password
                user.password_hash = self.hash_password(new_password)
                user.password_changed_at = datetime.utcnow()
                
                session.commit()

                self.audit_service.log_action(
                    action="PASSWORD_CHANGED",
                    description=f"Password changed for user: {user.email}",
                    user_id=user.id,
                    username=user.name
                )

                return {"success": True, "message": "Password changed successfully"}

            except Exception as e:
                session.rollback()
                return {"success": False, "message": f"Error changing password: {str(e)}"}

    def reset_password(self, user_id: int, new_password: str, reset_by_user_id: int) -> Dict[str, Any]:
        """Reset user password (admin function)."""
        with get_db() as session:
            try:
                user = session.query(User).filter(User.id == user_id).first()
                reset_by = session.query(User).filter(User.id == reset_by_user_id).first()
                
                if not user:
                    return {"success": False, "message": "User not found"}

                if not reset_by:
                    return {"success": False, "message": "Reset by user not found"}

                # Update password
                user.password_hash = self.hash_password(new_password)
                user.password_changed_at = datetime.utcnow()
                
                session.commit()

                self.audit_service.log_action(
                    action="PASSWORD_RESET",
                    description=f"Password reset for user {user.email} by {reset_by.email}",
                    user_id=reset_by.id,
                    username=reset_by.name,
                    table_name="users",
                    record_id=str(user.id)
                )

                return {"success": True, "message": "Password reset successfully"}

            except Exception as e:
                session.rollback()
                return {"success": False, "message": f"Error resetting password: {str(e)}"}

    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions. Returns number of sessions cleaned up."""
        with get_db() as session:
            try:
                expired_time = datetime.utcnow() - timedelta(hours=24)
                
                expired_sessions = session.query(UserSession).filter(
                    UserSession.last_activity < expired_time,
                    UserSession.is_active == "Active"
                ).all()

                count = 0
                for sess in expired_sessions:
                    sess.is_active = "Expired"
                    sess.logout_time = datetime.utcnow()
                    count += 1

                session.commit()
                return count

            except Exception:
                session.rollback()
                return 0

    def is_admin_user(self) -> bool:
        """Check if the current user is an admin"""
        if not self._current_user:
            return False
            
        # Handle default admin user  
        admin_creds = self.config_service.get_admin_credentials()
        if hasattr(self._current_user, 'email') and self._current_user.email == admin_creds["email"]:
            return True
        elif isinstance(self._current_user, dict) and self._current_user.get('email') == admin_creds["email"]:
            return True
            
        # Handle database user
        if hasattr(self._current_user, 'role'):
            return self._current_user.role == UserRole.ADMIN
            
        return False
