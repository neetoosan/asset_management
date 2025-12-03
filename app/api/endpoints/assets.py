from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.services import asset_service
from app.core.models import AssetStatus
from ..schemas import AssetCreate, AssetResponse, CategoryResponse
from ..utils import convert_asset_to_response, convert_category_to_response

AssetService = asset_service.AssetService

router = APIRouter(prefix="/assets", tags=["assets"])
asset_service = AssetService()

@router.get("/", response_model=List[AssetResponse])
async def get_all_assets(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by asset status"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    department: Optional[str] = Query(None, description="Filter by department"),
    location: Optional[str] = Query(None, description="Filter by location"),
    db: Session = Depends(get_db)
):
    """Get all assets with pagination and filtering"""
    filters = {
        "status": status,
        "category_id": category_id,
        "department": department,
        "location": location
    }
    assets = asset_service.get_all_assets(skip=skip, limit=limit, filters=filters)
    return [convert_asset_to_response(asset) for asset in assets]

@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: str, db: Session = Depends(get_db)):
    """Get a specific asset by ID"""
    asset = asset_service.get_asset_by_asset_id(asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return convert_asset_to_response(asset)

@router.post("/", response_model=AssetResponse)
async def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db)
):
    """Create a new asset"""
    try:
        asset_data = asset.dict()
        asset_data["total_cost"] = asset_data["unit_cost"] * asset_data["quantity"]
        created_asset = asset_service.create_asset(asset_data)
        return convert_asset_to_response(created_asset)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/categories", response_model=List[CategoryResponse])
async def get_asset_categories(db: Session = Depends(get_db)):
    """Get all asset categories using the dependency-injected session.

    Passing the FastAPI-provided session into the service ensures any
    accessed relationship attributes are loaded while the session is
    still open and avoids DetachedInstanceError when Pydantic reads
    attributes during response creation.
    """
    categories = asset_service.get_all_categories(session=db)
    return [convert_category_to_response(cat) for cat in categories]

@router.patch("/{asset_id}/status", response_model=AssetResponse)
async def update_asset_status(
    asset_id: str,
    status: AssetStatus,
    db: Session = Depends(get_db)
):
    """Update the status of an asset"""
    updated_asset = asset_service.update_asset_status(asset_id, status)
    if not updated_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return convert_asset_to_response(updated_asset)

@router.get("/statistics")
async def get_asset_statistics(db: Session = Depends(get_db)):
    """Get asset statistics by category and status"""
    return {
        "by_category": asset_service.get_assets_by_category(),
        "by_status": asset_service.get_assets_by_status(),
        "category_summary": asset_service.get_category_summary()
    }

@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str,
    asset_update: AssetCreate,
    db: Session = Depends(get_db)
):
    """Update an existing asset"""
    try:
        # Find asset by asset_id (user-defined ID)
        asset = asset_service.get_asset_by_asset_id(asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        # Update asset data
        asset_data = asset_update.dict(exclude_unset=True)
        result = asset_service.update_asset(asset.id, asset_data)
        
        if result["success"]:
            return convert_asset_to_response(result["asset"])
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{asset_id}")
async def delete_asset(asset_id: str, db: Session = Depends(get_db)):
    """Delete an asset"""
    try:
        # Find asset by asset_id (user-defined ID)
        asset = asset_service.get_asset_by_asset_id(asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        result = asset_service.delete_asset(asset.id)
        if result["success"]:
            return {"message": "Asset deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
