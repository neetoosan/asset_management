#!/usr/bin/env python3
"""
Test script to verify user session creation and management
"""

import sys
import os
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.auth_service import AuthService
from app.core.database import get_db, init_db
from app.core.config import Config
from app.core.models import User, UserSession

def test_session():
    """Test user session management"""
    print("\n🔍 Testing user session management...")
    
    # Initialize database connection
    config = Config()
    init_db(config.DATABASE_URL)
    
    # Create auth service instance
    auth_service = AuthService()
    
    # Test user credentials
    email = "admin@company.com"
    password = "admin123"
    
    # Try to login and create session
    print(f"\n📧 Testing login for user: {email}")
    result = auth_service.login(
        email=email,
        password=password
    )
    
    print("\n🔑 Login result:")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    if result['success']:
        print("\n🎫 Session details:")
        with get_db() as session:
            if result['user']['is_default_admin']:
                print("Admin session details (in-memory):")
                print(f"User: {result['user']['name']}")
                print(f"Session token: {result['session_token'][:20]}...")
            else:
                user_session = session.query(UserSession).filter(
                    UserSession.session_token == result['session_token']
                ).first()
                
                if user_session:
                    print("Database session details:")
                    print(f"Session ID: {user_session.id}")
                    print(f"User ID: {user_session.user_id}")
                    print(f"Login time: {user_session.login_time}")
                    print(f"Session token: {user_session.session_token[:20]}...")
                else:
                    print("❌ No session found in database!")
    else:
        print("\n❌ Failed to create session!")

if __name__ == "__main__":
    test_session()