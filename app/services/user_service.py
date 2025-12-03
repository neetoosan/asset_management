from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_, and_, inspect
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
from passlib.context import CryptContext

from ..core.models import (
    User, Role, Permission, RolePermission, UserRole, PermissionType, UserSession
)
from ..core.database import get_db
from .audit_service import AuditService
from .settings_service import SettingsService
from .auth_service import AuthService


class UserService:
    def __init__(self):
        self.audit_service = AuditService()
        self.settings_service = SettingsService()
        self._current_user_id = None
        self._current_user_name = None
        # Initialize auth service lazily to avoid circular imports at module import time
        try:
            from .auth_service import AuthService
            self.auth_service = AuthService()
        except Exception:
            # If import fails for circular import reasons, set to None and create on demand
            self.auth_service = None
        
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt (consistent with AuthService)."""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash using bcrypt (consistent with AuthService)."""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        try:
            return pwd_context.verify(password, password_hash)
        except Exception:
            return False
    
    def set_current_user(self, user_id: int, user_name: str):
        """Set current user for audit logging."""
        self._current_user_id = user_id
        self._current_user_name = user_name
        self.audit_service.set_current_user(user_id, user_name)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with role information and pagination"""
        try:
            with get_db() as session:
                # First check if we have the User table
                inspector = inspect(session.bind)
                if 'users' not in inspector.get_table_names():
                    print("User table does not exist")
                    return []
                    
                users = (session.query(User)
                          .options(joinedload(User.role))
                          .filter(User.deleted_at == None)
                          .order_by(User.created_at.desc())
                          .offset(skip)
                          .limit(limit)
                          .all())
                return [self._user_to_dict(u) for u in users]
        except Exception as query_error:
            print(f"Database query error: {query_error}")
            return []
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            with get_db() as session:
                user = session.query(User).options(joinedload(User.role)).filter(
                    User.id == user_id
                ).first()
                
                return self._user_to_dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            with get_db() as session:
                user = session.query(User).options(joinedload(User.role)).filter(
                    User.email == email
                ).first()
                
                return self._user_to_dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def get_all_roles(self) -> List[Dict[str, Any]]:
        """Get all available roles"""
        try:
            with get_db() as session:
                roles = session.query(Role).all()
                
                return [{
                    'id': role.id,
                    'name': role.name.value,
                    'description': role.description
                } for role in roles]
        except Exception as e:
            print(f"Error getting roles: {e}")
            return []
    
    def get_all_permissions(self) -> List[Dict[str, Any]]:
        """Get all available permissions"""
        try:
            with get_db() as session:
                permissions = session.query(Permission).all()
                
                return [{
                    'id': permission.id,
                    'name': permission.name.value,
                    'description': permission.description
                } for permission in permissions]
        except Exception as e:
            print(f"Error getting permissions: {e}")
            return []
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Get permissions for a specific user"""
        try:
            with get_db() as session:
                user = session.query(User).options(joinedload(User.role)).filter(
                    User.id == user_id
                ).first()
                
                if not user or not user.role:
                    return []
                
                # Get role permissions
                role_permissions = session.query(RolePermission).filter(
                    RolePermission.role_id == user.role.id,
                    RolePermission.granted == "true"
                ).all()
                
                # Get permission names
                permission_ids = [rp.permission_id for rp in role_permissions]
                permissions = session.query(Permission).filter(
                    Permission.id.in_(permission_ids)
                ).all()
                
                return [perm.name.value for perm in permissions]
        except Exception as e:
            print(f"Error getting user permissions: {e}")
            return []
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user with validation and audit logging"""
        try:
            with get_db() as session:
                # Check if user already exists
                existing_user = session.query(User).filter(
                    User.email == user_data.get('email')
                ).first()
                
                if existing_user:
                    return {
                        "success": False,
                        "message": "User with this email already exists"
                    }
                
                # Validate required fields
                required_fields = ['name', 'email', 'password']
                for field in required_fields:
                    if not user_data.get(field):
                        return {
                            "success": False,
                            "message": f"Field '{field}' is required"
                        }
                
                # Validate email format
                if '@' not in user_data['email']:
                    return {
                        "success": False,
                        "message": "Invalid email format"
                    }
                
                # Validate password strength
                password = user_data['password']
                min_length = self.settings_service.get_min_password_length()
                if len(password) < min_length:
                    return {
                        "success": False,
                        "message": f"Password must be at least {min_length} characters long"
                    }
                
                # Get or create role
                role_name = user_data.get('role', 'User')
                try:
                    user_role = UserRole(role_name)
                except ValueError:
                    user_role = UserRole.USER
                
                role = session.query(Role).filter(Role.name == user_role).first()
                if not role:
                    # Create default roles if they don't exist
                    self._initialize_default_roles(session)
                    role = session.query(Role).filter(Role.name == user_role).first()
                
                # Hash password using centralized AuthService when available to ensure compatibility
                if self.auth_service:
                    try:
                        password_hash = self.auth_service.hash_password(password)
                    except Exception:
                        password_hash = self.hash_password(password)
                else:
                    password_hash = self.hash_password(password)
                
                # Create user
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password_hash=password_hash,
                    department=user_data.get('department'),
                    position=user_data.get('position'),
                    role_id=role.id,
                    is_active=user_data.get('is_active', 'Active')
                )
                
                session.add(user)
                # Flush to assign an ID and ensure relationships are available while still bound
                session.flush()

                # Convert to dict while still bound to the session
                result_user = self._user_to_dict(user)

                # Commit the transaction
                session.commit()

                # Audit logging (provide plain dicts)
                try:
                    self.audit_service.log_action(
                        action="USER_CREATED",
                        description=f"Created user: {result_user.get('name')} ({result_user.get('email')})",
                        table_name="users",
                        record_id=str(result_user.get('id')),
                        new_values={k: v for k, v in result_user.items() if k != 'password_changed_at'}
                    )
                except Exception:
                    # Audit failure shouldn't block user creation
                    pass

                return {
                    "success": True,
                    "message": "User created successfully",
                    "user": result_user
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating user: {str(e)}"
            }
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user with validation and audit logging"""
        try:
            with get_db() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return {"success": False, "message": "User not found"}
                
                # Store old values for audit
                old_values = self._user_to_dict(user, include_sensitive=False)
                
                # Check if email is being changed and if it already exists
                if 'email' in user_data and user_data['email'] != user.email:
                    existing_user = session.query(User).filter(
                        User.email == user_data['email'],
                        User.id != user_id
                    ).first()
                    
                    if existing_user:
                        return {
                            "success": False,
                            "message": "Another user with this email already exists"
                        }
                
                # Handle role changes
                if 'role' in user_data:
                    try:
                        user_role = UserRole(user_data['role'])
                        role = session.query(Role).filter(Role.name == user_role).first()
                        if role:
                            user.role_id = role.id
                    except ValueError:
                        pass  # Keep existing role if invalid
                
                # Build an atomic update dict to avoid identity-map / flush issues
                update_dict = {}

                # Handle password changes
                if 'password' in user_data and user_data['password']:
                    password = user_data['password']
                    min_length = self.settings_service.get_min_password_length()
                    if len(password) < min_length:
                        return {
                            "success": False,
                            "message": f"Password must be at least {min_length} characters long"
                        }

                    try:
                        if self.auth_service:
                            hashed = self.auth_service.hash_password(password)
                        else:
                            hashed = self.hash_password(password)
                    except Exception:
                        hashed = self.hash_password(password)

                    update_dict['password_hash'] = hashed
                    update_dict['password_changed_at'] = datetime.utcnow()

                # Update other simple fields if present
                updateable_fields = ['name', 'email', 'department', 'position', 'is_active']
                for field in updateable_fields:
                    if field in user_data:
                        update_dict[field] = user_data[field]

                # role handled earlier via role_id assignment; ensure it is included if changed
                if 'role' in user_data and 'role_id' in locals():
                    update_dict['role_id'] = user.role_id

                # Always set updated_at
                update_dict['updated_at'] = datetime.utcnow()

                # Perform atomic update on DB
                if update_dict:
                    session.query(User).filter(User.id == user_id).update(update_dict, synchronize_session=False)
                session.commit()
                # Debug: re-query in same session to confirm persistence
                try:
                    persisted = session.query(User).filter(User.id == user_id).first()
                    print(f"DEBUG: persisted hash after commit: {getattr(persisted, 'password_hash', None)[:32]}")
                except Exception:
                    pass
                # Re-query the user to ensure we have a persistent instance bound to this session
                user = session.query(User).filter(User.id == user_id).first()
                
                # Audit logging: convert to plain dicts while session is active
                new_values = self._user_to_dict(user, include_sensitive=False)
                result_user = self._user_to_dict(user)

                # Perform audit logging (uses its own DB session)
                self.audit_service.log_action(
                    action="USER_UPDATED",
                    description=f"Updated user: {result_user.get('name')} ({result_user.get('email')})",
                    table_name="users",
                    record_id=str(result_user.get('id')),
                    old_values=old_values,
                    new_values=new_values
                )

                return {
                    "success": True,
                    "message": "User updated successfully",
                    "user": result_user
                }
                
        except Exception as e:
            import traceback, sys
            tb = traceback.format_exc()
            print("Error in update_user:", repr(e), file=sys.stderr)
            print(tb, file=sys.stderr)
            return {
                "success": False,
                "message": f"Error updating user: {str(e)}"
            }
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete a user with validation and audit logging"""
        try:
            with get_db() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return {"success": False, "message": "User not found"}
                
                # Don't allow deletion of the current user
                if user_id == self._current_user_id:
                    return {
                        "success": False,
                        "message": "Cannot delete your own account"
                    }
                
                # Check if user has assigned assets
                from ..core.models import Asset
                asset_count = session.query(func.count(Asset.id)).filter(Asset.assigned_to_id == user_id).scalar()

                if asset_count and asset_count > 0:
                    return {
                        "success": False,
                        "message": f"Cannot delete user with {asset_count} assigned assets"
                    }

                # Store user data for audit
                user_data = self._user_to_dict(user, include_sensitive=False)

                # Invalidate all user sessions (use consistent 'Active'/'Expired' values)
                session.query(UserSession).filter(
                    UserSession.user_id == user_id,
                    UserSession.is_active == "Active"
                ).update({
                    "is_active": "Expired",
                    "logout_time": datetime.utcnow()
                }, synchronize_session=False)
                # Soft-delete: mark user as inactive and set deleted_at timestamp
                deleted_at = datetime.utcnow()
                user.deleted_at = deleted_at
                user.is_active = 'Inactive'

                # Invalidate all user sessions (mark as expired)
                session.query(UserSession).filter(
                    UserSession.user_id == user_id,
                    UserSession.is_active == "Active"
                ).update({
                    "is_active": "Expired",
                    "logout_time": datetime.utcnow()
                }, synchronize_session=False)

                # Commit the soft-delete
                session.commit()

                # Audit logging: record the deletion action (best-effort)
                try:
                    self.audit_service.log_action(
                        action="USER_DELETED",
                        description=f"Soft-deleted user: {user_data['name']} ({user_data['email']})",
                        table_name="users",
                        record_id=str(user_id),
                        old_values=user_data,
                        new_values={"deleted_at": deleted_at.isoformat()}
                    )
                except Exception:
                    pass

                return {
                    "success": True,
                    "message": "User deactivated successfully",
                    "deleted_at": deleted_at.isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting user: {str(e)}"
            }

    def restore_user(self, user_id: int) -> Dict[str, Any]:
        """Restore a soft-deleted user by clearing deleted_at and setting is_active to 'Active'."""
        try:
            with get_db() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return {"success": False, "message": "User not found"}

                if getattr(user, 'deleted_at', None) is None:
                    return {"success": False, "message": "User is not deleted"}

                old_values = self._user_to_dict(user, include_sensitive=False)
                user.deleted_at = None
                user.is_active = 'Active'
                user.updated_at = datetime.utcnow()
                session.commit()

                new_values = self._user_to_dict(user, include_sensitive=False)
                self.audit_service.log_action(
                    action="USER_RESTORED",
                    description=f"Restored user: {new_values.get('name')} ({new_values.get('email')})",
                    table_name="users",
                    record_id=str(user_id),
                    old_values=old_values,
                    new_values=new_values
                )

                return {"success": True, "message": "User restored"}
        except Exception as e:
            return {"success": False, "message": f"Error restoring user: {str(e)}"}

    def permanently_delete_user(self, user_id: int) -> Dict[str, Any]:
        """Permanently remove a user from the database. Use with care.

        This bypasses soft-delete and deletes the user row and related
        sessions. It writes an audit entry noting the permanent removal.
        """
        try:
            with get_db() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return {"success": False, "message": "User not found"}

                # Prevent deleting the current user
                if user_id == self._current_user_id:
                    return {"success": False, "message": "Cannot delete your own account"}

                # Ensure no assigned assets remain (safety check)
                from ..core.models import Asset
                asset_count = session.query(func.count(Asset.id)).filter(Asset.assigned_to_id == user_id).scalar()
                if asset_count and asset_count > 0:
                    return {"success": False, "message": f"Cannot permanently delete user with {asset_count} assigned assets"}

                # Capture old values for audit
                old_values = self._user_to_dict(user, include_sensitive=False)

                # Remove sessions
                session.query(UserSession).filter(UserSession.user_id == user_id).delete(synchronize_session=False)

                # Finally delete the user row
                session.delete(user)
                session.commit()

                # Audit logging
                try:
                    self.audit_service.log_action(
                        action="USER_PERMANENTLY_DELETED",
                        description=f"Permanently deleted user: {old_values.get('name')} ({old_values.get('email')})",
                        table_name="users",
                        record_id=str(user_id),
                        old_values=old_values
                    )
                except Exception:
                    pass

                return {"success": True, "message": "User permanently deleted"}

        except Exception as e:
            return {"success": False, "message": f"Error permanently deleting user: {str(e)}"}
    
    def reset_password(self, user_id: int, new_password: str) -> Dict[str, Any]:
        """Reset user password (admin function)"""
        try:
            # Validate password strength
            min_length = self.settings_service.get_min_password_length()
            if len(new_password) < min_length:
                return {
                    "success": False,
                    "message": f"Password must be at least {min_length} characters long"
                }
            
            # Use auth service for password reset
            result = self.auth_service.reset_password(
                user_id=user_id,
                new_password=new_password,
                reset_by_user_id=self._current_user_id
            )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error resetting password: {str(e)}"
            }
    
    def update_user_permissions(self, user_id: int, role_name: str, 
                              custom_permissions: List[str] = None) -> Dict[str, Any]:
        """Update user role and permissions"""
        try:
            with get_db() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return {"success": False, "message": "User not found"}
                
                # Update role
                try:
                    user_role = UserRole(role_name)
                    role = session.query(Role).filter(Role.name == user_role).first()
                    if not role:
                        return {"success": False, "message": "Invalid role"}
                    
                    old_role_id = user.role_id
                    user.role_id = role.id
                    user.updated_at = datetime.utcnow()
                    
                    session.commit()
                    
                    # Audit logging
                    self.audit_service.log_action(
                        action="USER_ROLE_CHANGED",
                        description=f"Changed role for user {user.name} to {role_name}",
                        table_name="users",
                        record_id=str(user.id),
                        old_values={"role_id": old_role_id},
                        new_values={"role_id": role.id}
                    )
                    
                    return {
                        "success": True,
                        "message": "User permissions updated successfully"
                    }
                    
                except ValueError:
                    return {"success": False, "message": "Invalid role"}
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating permissions: {str(e)}"
            }
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            with get_db() as session:
                total_users = session.query(User).count()
                active_users = session.query(User).filter(User.is_active == "Active").count()
                inactive_users = session.query(User).filter(User.is_active == "Inactive").count()
                suspended_users = session.query(User).filter(User.is_active == "Suspended").count()
                
                # Count by role
                role_counts = {}
                for role in UserRole:
                    count = session.query(User).join(Role).filter(
                        Role.name == role
                    ).count()
                    role_counts[role.value] = count
                
                # Recent login activity (last 30 days)
                recent_date = datetime.utcnow() - timedelta(days=30)
                recent_logins = session.query(User).filter(
                    User.last_login >= recent_date
                ).count()
                
                return {
                    "total_users": total_users,
                    "active_users": active_users,
                    "inactive_users": inactive_users,
                    "suspended_users": suspended_users,
                    "role_counts": role_counts,
                    "recent_logins": recent_logins
                }
                
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return {}
    
    def _initialize_default_roles(self, session: Session):
        """Initialize default roles and permissions if they don't exist"""
        try:
            # Create default roles
            default_roles = [
                (UserRole.ADMIN, "System administrator with full access"),
                (UserRole.USER, "Regular user with limited permissions"),
                (UserRole.VIEWER, "View-only access to system")
            ]
            
            for role_enum, description in default_roles:
                existing_role = session.query(Role).filter(Role.name == role_enum).first()
                if not existing_role:
                    role = Role(name=role_enum, description=description)
                    session.add(role)
            
            # Create default permissions
            for perm_enum in PermissionType:
                existing_perm = session.query(Permission).filter(
                    Permission.name == perm_enum
                ).first()
                if not existing_perm:
                    permission = Permission(
                        name=perm_enum,
                        description=f"Permission to {perm_enum.value.lower()}"
                    )
                    session.add(permission)
            
            session.flush()  # Flush to get IDs
            
            # Set up default role-permission mappings
            admin_role = session.query(Role).filter(Role.name == UserRole.ADMIN).first()
            user_role = session.query(Role).filter(Role.name == UserRole.USER).first()
            viewer_role = session.query(Role).filter(Role.name == UserRole.VIEWER).first()
            
            # Admin gets all permissions
            if admin_role:
                for perm_enum in PermissionType:
                    permission = session.query(Permission).filter(
                        Permission.name == perm_enum
                    ).first()
                    if permission:
                        existing_rp = session.query(RolePermission).filter(
                            RolePermission.role_id == admin_role.id,
                            RolePermission.permission_id == permission.id
                        ).first()
                        if not existing_rp:
                            role_perm = RolePermission(
                                role_id=admin_role.id,
                                permission_id=permission.id,
                                granted="true"
                            )
                            session.add(role_perm)
            
            # User gets limited permissions
            if user_role:
                user_permissions = [
                    PermissionType.VIEW_ASSET,
                    PermissionType.CREATE_ASSET,
                    PermissionType.EDIT_ASSET,
                    PermissionType.VIEW_REPORTS
                ]
                for perm_enum in user_permissions:
                    permission = session.query(Permission).filter(
                        Permission.name == perm_enum
                    ).first()
                    if permission:
                        existing_rp = session.query(RolePermission).filter(
                            RolePermission.role_id == user_role.id,
                            RolePermission.permission_id == permission.id
                        ).first()
                        if not existing_rp:
                            role_perm = RolePermission(
                                role_id=user_role.id,
                                permission_id=permission.id,
                                granted="true"
                            )
                            session.add(role_perm)
            
            # Viewer gets view-only permissions
            if viewer_role:
                viewer_permissions = [
                    PermissionType.VIEW_ASSET,
                    PermissionType.VIEW_REPORTS
                ]
                for perm_enum in viewer_permissions:
                    permission = session.query(Permission).filter(
                        Permission.name == perm_enum
                    ).first()
                    if permission:
                        existing_rp = session.query(RolePermission).filter(
                            RolePermission.role_id == viewer_role.id,
                            RolePermission.permission_id == permission.id
                        ).first()
                        if not existing_rp:
                            role_perm = RolePermission(
                                role_id=viewer_role.id,
                                permission_id=permission.id,
                                granted="true"
                            )
                            session.add(role_perm)
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            print(f"Error initializing default roles: {e}")
    
    def _user_to_dict(self, user: User, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert user object to dictionary"""
        if not user:
            return {}
            
        result = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'department': user.department,
            'position': user.position,
            'role': user.role.name.value if user.role else 'Unknown',
            'role_id': user.role_id,
            'is_active': user.is_active,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            'deleted_at': user.deleted_at.isoformat() if getattr(user, 'deleted_at', None) else None
        }
        
        if include_sensitive:
            result['password_changed_at'] = user.password_changed_at.isoformat() if user.password_changed_at else None
        
        return result
