from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from app.models.influencer import InfluencerProfile
from app.models.user import User
from app.schemas.influencer import InfluencerProfileCreate, InfluencerProfileUpdate
import os
import shutil
import uuid

def get_or_create_profile(db: Session, user: User) -> InfluencerProfile:
    profile = db.query(InfluencerProfile).filter(
        InfluencerProfile.user_id == user.id
    ).first()

    if not profile:
        profile = InfluencerProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


def update_profile(
    db: Session,
    user: User,
    profile_data: InfluencerProfileUpdate
) -> InfluencerProfile:
    profile = get_or_create_profile(db, user)

    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


def upload_file(
    db: Session,
    user: User,
    file: UploadFile,
    file_type: str  # "portfolio" or "media_kit"
) -> InfluencerProfile:
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG images and PDF files are allowed"
        )

    # Create upload directory
    upload_dir = f"uploads/{file_type}s"
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = f"{upload_dir}/{filename}"

    # Save file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update profile
    profile = get_or_create_profile(db, user)
    url = f"/{filepath}"

    if file_type == "portfolio":
        profile.portfolio_url = url
    elif file_type == "media_kit":
        profile.media_kit_url = url

    db.commit()
    db.refresh(profile)
    return profile


def get_all_influencers(db: Session, skip: int = 0, limit: int = 20):
    return db.query(User).filter(
        User.role == "influencer",
        User.is_active == True
    ).offset(skip).limit(limit).all()