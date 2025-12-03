import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import Config
from app.core.database import init_db, get_db
from app.core.models import User, Role, UserRole
from app.services.auth_service import AuthService

def initialize_roles(session):
    """Initializes default roles in the database."""
    roles = {
        UserRole.ADMIN: "Full system access",
        UserRole.USER: "Standard user access",
        UserRole.VIEWER: "Read-only access"
    }
    for role_enum, description in roles.items():
        if not session.query(Role).filter_by(name=role_enum).first():
            session.add(Role(name=role_enum, description=description))
    session.commit()

def create_admin_user(session):
    """Creates the default admin user if one doesn't exist."""
    if session.query(User).filter_by(email="admin@company.com").first():
        print("Admin user already exists.")
        return

    admin_role = session.query(Role).filter_by(name=UserRole.ADMIN).first()
    if not admin_role:
        print("Admin role not found. Please run initialize_roles first.")
        return
        
    admin_user = User(
        email="admin@company.com",
        name="System Administrator",
        role_id=admin_role.id
    )
    admin_user.set_password("admin123")  # Set a default password
    session.add(admin_user)
    session.commit()
    print("Admin user created successfully.")

def main():
    """Initialize the database and create default data"""
    try:
        # Get config
        config = Config()
        
        print("Initializing database...")
        # Initialize database
        init_db(config.DATABASE_URL)
        
        with get_db() as session:
            print("Creating default roles...")
            initialize_roles(session)
            
            print("Creating default admin user...")
            create_admin_user(session)
            
            print("Database initialization completed successfully!")
            return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)