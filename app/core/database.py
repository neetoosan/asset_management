from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from contextlib import contextmanager

Base = declarative_base()
_Session = None


def init_db(database_url):
    """Initialize the database with the given URL"""
    global _Session
    engine = create_engine(database_url, echo=False)
    _Session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    
    # Initialize default data
    _init_default_roles_and_permissions()


def get_db_session():
    """Get a database session"""
    if _Session is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _Session()


@contextmanager
def get_db():
    """Context manager for database sessions"""
    session = get_db_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _init_default_roles_and_permissions():
    """Initialize default roles and permissions if they don't exist"""
    from .models import Role, Permission, RolePermission, UserRole, PermissionType
    
    session = get_db_session()
    try:
        # Check if roles already exist
        if session.query(Role).count() > 0:
            return
        
        # Create all permissions first
        permissions = {}
        for perm_type in PermissionType:
            permission = Permission(
                name=perm_type,
                description=f"Permission to {perm_type.value.lower()}"
            )
            session.add(permission)
            session.flush()  # Get the ID
            permissions[perm_type] = permission
        
        # Create roles
        roles_data = {
            UserRole.ADMIN: list(PermissionType),  # Admin gets all permissions
            UserRole.USER: [
                PermissionType.VIEW_ASSET,
                PermissionType.CREATE_ASSET,
                PermissionType.EDIT_ASSET
            ],
            UserRole.VIEWER: [
                PermissionType.VIEW_ASSET,
                PermissionType.VIEW_REPORTS
            ]
        }
        
        for user_role, role_permissions in roles_data.items():
            # Create role
            role = Role(
                name=user_role,
                description=f"Role for {user_role.value} users"
            )
            session.add(role)
            session.flush()  # Get the ID
            
            # Assign permissions to role
            for perm_type in role_permissions:
                role_permission = RolePermission(
                    role_id=role.id,
                    permission_id=permissions[perm_type].id,
                    granted="true"
                )
                session.add(role_permission)
        
        session.commit()
        print("Default roles and permissions initialized successfully")
    except Exception as e:
        session.rollback()
        print(f"Error initializing roles and permissions: {e}")
    finally:
        session.close()


