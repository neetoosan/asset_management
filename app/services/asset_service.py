from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_, and_
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta, date
import json

from ..core.models import (
    Asset, AssetCategory, AssetSubCategory, User, AssetStatus, 
    DepreciationMethod, AuditLog
)
from ..core.models import PermissionType, UserRole
from ..core.database import get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import DetachedInstanceError
from .audit_service import AuditService
from .settings_service import SettingsService
import logging

# Custom type hints
AssetFilters = Dict[str, Union[str, int, None]]
AssetStatistics = Dict[str, Union[float, Dict[str, int]]]


class AssetService:
    def __init__(self):
        self.audit_service = AuditService()
        self.settings_service = SettingsService()
        self._current_user_id = None
        self._current_user_name = None
    
    def set_current_user(self, user_id: int, user_name: str):
        """Set current user for audit logging."""
        self._current_user_id = user_id
        self._current_user_name = user_name
        self.audit_service.set_current_user(user_id, user_name)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return get_db()

    def get_all_categories(self, session: Session = None) -> List[dict]:
        """Get all asset categories as primitive dicts.
        Always return primitive dicts with these keys: id, name, description,
        created_at, asset_count. Returning primitives prevents DetachedInstanceError
        when the UI accesses values after sessions are closed.
        """
        try:
            # Use provided session or open a new one
            if session is None:
                ctx = get_db()
                cm = ctx
            else:
                # If caller provided a session, use it directly (not context manager)
                cm = None

            if cm is not None:
                with cm as s:
                    rows = s.query(AssetCategory).order_by(AssetCategory.name).all()
                    result = []
                    for r in rows:
                        asset_count = len(r.assets) if hasattr(r, 'assets') and r.assets is not None else 0
                        result.append({
                            'id': r.id,
                            'name': r.name,
                            'description': getattr(r, 'description', None),
                            'created_at': getattr(r, 'created_at', None),
                            'asset_count': asset_count
                        })
                    return result
            else:
                rows = session.query(AssetCategory).order_by(AssetCategory.name).all()
                result = []
                for r in rows:
                    asset_count = len(r.assets) if hasattr(r, 'assets') and r.assets is not None else 0
                    result.append({
                        'id': r.id,
                        'name': r.name,
                        'description': getattr(r, 'description', None),
                        'created_at': getattr(r, 'created_at', None),
                        'asset_count': asset_count
                    })
                return result
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def get_category_by_name(self, session: Session, name: str) -> Optional[AssetCategory]:
        """Get category by name"""
        try:
            return session.query(AssetCategory).filter(AssetCategory.name == name).first()
        except Exception as e:
            print(f"Error getting category by name: {e}")
            return None
    
    def get_subcategories_by_category_id(self, session: Session, category_id: int) -> List[dict]:
        """Get subcategories for a specific category as primitive dicts."""
        try:
            rows = session.query(AssetSubCategory).filter(
                AssetSubCategory.category_id == category_id
            ).order_by(AssetSubCategory.name).all()
            return [{'id': r.id, 'name': r.name, 'category_id': r.category_id} for r in rows]
        except Exception as e:
            print(f"Error getting subcategories: {e}")
            return []
    
    def get_all_assets(self, session: Session = None) -> List[Asset]:
        """Get all assets with category and subcategory information"""
        try:
            # Always return primitive dicts to avoid DetachedInstanceError when UI accesses attributes
            if session is None:
                with get_db() as s:
                    rows = (s.query(Asset)
                           .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                           .filter(Asset.status.notin_([AssetStatus.RETIRED, AssetStatus.DISPOSED]))
                           .order_by(Asset.created_at.desc())
                           .all())
                    # Convert to primitive dicts while session is still open to avoid DetachedInstanceError
                    return [self._asset_to_dict(a) for a in rows]
            else:
                rows = (session.query(Asset)
                       .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                       .filter(Asset.status.notin_([AssetStatus.RETIRED, AssetStatus.DISPOSED]))
                       .order_by(Asset.created_at.desc())
                       .all())

            # If a session was provided by the caller, convert using that active session
            return [self._asset_to_dict(a) for a in rows]
        except Exception as e:
            print(f"Error getting all assets: {e}")
            return []

    def get_assets_by_category_name(self, session: Session | str = None, category_name: str | None = None) -> List[Asset]:
        """Get all assets in a specific category by name.

        Usage:
          - get_assets_by_category_name(session, category_name)
          - get_assets_by_category_name(category_name)

        The method auto-detects whether the first argument is a Session or a
        category name string for backward compatibility with existing callers.
        """
        try:
            # Support being called as get_assets_by_category_name(category_name)
            if category_name is None and isinstance(session, str):
                category_name = session
                session = None

            if category_name is None:
                return []

            if category_name.lower() == 'all':
                return self.get_all_assets(session)

            if session is None:
                with get_db() as s:
                    rows = (s.query(Asset)
                           .join(AssetCategory)
                           .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                           .filter(AssetCategory.name == category_name)
                           .order_by(Asset.created_at.desc())
                           .all())
                    # Convert to primitive dicts while session is still open
                    return [self._asset_to_dict(a) for a in rows]
            else:
                rows = (session.query(Asset)
                       .join(AssetCategory)
                       .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                       .filter(AssetCategory.name == category_name)
                       .order_by(Asset.created_at.desc())
                       .all())

            # If caller supplied an active session, convert using that session
            return [self._asset_to_dict(a) for a in rows]
        except Exception as e:
            print(f"Error getting assets by category name: {e}")
            return []
    
    def get_assets_by_category_id(self, session: Session, category_id: int) -> List[Asset]:
        """Get all assets in a specific category"""
        try:
            rows = (session.query(Asset)
                   .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                   .filter(Asset.category_id == category_id)
                   .order_by(Asset.created_at.desc())
                   .all())
            return [self._asset_to_dict(a) for a in rows]
        except Exception as e:
            print(f"Error getting assets by category ID: {e}")
            return []
    
    def get_assets_by_status(self) -> Dict[str, int]:
        """Get count of assets by status"""
        try:
            with get_db() as session:
                status_counts = (session.query(Asset.status, func.count(Asset.id))
                               .group_by(Asset.status)
                               .all())
                return {status.value: count for status, count in status_counts}
        except Exception as e:
            print(f"Error getting assets by status: {e}")
            return {}

    def get_assets_by_category(self, session: Session = None) -> Dict[str, Dict[str, Any]]:
        """Get assets statistics by category"""
        try:
            if session is None:
                with get_db() as session:
                    return self._get_assets_by_category_stats(session)
            return self._get_assets_by_category_stats(session)
        except Exception as e:
            print(f"Error getting assets by category: {e}")
            return {}
            
    def _get_assets_by_category_stats(self, session: Session) -> Dict[str, Dict[str, Any]]:
        """Helper method to get asset statistics by category"""
        try:
            # Query the database for category statistics
            category_stats = session.query(
                AssetCategory.name,
                func.count(Asset.id).label('count'),
                func.coalesce(func.sum(Asset.total_cost), 0).label('total_value'),
                func.coalesce(func.sum(Asset.accumulated_depreciation), 0).label('total_depreciation')
            ).outerjoin(Asset).group_by(AssetCategory.id, AssetCategory.name).all()
            
            # Process results into dictionary
            result = {}
            for stat in category_stats:
                result[stat.name] = {
                    'count': stat.count,
                    'total_value': float(stat.total_value),
                    'total_depreciation': float(stat.total_depreciation),
                    'net_book_value': float(stat.total_value - stat.total_depreciation)
                }
            return result
            
        except Exception as e:
            print(f"Error getting category statistics: {e}")
            return {}
    
    def get_category_summary(self, session: Session = None) -> List[Dict[str, Any]]:
        """Get asset count and value by category"""
        try:
            if session is None:
                with get_db() as session:
                    return self._get_category_summary_internal(session)
            return self._get_category_summary_internal(session)
        except Exception as e:
            print(f"Error getting category summary: {e}")
            return []
            
    def _get_category_summary_internal(self, session: Session) -> List[Dict[str, Any]]:
        """Internal method to get category summary with session"""
        try:
            category_stats = (session.query(
                AssetCategory.name,
                func.count(Asset.id).label('count'),
                func.coalesce(func.sum(Asset.total_cost), 0).label('total_value')
            ).outerjoin(Asset)
            .group_by(AssetCategory.id, AssetCategory.name)
            .order_by(AssetCategory.name)
            .all())
            
            return [{
                'category': stat.name, 
                'count': stat.count,
                'total_value': float(stat.total_value)
            } for stat in category_stats]
        except Exception as e:
            print(f"Error getting category summary internal: {e}")
            return []
    
    def get_recently_added_assets(self, session: Session, days: int = 7) -> List[Asset]:
        """Get assets added in the last N days"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            rows = (session.query(Asset)
                   .options(joinedload(Asset.category))
                   .filter(Asset.created_at >= cutoff_date)
                   .order_by(desc(Asset.created_at))
                   .limit(10)
                   .all())
            return [self._asset_to_dict(a) for a in rows]
        except Exception as e:
            print(f"Error getting recently added assets: {e}")
            return []
    
    def search_assets(self, query: str) -> List[Asset]:
        """Search assets by name, asset_id, description, or location"""
        if not query.strip():
            return self.get_all_assets()
            
        try:
            with get_db() as session:
                search_term = f'%{query}%'
                rows = (session.query(Asset)
                       .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                       .filter(
                           or_(
                               Asset.name.like(search_term),
                               Asset.asset_id.like(search_term),
                               Asset.description.like(search_term),
                               Asset.location.like(search_term),
                               Asset.asset_tag.like(search_term)
                           )
                       )
                       .order_by(Asset.created_at.desc())
                       .all())
                return [self._asset_to_dict(a) for a in rows]
        except Exception as e:
            print(f"Error searching assets: {e}")
            return []
    
    def can_create_asset(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if asset creation is allowed based on system settings"""
        # Check if asset creation is allowed
        if not self.settings_service.can_create_asset():
            return {
                "success": False, 
                "message": "Asset creation is currently disabled by system settings"
            }
        # No high-value approval enforcement here.
        # The settings service controls whether creation is allowed;
        # any threshold/approval policy is intentionally not enforced in the
        # asset service so users can create assets regardless of total_cost.
        return {"success": True, "message": "Asset creation allowed"}
    
    def create_asset(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new asset with validation and audit logging"""
        # Check permissions
        permission_check = self.can_create_asset(asset_data)
        if not permission_check["success"]:
            return permission_check
        
        try:
            with get_db() as session:
                # Handle enum conversions
                if 'status' in asset_data and isinstance(asset_data['status'], str):
                    try:
                        asset_data['status'] = AssetStatus(asset_data['status'])
                    except ValueError:
                        asset_data['status'] = AssetStatus.AVAILABLE
                
                if 'depreciation_method' in asset_data and isinstance(asset_data['depreciation_method'], str):
                    try:
                        asset_data['depreciation_method'] = DepreciationMethod(asset_data['depreciation_method'])
                    except ValueError:
                        asset_data.pop('depreciation_method', None)
                
                # Calculate net book value
                if 'total_cost' in asset_data and 'accumulated_depreciation' in asset_data:
                    asset_data['net_book_value'] = asset_data['total_cost'] - asset_data.get('accumulated_depreciation', 0)
                elif 'total_cost' in asset_data:
                    asset_data['net_book_value'] = asset_data['total_cost']
                # Remove keys that are not columns on the Asset model (e.g., annual_depreciation)
                try:
                    allowed_fields = set(Asset.__table__.columns.keys())
                except Exception:
                    allowed_fields = { 
                        'id','asset_id','description','name','category_id','subcategory_id','acquisition_date',
                        'supplier','quantity','unit_cost','total_cost','useful_life','depreciation_method',
                        'depreciation_percentage','accumulated_depreciation','net_book_value','location','custodian','department',
                        'assigned_to_id','status','asset_tag','serial_number','remarks','created_at','updated_at','expiry_date',
                        'model_number'
                    }

                filtered_data = {k: v for k, v in asset_data.items() if k in allowed_fields}

                # Ensure asset_id is unique: if provided and exists, generate a unique fallback
                provided_asset_id = filtered_data.get('asset_id')
                if provided_asset_id:
                    exists = session.query(Asset).filter(Asset.asset_id == provided_asset_id).first()
                    if exists:
                        # Append a numeric suffix to try to make it unique
                        base = provided_asset_id
                        suffix = 1
                        new_id = f"{base}-{suffix}"
                        while session.query(Asset).filter(Asset.asset_id == new_id).first():
                            suffix += 1
                            new_id = f"{base}-{suffix}"
                        filtered_data['asset_id'] = new_id

                asset = Asset(**filtered_data)
                session.add(asset)
                try:
                    session.commit()
                except IntegrityError as ie:
                    session.rollback()
                    return {"success": False, "message": f"Asset creation failed: duplicate asset ID or constraint violation ({str(ie.orig)})"}
                session.refresh(asset)
                
                # Audit logging
                self.audit_service.log_action(
                    action="ASSET_CREATED",
                    description=f"Created asset: {asset.name} (ID: {asset.asset_id})",
                    table_name="assets",
                    record_id=str(asset.id),
                    new_values=self._asset_to_dict(asset)
                )
                
                return {
                    "success": True,
                    "message": "Asset created successfully",
                    "asset": self._asset_to_dict(asset)
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating asset: {str(e)}"
            }
    
    def get_asset_by_id(self, asset_id: int) -> Optional[Asset]:
        """Get an asset by ID"""
        try:
            with get_db() as session:
                asset = (session.query(Asset)
                       .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                       .filter(Asset.id == asset_id)
                       .first())
                return self._asset_to_dict(asset) if asset else None
        except Exception as e:
            print(f"Error getting asset by ID: {e}")
            return None
    
    def can_update_asset(self, asset: Asset, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if asset update is allowed"""
        if not self.settings_service.can_edit_asset():
            return {
                "success": False,
                "message": "Asset editing is currently disabled by system settings"
            }
        # No high-value approval enforcement on updates.
        # Updates are allowed as long as editing is enabled in system settings.
        return {"success": True, "message": "Asset update allowed"}
    
    def update_asset(self, asset_id: int, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing asset with validation and audit logging"""
        try:
            # Defensive: if caller passed an ORM instance, extract its id
            try:
                if not isinstance(asset_id, (int, str)) and hasattr(asset_id, 'id'):
                    asset_id = getattr(asset_id, 'id')
            except Exception:
                pass

            with get_db() as session:
                asset = session.query(Asset).filter(Asset.id == asset_id).first()
                if not asset:
                    return {"success": False, "message": "Asset not found"}
                
                # Store old values for audit early (use safe access to avoid DetachedInstanceError)
                old_values = self._asset_to_dict(asset)

                # Check permissions
                permission_check = self.can_update_asset(asset, asset_data)
                if not permission_check["success"]:
                    return permission_check
                
                # Handle enum conversions
                if 'status' in asset_data and isinstance(asset_data['status'], str):
                    try:
                        asset_data['status'] = AssetStatus(asset_data['status'])
                    except ValueError:
                        pass  # Keep existing status if invalid
                
                if 'depreciation_method' in asset_data and isinstance(asset_data['depreciation_method'], str):
                    try:
                        asset_data['depreciation_method'] = DepreciationMethod(asset_data['depreciation_method'])
                    except ValueError:
                        asset_data.pop('depreciation_method', None)
                
                # Update asset attributes
                for key, value in asset_data.items():
                    if hasattr(asset, key) and key not in ['id', 'created_at']:
                        setattr(asset, key, value)
                
                # Recalculate net book value if needed
                if 'total_cost' in asset_data or 'accumulated_depreciation' in asset_data:
                    asset.net_book_value = asset.total_cost - (asset.accumulated_depreciation or 0)
                
                asset.updated_at = datetime.utcnow()
                try:
                    session.commit()
                except IntegrityError as ie:
                    session.rollback()
                    return {"success": False, "message": f"Asset update failed: constraint violation ({str(ie)})"}

                # Re-query the asset on the same session to ensure we are working with
                # a session-bound, up-to-date instance. This avoids refresh operations
                # on instances that may not be bound to the current session.
                try:
                    asset = (session.query(Asset)
                             .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                             .filter(Asset.id == asset_id)
                             .first())
                except Exception:
                    asset = None
                if asset is None:
                    # As a fallback, return the primitive representation built from old_values
                    return {
                        "success": True,
                        "message": "Asset updated successfully",
                        "asset": old_values
                    }
                
                # Audit logging
                new_values = self._asset_to_dict(asset)
                self.audit_service.log_action(
                    action="ASSET_UPDATED",
                    description=f"Updated asset: {asset.name} (ID: {asset.asset_id})",
                    table_name="assets",
                    record_id=str(asset.id),
                    old_values=old_values,
                    new_values=new_values
                )
                
                return {
                    "success": True,
                    "message": "Asset updated successfully",
                    "asset": new_values
                }
                
        except DetachedInstanceError:
            # Defensive retry: if we hit a DetachedInstanceError for any reason,
            # re-run the update in a fresh session by re-querying the asset and
            # applying the changes. This handles cases where callers passed
            # detached ORM instances or where the session state got lost.
            try:
                with get_db() as session2:
                    asset2 = session2.query(Asset).filter(Asset.id == asset_id).first()
                    if not asset2:
                        return {"success": False, "message": "Asset not found (retry)"}

                    # Handle enum conversions (same logic as primary path)
                    if 'status' in asset_data and isinstance(asset_data['status'], str):
                        try:
                            asset_data['status'] = AssetStatus(asset_data['status'])
                        except Exception:
                            # keep original string if conversion fails
                            pass

                    if 'depreciation_method' in asset_data and isinstance(asset_data['depreciation_method'], str):
                        try:
                            asset_data['depreciation_method'] = DepreciationMethod(asset_data['depreciation_method'])
                        except Exception:
                            # If conversion fails, remove to avoid DB errors
                            asset_data.pop('depreciation_method', None)

                    # Apply updates again safely
                    for key, value in asset_data.items():
                        if hasattr(asset2, key) and key not in ['id', 'created_at']:
                            setattr(asset2, key, value)

                    if 'total_cost' in asset_data or 'accumulated_depreciation' in asset_data:
                        asset2.net_book_value = asset2.total_cost - (asset2.accumulated_depreciation or 0)
                    asset2.updated_at = datetime.utcnow()
                    try:
                        session2.commit()
                    except IntegrityError as ie:
                        session2.rollback()
                        return {"success": False, "message": f"Asset update failed on retry: constraint violation ({str(ie)})"}

                    new_values = self._asset_to_dict(asset2)
                    self.audit_service.log_action(
                        action="ASSET_UPDATED",
                        description=f"Updated asset (retry): {asset2.name} (ID: {asset2.asset_id})",
                        table_name="assets",
                        record_id=str(asset2.id),
                        old_values=old_values,
                        new_values=new_values
                    )

                    return {"success": True, "message": "Asset updated successfully (retry)", "asset": new_values}
            except Exception as e:
                return {"success": False, "message": f"Error updating asset on retry: {str(e)}"}
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating asset: {str(e)}"
            }
    
    def can_delete_asset(self, asset: Asset) -> Dict[str, Any]:
        """Check if asset deletion is allowed"""
        logger = logging.getLogger(__name__)
        # Normalize input: caller may pass an ORM Asset instance or an id. Ensure we
        # operate on a session-bound Asset instance to avoid DetachedInstanceError.
        aid = None
        try:
            if isinstance(asset, (int, str)):
                aid = int(asset)
            else:
                aid = getattr(asset, 'id', None)
                if isinstance(aid, str) and aid.isdigit():
                    aid = int(aid)
        except Exception:
            aid = None

        is_admin = False
        user_info = None
        try:
            # Treat the special admin session id (0) as admin without DB lookup
            if getattr(self, '_current_user_id', None) == 0:
                is_admin = True
            elif getattr(self, '_current_user_id', None):
                from .user_service import UserService
                user_svc = UserService()
                user_info = user_svc.get_user_by_id(self._current_user_id)
                if user_info and user_info.get('role') == UserRole.ADMIN.value:
                    is_admin = True
        except Exception as e:
            # Non-fatal: log and continue; permission checks below will handle failures
            logger.exception("Error fetching current user for delete check: %s", e)

        # Permission-first policy: explicit Delete permission grants ability
        # to delete regardless of the global toggle. Admins bypass checks.

        # Don't allow deletion of assets that are currently in use
        # Use a session-bound instance to check status safely.
        try:
            if aid is not None:
                with get_db() as session:
                    a = session.query(Asset).filter(Asset.id == aid).first()
                    if a and a.status == AssetStatus.IN_USE:
                        return {"success": False, "message": "Cannot delete assets that are currently in use"}
            else:
                # If we don't have an id, try to read status defensively
                try:
                    st = getattr(asset, 'status')
                    if st == AssetStatus.IN_USE:
                        return {"success": False, "message": "Cannot delete assets that are currently in use"}
                except DetachedInstanceError:
                    # Treat as unknown/in use? Deny to be safe
                    return {"success": False, "message": "Cannot verify asset state for deletion"}
        except Exception as e:
            logger.exception("Error checking asset usage state: %s", e)
            return {"success": False, "message": "Error verifying asset state"}

        # Admins bypass the permission check and are allowed
        if is_admin:
            return {"success": True, "message": "Asset deletion allowed"}

        # For non-admins, preference order:
        # 1. If user has explicit DELETE_ASSET permission, allow
        # 2. Else if global setting allows deletion, allow
        # 3. Otherwise deny
        try:
            # Ensure we log current context for debugging permission failures
            logger.debug("can_delete_asset called: current_user_id=%r, aid=%r", getattr(self, '_current_user_id', None), aid)
            if not getattr(self, '_current_user_id', None):
                logger.warning("Deletion blocked: no authenticated user in AssetService context")
                return {"success": False, "message": "Deletion requires an authenticated user"}

            # Prefer to check permissions directly in the DB to avoid any
            # potential context/instance issues with UserService.
            try:
                with get_db() as session:
                    user = session.query(User).options(joinedload(User.role)).filter(User.id == self._current_user_id).first()
                    if user and user.role:
                        # Check RolePermission for DELETE_ASSET
                        from ..core.models import RolePermission, Permission
                        rp = session.query(RolePermission).join(Permission, RolePermission.permission_id == Permission.id).filter(
                            RolePermission.role_id == user.role.id,
                            Permission.name == PermissionType.DELETE_ASSET,
                            RolePermission.granted == 'true'
                        ).first()
                        if rp:
                            logger.debug("User %r allowed via RolePermission", self._current_user_id)
                            return {"success": True, "message": "Asset deletion allowed"}
            except Exception as e:
                logger.exception("Error checking RolePermission directly: %s", e)

            # Fall back to global toggle if no explicit permission found
            if self.settings_service.can_delete_asset():
                logger.debug("Asset deletion allowed via global setting")
                return {"success": True, "message": "Asset deletion allowed"}

            logger.warning("Asset deletion blocked: no delete permission and global setting disabled (user=%r)", getattr(self, '_current_user_id', None))
            return {"success": False, "message": "Asset deletion is currently disabled by system settings"}
        except Exception as e:
            print(f"Error checking delete permission: {e}")
            return {"success": False, "message": "Error verifying delete permissions"}
    
    def delete_asset(self, asset_id: int, reason: str = None, permanent: bool = False) -> Dict[str, Any]:
        """Delete an asset.
        By default this performs a soft-delete (marking the asset as
        RETIRED). If `permanent=True` a hard delete is performed and the
        row is removed from the database. Audit logging records the action
        in both cases.
        """
        logger = logging.getLogger(__name__)
        try:
            # Small trace to help diagnose detached-instance calls in user environments
            logger.debug("delete_asset called with asset_id=%r permanent=%s by user=%r", asset_id, permanent, getattr(self, '_current_user_id', None))

            # Defensive: callers may pass an ORM Asset instance, an int ID, or an asset_id string.
            aid = None
            try:
                if isinstance(asset_id, (int, str)):
                    aid = int(asset_id)
                else:
                    # Try to read .id from an ORM instance/object without triggering lazy loads
                    aid = getattr(asset_id, 'id', None)
                    if isinstance(aid, str) and aid.isdigit():
                        aid = int(aid)
            except Exception:
                aid = None

            with get_db() as session:
                # Prefer a fresh, session-bound instance: normalize to id and re-query
                asset = None
                if aid is not None:
                    asset = session.query(Asset).filter(Asset.id == aid).first()
                else:
                    # If caller passed an object with an 'id' attribute, try to use it
                    try:
                        possible_id = getattr(asset_id, 'id', None)
                        if isinstance(possible_id, (int, str)):
                            aid = int(possible_id)
                            asset = session.query(Asset).filter(Asset.id == aid).first()
                    except Exception:
                        pass

                # As a last resort, lookup by user-defined asset_id string
                if asset is None:
                    try:
                        asset = session.query(Asset).filter(Asset.asset_id == str(asset_id)).first()
                        if asset:
                            aid = asset.id
                    except Exception:
                        asset = None

                if not asset:
                    return {"success": False, "message": "Asset not found"}

                # Now asset is bound to the current session. Run permission checks safely.
                try:
                    permission_check = self.can_delete_asset(asset)
                    if not permission_check["success"]:
                        return permission_check
                except DetachedInstanceError:
                    # If we somehow hit a DetachedInstanceError, re-query by id and retry
                    logger.debug("DetachedInstanceError during permission check, re-querying by id=%r", aid)
                    if aid is None:
                        return {"success": False, "message": "Unable to verify permissions for deletion"}
                    asset = session.query(Asset).filter(Asset.id == aid).first()
                    if not asset:
                        return {"success": False, "message": "Asset not found (permission retry)"}
                    permission_check = self.can_delete_asset(asset)
                    if not permission_check["success"]:
                        return permission_check

                # Store asset data for audit from the session-bound instance
                try:
                    asset_data = self._asset_to_dict(asset)
                except Exception:
                    # Defensive minimal audit data if conversion fails
                    asset_data = {
                        'id': getattr(asset, 'id', aid),
                        'asset_id': getattr(asset, 'asset_id', None),
                        'name': getattr(asset, 'name', None)
                    }

                # Hard delete path
                if permanent:
                    try:
                        session.delete(asset)
                        session.commit()
                    except DetachedInstanceError:
                        # Fallback: perform a direct delete by id in a fresh session
                        try:
                            session.rollback()
                        except Exception:
                            pass
                        rid = aid or asset_data.get('id')
                        if not rid:
                            return {"success": False, "message": "Could not determine asset id for permanent delete"}
                        with get_db() as session2:
                            try:
                                a2 = session2.query(Asset).filter(Asset.id == rid).first()
                                if not a2:
                                    return {"success": False, "message": "Asset not found (during permanent delete)"}
                                old_vals = self._asset_to_dict(a2)
                                session2.delete(a2)
                                session2.commit()
                                desc = f"Permanently deleted asset: {old_vals.get('name')} (ID: {old_vals.get('asset_id')})"
                                if reason:
                                    desc = f"{desc} -- Reason: {reason}"
                                self.audit_service.log_action(
                                    action="ASSET_PERMANENTLY_DELETED",
                                    description=desc,
                                    table_name="assets",
                                    record_id=str(rid),
                                    old_values=old_vals
                                )
                                return {"success": True, "message": "Asset permanently deleted"}
                            except Exception as ex:
                                session2.rollback()
                                logger.exception("Permanent delete fallback failed for id=%r: %s", rid, ex)
                                return {"success": False, "message": f"Failed to permanently delete asset: {ex}"}

                    # Primary path succeeded
                    desc = f"Permanently deleted asset: {asset_data.get('name')} (ID: {asset_data.get('asset_id')})"
                    if reason:
                        desc = f"{desc} -- Reason: {reason}"
                    self.audit_service.log_action(
                        action="ASSET_PERMANENTLY_DELETED",
                        description=desc,
                        table_name="assets",
                        record_id=str(asset_data.get('id') or aid),
                        old_values=asset_data
                    )

                    return {"success": True, "message": "Asset permanently deleted"}

                # Soft delete: mark as RETIRED and preserve the row for admin restore/delete
                try:
                    logger.info("Attempting soft-delete for asset id=%r asset_id=%r by user=%r", aid, getattr(asset, 'asset_id', None), getattr(self, '_current_user_id', None))
                    asset.status = AssetStatus.RETIRED
                    asset.updated_at = datetime.utcnow()
                    session.commit()
                    logger.info("Soft-delete committed for asset id=%r", getattr(asset, 'id', aid))
                except DetachedInstanceError:
                    # Fallback to UPDATE by id to avoid detached-instance problems
                    try:
                        session.rollback()
                    except Exception:
                        pass
                    rid = aid or asset_data.get('id')
                    if not rid:
                        return {"success": False, "message": "Could not determine asset id for soft delete"}
                    with get_db() as session2:
                        try:
                            a2 = session2.query(Asset).filter(Asset.id == rid).first()
                            if not a2:
                                return {"success": False, "message": "Asset not found (during soft delete)"}
                            old_vals = self._asset_to_dict(a2)
                            session2.query(Asset).filter(Asset.id == rid).update({
                                'status': AssetStatus.RETIRED,
                                'updated_at': datetime.utcnow()
                            }, synchronize_session=False)
                            session2.commit()
                            desc = f"Soft-deleted asset: {old_vals.get('name')} (ID: {old_vals.get('asset_id')})"
                            if reason:
                                desc = f"{desc} -- Reason: {reason}"
                            self.audit_service.log_action(
                                action="ASSET_SOFT_DELETED",
                                description=desc,
                                table_name="assets",
                                record_id=str(rid),
                                old_values=old_vals
                            )
                            logger.info("Soft-delete fallback committed for asset id=%r", rid)
                            return {"success": True, "message": "Asset retired (soft-deleted)"}
                        except Exception as ex:
                            session2.rollback()
                            logger.exception("Soft-delete fallback failed for id=%r: %s", rid, ex)
                            return {"success": False, "message": f"Asset soft-delete failed: {ex}"}

                # Primary path succeeded, log audit using previously captured asset_data
                desc = f"Soft-deleted asset: {asset_data.get('name')} (ID: {asset_data.get('asset_id')})"
                if reason:
                    desc = f"{desc} -- Reason: {reason}"
                self.audit_service.log_action(
                    action="ASSET_SOFT_DELETED",
                    description=desc,
                    table_name="assets",
                    record_id=str(asset_data.get('id') or aid),
                    old_values=asset_data
                )

                return {"success": True, "message": "Asset retired (soft-deleted)"}

        except Exception as e:
            logger.exception("Unhandled error in delete_asset: %s", e)
            return {"success": False, "message": f"Error deleting asset: {str(e)}"}
    
    def get_asset_by_asset_id(self, asset_id: str) -> Optional[Asset]:
        """Get an asset by its user-defined asset_id"""
        try:
            with get_db() as session:
                asset = (session.query(Asset)
                       .options(joinedload(Asset.category), joinedload(Asset.subcategory))
                       .filter(Asset.asset_id == asset_id)
                       .first())
                return self._asset_to_dict(asset) if asset else None
        except Exception as e:
            print(f"Error getting asset by asset ID: {e}")
            return None
    
    def bulk_update_assets(self, asset_ids: List[int], update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Bulk update multiple assets"""
        if not self.settings_service.can_bulk_operate():
            return {
                "success": False,
                "message": "Bulk operations are currently disabled by system settings"
            }
        
        try:
            with get_db() as session:
                updated_count = 0
                errors = []
                
                for asset_id in asset_ids:
                    try:
                        result = self.update_asset(asset_id, update_data)
                        if result["success"]:
                            updated_count += 1
                        else:
                            errors.append(f"Asset {asset_id}: {result['message']}")
                    except Exception as e:
                        errors.append(f"Asset {asset_id}: {str(e)}")
                
                return {
                    "success": True,
                    "message": f"Updated {updated_count} assets",
                    "updated_count": updated_count,
                    "errors": errors
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error in bulk update: {str(e)}"
            }

    def restore_asset(self, asset_id: int) -> Dict[str, Any]:
        """Restore an asset previously marked retired/disposed by setting status to AVAILABLE and logging the action."""
        try:
            with get_db() as session:
                asset = session.query(Asset).filter(Asset.id == asset_id).first()
                if not asset:
                    return {"success": False, "message": "Asset not found"}

                # Only restore if asset is in retired/disposed
                if asset.status not in [AssetStatus.RETIRED, AssetStatus.DISPOSED]:
                    return {"success": False, "message": "Asset is not in a deletable state"}

                old = self._asset_to_dict(asset)
                asset.status = AssetStatus.AVAILABLE
                asset.updated_at = datetime.utcnow()
                session.commit()

                # Audit log
                self.audit_service.log_action(
                    action="ASSET_RESTORED",
                    description=f"Restored asset: {old.get('name')} (ID: {old.get('asset_id')})",
                    table_name="assets",
                    record_id=str(asset_id),
                    old_values=old
                )

                return {"success": True, "message": "Asset restored"}
        except Exception as e:
            return {"success": False, "message": f"Error restoring asset: {str(e)}"}
    
    def _asset_to_dict(self, asset: Asset) -> Dict[str, Any]:
        """Convert asset object to dictionary for audit logging"""
        # Read attributes defensively: some callers may pass detached instances
        def _safe_getattr(obj, name, default=None):
            try:
                return getattr(obj, name)
            except Exception:
                return default

        # Safely read enum values and relationship names
        try:
            depreciation_method = _safe_getattr(asset, 'depreciation_method')
            depreciation_method_val = depreciation_method.value if depreciation_method else None
        except Exception:
            depreciation_method_val = None

        try:
            status_attr = _safe_getattr(asset, 'status')
            status_val = status_attr.value if status_attr else None
        except Exception:
            status_val = None

        # Category name may be a relationship; avoid triggering lazy load on a closed session
        try:
            cat = _safe_getattr(asset, 'category')
            category_name = cat.name if cat is not None and hasattr(cat, 'name') else None
        except Exception:
            category_name = None

        try:
            sub = _safe_getattr(asset, 'subcategory')
            subcategory_name = sub.name if sub is not None and hasattr(sub, 'name') else None
        except Exception:
            subcategory_name = None

        # Dates and numeric conversions
        acq = _safe_getattr(asset, 'acquisition_date')
        try:
            acq_iso = acq.isoformat() if acq else None
        except Exception:
            acq_iso = str(acq) if acq is not None else None

        # Expiry date handling
        expiry = _safe_getattr(asset, 'expiry_date')
        try:
            expiry_iso = expiry.isoformat() if expiry else None
        except Exception:
            expiry_iso = str(expiry) if expiry is not None else None

        def _to_float(val):
            try:
                return float(val) if val is not None else None
            except Exception:
                return None

        return {
            'id': _safe_getattr(asset, 'id'),
            'asset_id': _safe_getattr(asset, 'asset_id'),
            'name': _safe_getattr(asset, 'name'),
            'description': _safe_getattr(asset, 'description'),
            'category_id': _safe_getattr(asset, 'category_id'),
            'category_name': category_name,
            'subcategory_id': _safe_getattr(asset, 'subcategory_id'),
            'subcategory_name': subcategory_name,
            'acquisition_date': acq_iso,
            'expiry_date': expiry_iso,  # Calculated expiry date
            'supplier': _safe_getattr(asset, 'supplier'),
            'quantity': _safe_getattr(asset, 'quantity'),
            'unit_cost': _to_float(_safe_getattr(asset, 'unit_cost')),
            'total_cost': _to_float(_safe_getattr(asset, 'total_cost')),
            'useful_life': _safe_getattr(asset, 'useful_life'),
            'depreciation_method': depreciation_method_val,
            'depreciation_percentage': _to_float(_safe_getattr(asset, 'depreciation_percentage')),
            'accumulated_depreciation': _to_float(_safe_getattr(asset, 'accumulated_depreciation')),
            'net_book_value': _to_float(_safe_getattr(asset, 'net_book_value')),
            'location': _safe_getattr(asset, 'location'),
            'custodian': _safe_getattr(asset, 'custodian'),
            'department': _safe_getattr(asset, 'department'),
            'assigned_to_id': _safe_getattr(asset, 'assigned_to_id'),
            'status': status_val,
            'asset_tag': _safe_getattr(asset, 'asset_tag'),
            'serial_number': _safe_getattr(asset, 'serial_number'),
            'model_number': _safe_getattr(asset, 'model_number'),
            'remarks': _safe_getattr(asset, 'remarks')
        }
