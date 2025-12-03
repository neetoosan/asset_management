from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..core.database import get_db
from ..core.models import Role, Permission, RolePermission, UserRole, PermissionType, User, UserSession


class RoleService:
    def __init__(self):
        pass
        
    def get_all_roles(self) -> List[Dict]:
        """Get all roles with their permissions"""
        with get_db() as session:
            roles = session.query(Role).all()
            return [self._role_to_dict(role) for role in roles]
            
    def validate_session_permission(self, session_token: str, permission: str) -> bool:
        """Validate if a session has a specific permission"""
        with get_db() as session:
            try:
                # Get user session
                user_session = session.query(UserSession).filter(
                    UserSession.session_token == session_token,
                    UserSession.is_active == "Active"
                ).first()
                
                if not user_session:
                    return False
                    
                # Get user and role
                user = session.query(User).get(user_session.user_id)
                if not user or not user.role:
                    return False
                    
                # Check permission
                perm_type = PermissionType(permission)
                role_perms = session.query(RolePermission).join(
                    Permission
                ).filter(
                    RolePermission.role_id == user.role_id,
                    Permission.name == perm_type
                ).first()
                
                return role_perms is not None
            except (ValueError, Exception):
                return False
    
    def get_role_permissions(self, role_id: int) -> List[str]:
        """Get permissions for a specific role"""
        with get_db() as session:
            role = session.query(Role).filter(Role.id == role_id).first()
            if not role:
                return []
            return [perm.permission.name.value for perm in role.permissions]
    
    def update_role_permissions(self, role_id: int, permissions: List[str]) -> bool:
        """Update permissions for a role"""
        with get_db() as session:
            try:
                # Get role
                role = session.query(Role).filter(Role.id == role_id).first()
                if not role:
                    return False
                    
                # Clear existing permissions
                session.query(RolePermission).filter(
                    RolePermission.role_id == role_id
                ).delete()
                
                # Add new permissions
                for perm_name in permissions:
                    try:
                        perm_type = PermissionType(perm_name)
                        # Get or create permission
                        permission = session.query(Permission).filter(
                            Permission.name == perm_type
                        ).first()
                        if not permission:
                            permission = Permission(name=perm_type)
                            session.add(permission)
                            session.flush()
                        
                        # Create role permission
                        role_perm = RolePermission(
                            role_id=role.id,
                            permission_id=permission.id
                        )
                        session.add(role_perm)
                    except ValueError:
                        # Invalid permission name
                        continue
                
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False
    
    def check_permission(self, user_id: int, permission: str) -> bool:
        """Check if a user has a specific permission"""
        # Handle default admin user (ID 0) - has all permissions
        if user_id == 0:
            return True
            
        with get_db() as session:
            try:
                perm_type = PermissionType(permission)
                user = session.query(User).filter(User.id == user_id).first()
                if not user or not user.role:
                    return False
                
                # Admin role has all permissions
                if user.role.name == UserRole.ADMIN:
                    return True
                
                # Check if user's role has the permission
                role_perms = session.query(RolePermission).join(
                    Permission
                ).filter(
                    RolePermission.role_id == user.role_id,
                    Permission.name == perm_type,
                    RolePermission.granted == "true"
                ).first()
                
                return role_perms is not None
            except (ValueError, Exception) as e:
                print(f"Permission check error: {e}")
                return False
    
    def update_user_role(self, user_id: int, role_id: int) -> bool:
        """Update a user's role"""
        with get_db() as session:
            try:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return False
                    
                role = session.query(Role).filter(Role.id == role_id).first()
                if not role:
                    return False
                
                user.role_id = role.id
                user.updated_at = datetime.utcnow()
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False
    
    @staticmethod
    def _role_to_dict(role: Role) -> Dict:
        """Convert a role object to dictionary"""
        return {
            "id": role.id,
            "name": role.name.value if isinstance(role.name, UserRole) else str(role.name),
            "description": role.description,
            "permissions": [p.permission.name.value for p in role.permissions] if role.permissions else []
        }