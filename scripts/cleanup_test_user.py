import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.core.models import User, AuditLog, UserSession
from app.core.database import init_db
from app.core.config import Config

email = 'testuser@example.com'

# Ensure DB is initialized (creates tables / default data if missing)
cfg = Config()
init_db(cfg.DATABASE_URL)

with get_db() as session:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        print(f'No user with email {email} found; nothing to delete.')
    else:
        print(f'Found user id={user.id}, deleting audit logs and user...')
        deleted_a = session.query(AuditLog).filter(AuditLog.user_id == user.id).delete(synchronize_session=False)
        deleted_s = session.query(UserSession).filter(UserSession.user_id == user.id).delete(synchronize_session=False)
        deleted_u = session.query(User).filter(User.id == user.id).delete(synchronize_session=False)
        session.commit()
        print(f'Deleted {deleted_a} audit log(s), {deleted_s} user session(s) and {deleted_u} user(s)')
