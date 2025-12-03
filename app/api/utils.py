"""
Utility functions for converting between service models and API schemas.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..core.models import Asset, User, Role, Permission, AssetCategory
from . import schemas


def convert_asset_to_response(asset: Asset) -> Dict[str, Any]:
    """Convert an Asset model to API response format"""
    # Support both dicts returned from service and ORM Asset objects
    if isinstance(asset, dict):
        return {
            'id': asset.get('id'),
            'asset_id': asset.get('asset_id'),
            'name': asset.get('name'),
            'description': asset.get('description'),
            'category_id': asset.get('category_id'),
            'subcategory_id': asset.get('subcategory_id'),
            'acquisition_date': asset.get('acquisition_date'),
            'supplier': asset.get('supplier'),
            'quantity': asset.get('quantity'),
            'unit_cost': float(asset.get('unit_cost', 0)),
            'total_cost': float(asset.get('total_cost', 0)),
            'location': asset.get('location'),
            'custodian': asset.get('custodian'),
            'department': asset.get('department'),
            'assigned_to_id': asset.get('assigned_to_id'),
            'status': asset.get('status'),
            'asset_tag': asset.get('asset_tag'),
            'serial_number': asset.get('serial_number'),
            'useful_life': asset.get('useful_life'),
            'depreciation_method': asset.get('depreciation_method'),
            'accumulated_depreciation': float(asset.get('accumulated_depreciation', 0)),
            'net_book_value': float(asset.get('net_book_value', 0)),
            'remarks': asset.get('remarks'),
            'created_at': asset.get('created_at'),
            'updated_at': asset.get('updated_at'),
            'category_name': asset.get('category_name'),
            'subcategory_name': asset.get('subcategory_name'),
            'assigned_to_name': asset.get('assigned_to_name')
        }

    return {
        "id": asset.id,
        "asset_id": asset.asset_id,
        "name": asset.name,
        "description": asset.description,
        "category_id": asset.category_id,
        "subcategory_id": asset.subcategory_id,
        "acquisition_date": asset.acquisition_date,
        "supplier": asset.supplier,
        "quantity": asset.quantity,
        "unit_cost": float(asset.unit_cost),
        "total_cost": float(asset.total_cost),
        "location": asset.location,
        "custodian": asset.custodian,
        "department": asset.department,
        "assigned_to_id": asset.assigned_to_id,
        "status": asset.status.value,
        "asset_tag": asset.asset_tag,
        "serial_number": asset.serial_number,
        "useful_life": asset.useful_life,
        "depreciation_method": asset.depreciation_method.value if asset.depreciation_method else None,
        "accumulated_depreciation": float(asset.accumulated_depreciation),
        "net_book_value": float(asset.net_book_value),
        "remarks": asset.remarks,
        "created_at": asset.created_at,
        "updated_at": asset.updated_at,
        "category_name": asset.category.name if asset.category else None,
        "subcategory_name": asset.subcategory.name if asset.subcategory else None,
        "assigned_to_name": asset.assigned_to.name if asset.assigned_to else None
    }


def convert_user_to_response(user: User, include_permissions: bool = False) -> Dict[str, Any]:
    """Convert a User model to API response format"""
    response = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "department": user.department,
        "position": user.position,
        "role_id": user.role_id,
        "is_active": user.is_active,
        "last_login": user.last_login,
        "role_name": user.role.name.value if user.role else None
    }
    
    if include_permissions and user.role:
        response["permissions"] = [
            perm.permission.name.value 
            for perm in user.role.permissions 
            if perm.granted == "true"
        ]
    
    return response


def convert_category_to_response(category: AssetCategory) -> Dict[str, Any]:
    """Convert an AssetCategory model to API response format"""
    # Support both dicts (returned by service) and ORM models
    if isinstance(category, dict):
        return {
            'id': category.get('id'),
            'name': category.get('name'),
            'description': category.get('description'),
            'created_at': category.get('created_at'),
            'asset_count': category.get('asset_count', 0)
        }

    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "created_at": category.created_at,
        "asset_count": len(category.assets) if category.assets else 0
    }


def convert_role_to_response(role: Role, include_stats: bool = False) -> Dict[str, Any]:
    """Convert a Role model to API response format"""
    response = {
        "id": role.id,
        "name": role.name.value,
        "description": role.description,
        "created_at": role.created_at,
        "permissions": [
            perm.permission.name.value 
            for perm in role.permissions 
            if perm.granted == "true"
        ]
    }
    
    if include_stats:
        response["users_count"] = len(role.users)
        response["conditional_permissions"] = [
            perm.permission.name.value 
            for perm in role.permissions 
            if perm.granted == "conditional"
        ]
    
    return response