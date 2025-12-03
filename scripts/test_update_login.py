import sys
import os
# Ensure project root is on sys.path so 'app' imports work when running the script directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.database import get_db
from app.core.models import User
from app.core.config import Config
from app.core.database import init_db


def run_test():
    us = UserService()
    auth = AuthService()
    # Initialize database (creates tables and default roles/permissions)
    cfg = Config()
    init_db(cfg.DATABASE_URL)
    email = 'testuser@example.com'
    plain1 = 'TestPass123'
    plain2 = 'NewPass123'

    # Clean up existing test user if present
    # Ensure no existing user remains (force delete via direct DB session)
    try:
        with get_db() as session:
            session.query(User).filter(User.email == email).delete(synchronize_session=False)
    except Exception:
        pass

    # Create user
    print('Creating user...')
    create_res = us.create_user({
        'name': 'Test User',
        'email': email,
        'password': plain1,
        'role': 'User',
        'department': 'IT',
        'position': 'Engineer',
        'is_active': 'Active'
    })
    print('Create result:', create_res)
    if not create_res.get('success'):
        print('Create failed, aborting test')
        return

    user = create_res.get('user')
    user_id = user.get('id')

    # Try login with original password
    print('\nAttempt login with original password...')
    res1 = auth.login(email, plain1)
    print('Login result (original):', res1)
    # Inspect stored hash directly
    with get_db() as session:
        db_user = session.query(User).filter(User.email == email).first()
        print('Stored hash after create:', db_user.password_hash)
        print('verify_password(original):', auth.verify_password(plain1, db_user.password_hash))
        print('verify_password(new):', auth.verify_password(plain2, db_user.password_hash))

    # Update user's password
    print('\nUpdating user password...')
    update_res = us.update_user(user_id, {'password': plain2})
    print('Update result:', update_res)
    # Inspect stored hash after update
    with get_db() as session:
        db_user = session.query(User).filter(User.email == email).first()
        print('Stored hash after update:', db_user.password_hash)
        print('verify_password(original) after update:', auth.verify_password(plain1, db_user.password_hash))
        print('verify_password(new) after update:', auth.verify_password(plain2, db_user.password_hash))

    # Try login with old password (should fail)
    print('\nAttempt login with old password (should fail)...')
    res_old = auth.login(email, plain1)
    print('Login result (old):', res_old)

    # Try login with new password (should succeed)
    print('\nAttempt login with new password (should succeed)...')
    res_new = auth.login(email, plain2)
    print('Login result (new):', res_new)

    # Clean up test user
    print('\nCleaning up test user...')
    us.delete_user(user_id)
    print('Done')


if __name__ == '__main__':
    run_test()
