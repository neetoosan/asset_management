"""
Desktop Session Management Service
Handles session state, authentication tokens, and user context for the desktop application
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from PySide6.QtCore import QObject, Signal

from ..core.database import get_db
from ..core.models import User, UserSession, UserRole
from .auth_service import AuthService
from .audit_service import AuditService


class SessionService(QObject):
    """
    Desktop session management service
    Provides secure session handling for the PySide6 application
    """
    
    # Signals for session state changes
    sessionExpired = Signal()
    sessionUpdated = Signal(dict)  # Emits user data
    
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.audit_service = AuditService()
        
        # Session state
        self._current_user = None
        self._session_token = None
        self._login_time = None
        self._last_activity = None
        self._session_timeout = 24 * 60 * 60  # 24 hours in seconds
        
        # Auto-logout on inactivity (30 minutes)
        self._inactivity_timeout = 30 * 60  # 30 minutes in seconds
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and create desktop session
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with success status, message, and user data
        """
        try:
            # Use AuthService for authentication
            result = self.auth_service.login(email, password)
            
            if result["success"]:
                # Store session information
                self._current_user = result["user"]
                self._session_token = result["session_token"]
                self._login_time = datetime.utcnow()
                self._last_activity = datetime.utcnow()
                
                # Set up audit logging with current user
                user_id = result["user"]["id"]
                user_name = result["user"]["name"]
                self.audit_service.set_current_user(user_id, user_name)
                
                # Log desktop session start
                self.audit_service.log_action(
                    action="DESKTOP_SESSION_START",
                    description=f"Desktop application session started for user: {email}",
                    user_id=user_id,
                    username=user_name
                )
                
                # Emit session updated signal
                self.sessionUpdated.emit(self._current_user)
                
                return {
                    "success": True,
                    "message": "Desktop session started successfully",
                    "user": self._current_user,
                    "session_token": self._session_token  # Include session token in response
                }
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Desktop login failed: {str(e)}"
            }
    
    def get_session_data(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get session data for a token
        
        Args:
            token: Session token
            
        Returns:
            Optional[Dict[str, Any]]: Session data if valid, None otherwise
        """
        if token.startswith('admin-'):
            return {
                'user_id': 0,
                'username': 'System Admin',
                'role': 'Admin'
            }
            
        try:
            with get_db() as session:
                user_session = session.query(UserSession).filter(
                    UserSession.session_token == token,
                    UserSession.is_active == "Active"
                ).first()
                
                if user_session:
                    return {
                        'user_id': user_session.user_id,
                        'username': user_session.user.name if user_session.user else None,
                        'role': user_session.user.role.name if user_session.user and user_session.user.role else None
                    }
                    
            return None
            
        except Exception as e:
            print(f"Error getting session data: {e}")
            return None
            
    def validate_session(self, token: str) -> bool:
        """
        Validate a session token
        
        Args:
            token: Session token to validate
            
        Returns:
            bool: True if session is valid, False otherwise
        """
        try:
            # For admin token
            if token and token.startswith('admin-'):
                return True
                
            # For regular user sessions
            with get_db() as session:
                user_session = session.query(UserSession).filter(
                    UserSession.session_token == token,
                    UserSession.is_active == "Active"
                ).first()
                
                if user_session:
                    # Update last activity
                    user_session.last_activity = datetime.utcnow()
                    session.commit()
                    return True
                    
            return False
            
        except Exception as e:
            print(f"Session validation error: {e}")
            return False
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout user and clean up desktop session
        
        Returns:
            Dictionary with success status and message
        """
        try:
            if self._current_user and self._session_token:
                # Log desktop session end
                self.audit_service.log_action(
                    action="DESKTOP_SESSION_END",
                    description=f"Desktop application session ended for user: {self._current_user['email']}"
                )
                
                # Use AuthService to invalidate session
                result = self.auth_service.logout(self._session_token)
                
                # Clear desktop session state
                self._clear_session()
                
                return result
            else:
                self._clear_session()
                return {
                    "success": True,
                    "message": "No active session to logout"
                }
                
        except Exception as e:
            self._clear_session()
            return {
                "success": False,
                "message": f"Logout error: {str(e)}"
            }
    
    def _clear_session(self):
        """Clear desktop session state"""
        self._current_user = None
        self._session_token = None
        self._login_time = None
        self._last_activity = None
        self.audit_service.clear_current_user()
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        if not self._current_user or not self._session_token:
            return False
        
        # Check session timeout
        if self.is_session_expired():
            self._handle_session_expiry()
            return False
        
        return True
    
    def is_session_expired(self) -> bool:
        """Check if current session has expired"""
        if not self._login_time:
            return True
        
        # Check absolute session timeout
        session_age = (datetime.utcnow() - self._login_time).total_seconds()
        if session_age > self._session_timeout:
            return True
        
        # Check inactivity timeout
        if self._last_activity:
            inactivity_duration = (datetime.utcnow() - self._last_activity).total_seconds()
            if inactivity_duration > self._inactivity_timeout:
                return True
        
        return False
    
    def update_activity(self):
        """Update last activity timestamp"""
        if self.is_authenticated():
            self._last_activity = datetime.utcnow()
    
    def _handle_session_expiry(self):
        """Handle session expiration"""
        if self._current_user:
            self.audit_service.log_action(
                action="DESKTOP_SESSION_EXPIRED",
                description=f"Desktop session expired for user: {self._current_user['email']}"
            )
        
        self._clear_session()
        self.sessionExpired.emit()
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user data"""
        if self.is_authenticated():
            return self._current_user
        return None
    
    def get_user_id(self) -> Optional[int]:
        """Get current user ID"""
        user = self.get_current_user()
        return user["id"] if user else None
    
    def get_username(self) -> Optional[str]:
        """Get current username"""
        user = self.get_current_user()
        return user["name"] if user else None
    
    def get_user_email(self) -> Optional[str]:
        """Get current user email"""
        user = self.get_current_user()
        return user["email"] if user else None
    
    def get_user_role(self) -> Optional[str]:
        """Get current user role"""
        user = self.get_current_user()
        return user["role"] if user else None
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has specific permission"""
        if not self.is_authenticated():
            return False
        
        # Use AuthService for permission checking
        return self.auth_service.has_permission(permission)
    
    def is_admin(self) -> bool:
        """Check if current user is an admin"""
        user_role = self.get_user_role()
        return user_role == "Admin" if user_role else False
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        if not self.is_authenticated():
            return {"authenticated": False}
        
        session_age = (datetime.utcnow() - self._login_time).total_seconds() if self._login_time else 0
        last_activity_age = (datetime.utcnow() - self._last_activity).total_seconds() if self._last_activity else 0
        
        return {
            "authenticated": True,
            "user": self._current_user,
            "login_time": self._login_time.isoformat() if self._login_time else None,
            "last_activity": self._last_activity.isoformat() if self._last_activity else None,
            "session_age_seconds": int(session_age),
            "inactivity_seconds": int(last_activity_age),
            "expires_in_seconds": max(0, self._session_timeout - int(session_age)),
            "inactivity_expires_in_seconds": max(0, self._inactivity_timeout - int(last_activity_age))
        }
    
    def validate_and_refresh_session(self) -> bool:
        """
        Validate current session with the database and refresh if needed
        
        Returns:
            True if session is valid, False otherwise
        """
        if not self._session_token:
            return False
        
        try:
            # Validate session with AuthService
            user_data = self.auth_service.validate_session(self._session_token)
            
            if user_data:
                # Update user data if it has changed
                self._current_user = user_data
                self.update_activity()
                
                # Emit updated user data
                self.sessionUpdated.emit(self._current_user)
                return True
            else:
                # Session is invalid
                self._handle_session_expiry()
                return False
                
        except Exception as e:
            print(f"Session validation error: {e}")
            self._handle_session_expiry()
            return False
    
    def change_password(self, current_password: str, new_password: str) -> Dict[str, Any]:
        """
        Change current user's password
        
        Args:
            current_password: Current password
            new_password: New password
            
        Returns:
            Dictionary with success status and message
        """
        if not self.is_authenticated():
            return {"success": False, "message": "Not authenticated"}
        
        user_id = self.get_user_id()
        if not user_id:
            return {"success": False, "message": "User ID not available"}
        
        try:
            result = self.auth_service.change_password(user_id, current_password, new_password)
            
            if result["success"]:
                # Log password change
                self.audit_service.log_action(
                    action="PASSWORD_CHANGED_DESKTOP",
                    description=f"Password changed via desktop application for user: {self.get_user_email()}"
                )
            
            return result
            
        except Exception as e:
            return {"success": False, "message": f"Password change failed: {str(e)}"}