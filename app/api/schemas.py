from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    department: Optional[str] = None
    position: Optional[str] = None
    role_id: int
    is_active: str = "Active"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    last_login: Optional[datetime] = None
    role_name: Optional[str] = None
    permissions: List[str] = []

    class Config:
        orm_mode = True

# Asset schemas
class AssetBase(BaseModel):
    name: str
    asset_id: str
    description: str
    category_id: int
    subcategory_id: Optional[int] = None
    acquisition_date: datetime
    supplier: str
    quantity: int = 1
    unit_cost: float
    total_cost: float
    location: str
    custodian: Optional[str] = None
    department: Optional[str] = None
    assigned_to_id: Optional[int] = None
    status: str = "Available"
    asset_tag: Optional[str] = None
    serial_number: Optional[str] = None
    useful_life: Optional[int] = None
    depreciation_method: Optional[str] = None
    remarks: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    accumulated_depreciation: float = 0.0
    net_book_value: float
    category_name: Optional[str] = None
    subcategory_name: Optional[str] = None
    assigned_to_name: Optional[str] = None

    class Config:
        orm_mode = True

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    asset_count: Optional[int] = None

    class Config:
        orm_mode = True

# Role and Permission schemas
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permissions: List[int]  # List of permission IDs to assign

class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    permissions: List[str]  # List of permission names

    class Config:
        orm_mode = True

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    permissions: List[str] = []