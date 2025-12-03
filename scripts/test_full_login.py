#!/usr/bin/env python3
"""
Test script to verify complete login functionality including GUI integration
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.auth_service import AuthService
from app.core.database import get_db, init_db
from app.core.config import Config
from app.core.models import User
from app.gui.views.login_screen import LoginScreen
from PySide6.QtWidgets import QApplication


def test_auth_service():
    """Test the AuthService directly"""
    print("🔍 Testing AuthService...")
    
    # Initialize database
    config = Config()
    init_db(config.DATABASE_URL)
    
    auth_service = AuthService()
    
    # Test credentials
    email = "admin@company.com"
    password = "admin123"
    
    print(f"📧 Testing email: {email}")
    print(f"🔑 Testing password: {password}")
    
    # Test login
    result = auth_service.login(email, password)
    
    if result['success']:
        print(f"✅ Login successful!")
        print(f"   User: {result['user']['name']}")
        print(f"   Role: {result['user']['role']}")
        print(f"   Session token: {result['session_token'][:20]}...")
        
        # Test session validation
        print(f"\n🔍 Testing session validation...")
        session_info = auth_service.validate_session(result['session_token'])
        if session_info:
            print(f"✅ Session validation successful!")
            print(f"   User: {session_info['name']}")
            print(f"   Role: {session_info['role']}")
        else:
            print(f"❌ Session validation failed!")
        
        # Test logout
        print(f"\n🚪 Testing logout...")
        logout_result = auth_service.logout(result['session_token'])
        if logout_result['success']:
            print(f"✅ Logout successful!")
        else:
            print(f"❌ Logout failed: {logout_result['message']}")
            
    else:
        print(f"❌ Login failed: {result['message']}")
    
    return result['success']


def test_login_screen():
    """Test the login screen GUI component"""
    print(f"\n🖥️ Testing LoginScreen GUI component...")
    
    # Initialize QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Create login screen
        login_screen = LoginScreen()
        
        # Set test credentials programmatically
        login_screen.ui.email_input.setText("admin@company.com")
        login_screen.ui.password_input.setText("admin123")
        
        print(f"✅ LoginScreen created successfully!")
        print(f"   Email field: {login_screen.ui.email_input.text()}")
        print(f"   Password field: {'*' * len(login_screen.ui.password_input.text())}")
        
        # Test the login handler
        print(f"🔍 Testing login handler...")
        result = login_screen.handle_login()
        
        if result:
            print(f"✅ Login screen authentication successful!")
        else:
            print(f"❌ Login screen authentication failed!")
        
        return result
        
    except Exception as e:
        print(f"❌ Error testing login dialog: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("🧪 Running complete login functionality tests...\n")
    
    # Test 1: AuthService
    auth_success = test_auth_service()
    
    # Test 2: Login Screen GUI (if available)
    gui_success = test_login_screen()
    
    print(f"\n📊 Test Results:")
    print(f"   AuthService: {'✅ PASS' if auth_success else '❌ FAIL'}")
    print(f"   GUI Dialog:  {'✅ PASS' if gui_success else '❌ FAIL'}")
    
    if auth_success and gui_success:
        print(f"\n🎉 All tests passed! Login functionality is working correctly.")
        return True
    else:
        print(f"\n⚠️ Some tests failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
