import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import Config
from app.core.database import init_db, get_db
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.models import User

cfg = Config()
init_db(cfg.DATABASE_URL)

us = UserService()
auth = AuthService()

email = 'debuguser@example.com'
import time
email = f"debuguser_{int(time.time())}@example.com"
old = 'OldPass123'
new = 'NewPass456'

print('Cleaning existing debug user if present')
with get_db() as session:
    session.query(User).filter(User.email == email).delete(synchronize_session=False)

print('Creating user...')
res = us.create_user({'name':'Debug User','email':email,'password':old,'role':'User','department':'IT','position':'Dev','is_active':'Active'})
print('create res:', res)

with get_db() as session:
    u = session.query(User).filter(User.email==email).first()
    print('Stored hash after create:', getattr(u,'password_hash',None))
    print('verify_password(old):', auth.verify_password(old, u.password_hash))
    print('verify_password(new):', auth.verify_password(new, u.password_hash))

print('AuthService.login with old')
print(auth.login(email, old))
print('AuthService.login with new')
print(auth.login(email, new))

print('Updating password via UserService.update_user...')
update_res = us.update_user(res['user']['id'], {'password': new})
print('update res:', update_res)

with get_db() as session:
    u2 = session.query(User).filter(User.email==email).first()
    print('Stored hash after update:', getattr(u2,'password_hash',None))
    print('verify_password(old):', auth.verify_password(old, u2.password_hash))
    print('verify_password(new):', auth.verify_password(new, u2.password_hash))

print('AuthService.login with old after update')
print(auth.login(email, old))
print('AuthService.login with new after update')
print(auth.login(email, new))

print('Cleaning up')
with get_db() as session:
    # Remove audit log references first to avoid FK constraint
    from app.core.models import AuditLog
    session.query(AuditLog).filter(AuditLog.user_id == None).delete(synchronize_session=False)
    session.query(User).filter(User.email == email).delete(synchronize_session=False)
print('done')
