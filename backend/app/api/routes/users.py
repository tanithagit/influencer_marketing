from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_current_influencer,
    get_current_admin
)
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.influencer import (
    InfluencerProfileCreate,
    InfluencerProfileUpdate,
    InfluencerProfileResponse
)
from app.services.influencer_service import (
    get_or_create_profile,
    update_profile,
    upload_file,
    get_all_influencers
)

router = APIRouter(prefix="/api/users", tags=["Users"])


# ─── Current User ────────────────────────────────────────────

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user


# ─── Influencer Profile ───────────────────────────────────────

@router.get("/influencer/profile", response_model=InfluencerProfileResponse)
def get_influencer_profile(
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return get_or_create_profile(db, current_user)


@router.put("/influencer/profile", response_model=InfluencerProfileResponse)
def update_influencer_profile(
    profile_data: InfluencerProfileUpdate,
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return update_profile(db, current_user, profile_data)


# ─── File Uploads ─────────────────────────────────────────────

@router.post("/influencer/upload/portfolio", response_model=InfluencerProfileResponse)
def upload_portfolio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return upload_file(db, current_user, file, "portfolio")


@router.post("/influencer/upload/media-kit", response_model=InfluencerProfileResponse)
def upload_media_kit(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return upload_file(db, current_user, file, "media_kit")


# ─── Admin Routes ─────────────────────────────────────────────

@router.get("/all-influencers", response_model=List[UserResponse])
def list_all_influencers(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return get_all_influencers(db, skip, limit)


@router.put("/admin/verify/{user_id}", response_model=UserResponse)
def verify_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user


@router.put("/admin/deactivate/{user_id}", response_model=UserResponse)
def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user