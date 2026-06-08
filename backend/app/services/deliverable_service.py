from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from datetime import datetime, timezone
from app.models.deliverable import Deliverable, DeliverableStatus
from app.models.application import CampaignApplication, ApplicationStatus
from app.models.campaign import Campaign
from app.models.user import User
import os
import shutil
import uuid


def now_utc():
    return datetime.now(timezone.utc)


# ─── Submit Deliverable ───────────────────────────────────────

def submit_deliverable(
    db: Session,
    influencer: User,
    campaign_id: int,
    file: UploadFile,
    description: str = None
) -> Deliverable:

    # Check campaign exists
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Check influencer has approved application
    application = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id == campaign_id,
        CampaignApplication.influencer_id == influencer.id,
        CampaignApplication.status == ApplicationStatus.approved
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must have an approved application to submit deliverables"
        )

    # Validate file type
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "video/mp4",
        "application/pdf"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, MP4 and PDF files are allowed"
        )

    # Save file
    upload_dir = "uploads/deliverables"
    os.makedirs(upload_dir, exist_ok=True)

    ext      = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = f"{upload_dir}/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create deliverable
    deliverable = Deliverable(
        campaign_id=campaign_id,
        influencer_id=influencer.id,
        content_url=f"/{filepath}",
        description=description,
        status=DeliverableStatus.pending_review
    )

    db.add(deliverable)
    db.commit()
    db.refresh(deliverable)
    return deliverable


# ─── Get Deliverables ─────────────────────────────────────────

def get_campaign_deliverables(
    db: Session,
    campaign_id: int,
    brand: User
):
    # Verify brand owns campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.brand_id == brand.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found or you don't own it"
        )

    return db.query(Deliverable).filter(
        Deliverable.campaign_id == campaign_id
    ).all()


def get_influencer_deliverables(
    db: Session,
    influencer_id: int
):
    return db.query(Deliverable).filter(
        Deliverable.influencer_id == influencer_id
    ).all()


def get_deliverable_by_id(
    db: Session,
    deliverable_id: int
) -> Deliverable:
    deliverable = db.query(Deliverable).filter(
        Deliverable.id == deliverable_id
    ).first()

    if not deliverable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverable not found"
        )
    return deliverable


# ─── Review Deliverable ───────────────────────────────────────

def review_deliverable(
    db: Session,
    deliverable_id: int,
    new_status: DeliverableStatus,
    brand: User
) -> Deliverable:

    deliverable = get_deliverable_by_id(db, deliverable_id)

    # Verify brand owns the campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == deliverable.campaign_id,
        Campaign.brand_id == brand.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this campaign"
        )

    # Can only review pending deliverables
    if deliverable.status != DeliverableStatus.pending_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deliverable is already {deliverable.status}"
        )

    deliverable.status      = new_status
    deliverable.reviewed_at = now_utc()

    db.commit()
    db.refresh(deliverable)
    return deliverable