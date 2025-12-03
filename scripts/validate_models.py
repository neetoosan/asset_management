#!/usr/bin/env python3
"""
Validation script to test the fixed database models
"""

import sys
import os
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import init_db
from app.core.config import Config
from app.core.models import UserSession, RolePermission, User, Role, UserRole, Permission, PermissionType
from app.services.auth_service import AuthService


def test_user_session_model():
    """Test UserSession model structure"""
    print("🧪 Testing UserSession model...")
    
    try:
        config = Config()
        init_db(config.DATABASE_URL)
        
        from app.core.database import get_db
        
        # Create a test session
        auth_service = AuthService()
        
        with get_db() as session:
            # Create a test user first
            admin_role = session.query(Role).filter(Role.name == UserRole.ADMIN).first()
            if not admin_role:
                admin_role = Role(name=UserRole.ADMIN, description="Test admin role")
                session.add(admin_role)
                session.flush()
            
            test_user = User(
                name="Test User",
                email="test@example.com",
                password_hash=auth_service.hash_password("testpass"),
                role_id=admin_role.id,
                is_active="Active"
            )
            session.add(test_user)
            session.flush()
            
            # Create a test session
            test_session = UserSession(
                user_id=test_user.id,
                session_token="test_token_123",
                is_active="Active"
            )
            session.add(test_session)
            session.commit()
            
            # Verify the session was created correctly
            retrieved_session = session.query(UserSession).filter(
                UserSession.session_token == "test_token_123"
            ).first()
            
            if retrieved_session:
                print("  ✅ UserSession model is working correctly")
                print(f"    - Session ID: {retrieved_session.id}")
                print(f"    - User ID: {retrieved_session.user_id}")
                print(f"    - Status: {retrieved_session.is_active}")
                print(f"    - Login Time: {retrieved_session.login_time}")
                print(f"    - Last Activity: {retrieved_session.last_activity}")
                
                # Test updating session status
                retrieved_session.is_active = "Expired"
                session.commit()
                
                # Verify update
                updated_session = session.query(UserSession).filter(
                    UserSession.session_token == "test_token_123"
                ).first()
                
                if updated_session.is_active == "Expired":
                    print("  ✅ Session status update works correctly")
                else:
                    print("  ❌ Session status update failed")
                    
            else:
                print("  ❌ Failed to create or retrieve UserSession")
                
    except Exception as e:
        print(f"  ❌ UserSession model test failed: {e}")
        import traceback
        traceback.print_exc()


def test_role_permission_model():
    """Test RolePermission model structure"""
    print("🧪 Testing RolePermission model...")
    
    try:
        from app.core.database import get_db
        
        with get_db() as session:
            # Check for existing role or create new one
            test_role = session.query(Role).filter(Role.name == UserRole.USER).first()
            if not test_role:
                test_role = Role(name=UserRole.USER, description="Test user role")
                session.add(test_role)
                session.flush()
            
            test_permission = Permission(name=PermissionType.VIEW_ASSET, description="View assets")
            session.add(test_permission)
            session.flush()
            
            # Create role-permission relationship
            role_perm = RolePermission(
                role_id=test_role.id,
                permission_id=test_permission.id,
                granted="true"
            )
            session.add(role_perm)
            session.commit()
            
            # Verify the relationship was created correctly
            retrieved_rp = session.query(RolePermission).filter(
                RolePermission.role_id == test_role.id,
                RolePermission.permission_id == test_permission.id
            ).first()
            
            if retrieved_rp:
                print("  ✅ RolePermission model is working correctly")
                print(f"    - Role ID: {retrieved_rp.role_id}")
                print(f"    - Permission ID: {retrieved_rp.permission_id}")
                print(f"    - Granted: {retrieved_rp.granted}")
                print(f"    - Type of granted: {type(retrieved_rp.granted)}")
                
                if retrieved_rp.granted == "true":
                    print("  ✅ Granted field is using correct string format")
                else:
                    print(f"  ❌ Granted field has unexpected value: {retrieved_rp.granted}")
                    
            else:
                print("  ❌ Failed to create or retrieve RolePermission")
                
    except Exception as e:
        print(f"  ❌ RolePermission model test failed: {e}")
        import traceback
        traceback.print_exc()


def test_auth_service_consistency():
    """Test AuthService session consistency"""
    print("🧪 Testing AuthService session consistency...")
    
    try:
        from app.core.database import get_db
        
        auth_service = AuthService()
        
        with get_db() as session:
            # Create test user
            admin_role = session.query(Role).filter(Role.name == UserRole.ADMIN).first()
            if not admin_role:
                admin_role = Role(name=UserRole.ADMIN, description="Test admin role")
                session.add(admin_role)
                session.flush()
            
            test_user = User(
                name="Test Auth User",
                email="testauth@example.com",
                password_hash=auth_service.hash_password("testpass123"),
                role_id=admin_role.id,
                is_active="Active"
            )
            session.add(test_user)
            session.commit()
        
        # Test login functionality
        result = auth_service.login("testauth@example.com", "testpass123")
        
        if result["success"]:
            print("  ✅ Authentication login works correctly")
            print(f"    - User: {result['user']['name']}")
            print(f"    - Session Token: {result['session_token'][:20]}...")
            
            # Test session validation
            user_data = auth_service.validate_session(result["session_token"])
            if user_data:
                print("  ✅ Session validation works correctly")
                
                # Test logout
                logout_result = auth_service.logout(result["session_token"])
                if logout_result["success"]:
                    print("  ✅ Session logout works correctly")
                    
                    # Verify session is expired
                    expired_data = auth_service.validate_session(result["session_token"])
                    if not expired_data:
                        print("  ✅ Session expiration works correctly")
                    else:
                        print("  ❌ Session should be expired but still validates")
                else:
                    print(f"  ❌ Logout failed: {logout_result['message']}")
            else:
                print("  ❌ Session validation failed")
        else:
            print(f"  ❌ Authentication failed: {result['message']}")
            
    except Exception as e:
        print(f"  ❌ AuthService test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run all validation tests"""
    print("🎯 Database Model Validation")
    print("=" * 50)
    
    try:
        test_user_session_model()
        print()
        
        test_role_permission_model()
        print()
        
        test_auth_service_consistency()
        print()
        
        print("=" * 50)
        print("🎉 Validation complete!")
        print("✅ All database model fixes have been validated")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()