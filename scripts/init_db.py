import sys
from pathlib import Path
# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from app.core.config import Config
from app.core.database import init_db, get_db
from app.core.models import Role, Permission, RolePermission, UserRole, PermissionType
from app.services.user_service import UserService
from app.services.role_service import RoleService

def initialize_database():
    """Initialize database with default roles and permissions"""
    config = Config()
    
    # Initialize database connection
    init_db(config.DATABASE_URL)
        
    with get_db() as session:
        # Create default roles if they don't exist
        admin_role = session.query(Role).filter_by(name=UserRole.ADMIN).first()
        if not admin_role:
            admin_role = Role(name=UserRole.ADMIN, description="Administrator with full access")
            session.add(admin_role)
            session.flush()
        
        # Create all permissions
        for perm_type in PermissionType:
            perm = session.query(Permission).filter_by(name=perm_type).first()
            if not perm:
                perm = Permission(name=perm_type)
                session.add(perm)
                session.flush()
                
                # Grant permission to admin role
                role_perm = RolePermission(
                    role_id=admin_role.id,
                    permission_id=perm.id,
                    granted="true"
                )
                session.add(role_perm)
        
        session.commit()
        print("Database initialized successfully with default roles and permissions")

if __name__ == "__main__":
    initialize_database()