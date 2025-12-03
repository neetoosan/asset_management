#!/usr/bin/env python3
"""
Test script to debug login authentication
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.auth_service import AuthService
from app.core.database import get_db, init_db
from app.core.config import Config
from app.core.models import User


def test_login():
    """Test login functionality"""
    print("🔍 Testing login functionality...")
    
    # Initialize database
    config = Config()
    init_db(config.DATABASE_URL)
    
    auth_service = AuthService()
    
    # Test credentials
    email = "admin@company.com"
    password = "admin123"
    
    print(f"📧 Testing email: {email}")
    print(f"🔑 Testing password: {password}")
    
    # First, let's check if the user exists in the database
    try:
        with get_db() as session:
            user = session.query(User).filter(User.email == email).first()
            
            if user:
                print(f"✅ User found in database:")
                print(f"   ID: {user.id}")
                print(f"   Name: {user.name}")
                print(f"   Email: {user.email}")
                print(f"   Active: {user.is_active}")
                print(f"   Role ID: {user.role_id}")
                print(f"   Password hash: {user.password_hash[:50]}...")
                
                # Test password verification directly
                print(f"\n🔐 Testing password verification...")
                password_valid = auth_service.verify_password(password, user.password_hash)
                print(f"   Password valid: {password_valid}")
                
                # Test the full login process with direct session access
                print(f"\n🚪 Testing full login process...")
                print(f"\n🔍 Checking user role with fresh session...")
                
                # Test accessing role with a fresh session
                fresh_user = session.query(User).filter(User.email == email).first()
                if fresh_user.role:
                    print(f"   Role ID: {fresh_user.role_id}")
                    print(f"   Role object: {fresh_user.role}")
                    try:
                        print(f"   Role name: {fresh_user.role.name}")
                        if hasattr(fresh_user.role.name, 'value'):
                            print(f"   Role name value: {fresh_user.role.name.value}")
                        else:
                            print(f"   Role name is direct: {fresh_user.role.name}")
                    except Exception as role_e:
                        print(f"   ❌ Error accessing role name: {role_e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print(f"   ❌ User has no role assigned")
                
                # Now test the login method
                print(f"\n🚪 Testing AuthService.login...")
                try:
                    result = auth_service.login(email, password)
                    print(f"   Login result: {result}")
                    
                    if result['success']:
                        print(f"   ✅ Login successful!")
                        print(f"   User: {result['user']['name']}")
                        print(f"   Role: {result['user']['role']}")
                        print(f"   Session token: {result['session_token'][:20]}...")
                    else:
                        print(f"   ❌ Login failed: {result['message']}")
                        
                except Exception as e:
                    print(f"   ❌ Exception during login: {e}")
                    import traceback
                    traceback.print_exc()
                
            else:
                print(f"❌ User not found in database")
                
                # Let's see what users exist
                all_users = session.query(User).all()
                print(f"📋 Users in database ({len(all_users)}):")
                for u in all_users:
                    print(f"   - {u.name} ({u.email})")
                
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_login()
