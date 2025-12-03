import sys
from pathlib import Path
# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.role_service import RoleService
from app.core.models import UserRole, PermissionType

def test_get_all_roles():
    role_service = RoleService()
    roles = role_service.get_all_roles()
    print("All roles:", roles)

def test_role_permissions():
    role_service = RoleService()
    # Get first role's ID
    roles = role_service.get_all_roles()
    if roles:
        role_id = roles[0]["id"]
        permissions = role_service.get_role_permissions(role_id)
        print(f"Permissions for role {roles[0]['name']}:", permissions)

if __name__ == "__main__":
    test_get_all_roles()
    test_role_permissions()