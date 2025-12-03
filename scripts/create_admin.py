#!/usr/bin/env python3
"""
Simple script to create admin user for login
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import init_db
from app.core.config import Config
from app.core.models import User, Role, UserRole
from app.services.auth_service import AuthService
from app.core.models import Permission, RolePermission, PermissionType


def create_admin_user():
    """Create admin user for login"""
    print("🔧 Creating admin user...")
    
    config = Config()
    
    # Reinitialize database to ensure all tables exist
    init_db(config.DATABASE_URL)
    
    auth_service = AuthService()
    
    try:
        from app.core.database import get_db
        
        with get_db() as session:
            # Create admin role if it doesn't exist
            admin_role = session.query(Role).filter(Role.name == UserRole.ADMIN).first()
            if not admin_role:
                admin_role = Role(
                    name=UserRole.ADMIN,
                    description="System administrator with full access"
                )
                session.add(admin_role)
                session.flush()
                print("✅ Created admin role")
            
            # Check if admin user already exists
            existing_admin = session.query(User).filter(User.email == "admin@company.com").first()
            
            if existing_admin:
                # Update existing admin user
                print("🔄 Updating existing admin user...")
                existing_admin.password_hash = auth_service.hash_password("admin123")
                existing_admin.name = "System Administrator"
                existing_admin.department = "IT"
                existing_admin.position = "System Administrator"
                existing_admin.role_id = admin_role.id
                existing_admin.is_active = "Active"
                print("✅ Updated admin user credentials")
            else:
                # Create new admin user
                print("➕ Creating new admin user...")
                password_hash = auth_service.hash_password("admin123")
                
                admin_user = User(
                    name="System Administrator",
                    email="admin@company.com",
                    password_hash=password_hash,
                    department="IT",
                    position="System Administrator",
                    role_id=admin_role.id,
                    is_active="Active"
                )
                
                session.add(admin_user)
                print("✅ Created new admin user")
            
            session.commit()
            # Ensure all permissions exist and are granted to the admin role
            for perm_type in PermissionType:
                perm = session.query(Permission).filter_by(name=perm_type).first()
                if not perm:
                    perm = Permission(name=perm_type)
                    session.add(perm)
                    session.flush()

                # Ensure RolePermission exists and is granted
                rp = session.query(RolePermission).filter_by(role_id=admin_role.id, permission_id=perm.id).first()
                if not rp:
                    rp = RolePermission(role_id=admin_role.id, permission_id=perm.id, granted="true")
                    session.add(rp)
                else:
                    if getattr(rp, 'granted', None) != "true":
                        rp.granted = "true"
                        session.add(rp)
            session.commit()
            
            print("\n" + "="*50)
            print("🎉 ADMIN USER READY!")
            print("="*50)
            print("📧 Email: admin@company.com")
            print("🔑 Password: admin123")
            print("⚠️  Please change password after first login!")
            print("\n🚀 You can now login to the application")
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    create_admin_user()
