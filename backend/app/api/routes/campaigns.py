from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_current_brand,
    get_current_admin
)
from app.models.user import User
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse
)
from app.services.campaign_service import (
    create_campaign,
    get_all_active_campaigns,
    get_brand_campaigns,
    get_campaign_by_id,
    update_campaign,
    delete_campaign
)

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


# ─── Public / Influencer Routes ───────────────────────────────

@router.get("/", response_model=List[CampaignResponse])
def list_campaigns(
    skip: int = 0,
    limit: int = 20,
    niche: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_active_campaigns(db, skip, limit, niche)


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_campaign_by_id(db, campaign_id)


# ─── Brand Routes ─────────────────────────────────────────────

@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_new_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return create_campaign(db, current_user, campaign_data)


@router.get("/brand/my-campaigns", response_model=List[CampaignResponse])
def get_my_campaigns(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return get_brand_campaigns(db, current_user.id, skip, limit)


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_existing_campaign(
    campaign_id: int,
    update_data: CampaignUpdate,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return update_campaign(db, campaign_id, current_user, update_data)


@router.delete("/{campaign_id}")
def cancel_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return delete_campaign(db, campaign_id, current_user)


# ─── Admin Routes ─────────────────────────────────────────────

@router.get("/admin/all", response_model=List[CampaignResponse])
def admin_list_all_campaigns(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return db.query(__import__('app.models.campaign', fromlist=['Campaign']).Campaign)\
             .offset(skip).limit(limit).all()