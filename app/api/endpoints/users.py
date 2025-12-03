from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.user_service import UserService
from .. import schemas
from ..utils import convert_user_to_response

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.get("/", response_model=List[schemas.UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users with pagination"""
    users = user_service.get_all_users(skip=skip, limit=limit)
    return [convert_user_to_response(user, include_permissions=True) for user in users]

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/", response_model=schemas.UserResponse)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    result = user_service.create_user(user.dict())
    
    if result.get("success"):
        return convert_user_to_response(result["user"], include_permissions=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to create user")
        )

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int,
    user_update: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Update an existing user"""
    updated_user = user_service.update_user(user_id, user_update.dict())
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user