from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.models.campaign import Campaign, CampaignStatus
from app.models.subscription import Subscription, SubscriptionPlan
from app.models.user import User
from app.schemas.campaign import CampaignCreate, CampaignUpdate


# ─── Helper ───────────────────────────────────────────────────

def now_utc():
    """Always returns timezone-aware UTC datetime"""
    return datetime.now(timezone.utc)

def make_aware(dt: datetime) -> datetime:
    """Convert naive datetime to UTC aware datetime"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


# ─── Subscription Limit Check ─────────────────────────────────

def check_campaign_limit(db: Session, brand_id: int):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == brand_id
    ).first()

    # Premium brands have unlimited campaigns
    if subscription and subscription.plan == SubscriptionPlan.premium:
        return

    # Free brands max 3 active campaigns
    active_count = db.query(Campaign).filter(
        Campaign.brand_id == brand_id,
        Campaign.status == CampaignStatus.active
    ).count()

    if active_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Free plan allows maximum 3 active campaigns. Upgrade to Premium."
        )


# ─── Create Campaign ──────────────────────────────────────────

def create_campaign(
    db: Session,
    brand: User,
    campaign_data: CampaignCreate
) -> Campaign:
    start = make_aware(campaign_data.start_date)
    end   = make_aware(campaign_data.end_date)
    now   = now_utc()

    # Validate dates
    if end <= start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )

    if end <= now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be in the future"
        )

    # Check subscription limit
    check_campaign_limit(db, brand.id)

    campaign = Campaign(
        brand_id=brand.id,
        title=campaign_data.title,
        description=campaign_data.description,
        requirements=campaign_data.requirements,
        budget=campaign_data.budget,
        niche=campaign_data.niche,
        start_date=start,
        end_date=end,
        status=CampaignStatus.active
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


# ─── Get Campaigns ────────────────────────────────────────────

def get_all_active_campaigns(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    niche: str = None
):
    query = db.query(Campaign).filter(
        Campaign.status == CampaignStatus.active,
        Campaign.end_date > now_utc()
    )

    if niche:
        query = query.filter(Campaign.niche.ilike(f"%{niche}%"))

    return query.offset(skip).limit(limit).all()


def get_brand_campaigns(
    db: Session,
    brand_id: int,
    skip: int = 0,
    limit: int = 20
):
    return db.query(Campaign).filter(
        Campaign.brand_id == brand_id
    ).offset(skip).limit(limit).all()


def get_campaign_by_id(db: Session, campaign_id: int) -> Campaign:
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return campaign


# ─── Update Campaign ──────────────────────────────────────────

def update_campaign(
    db: Session,
    campaign_id: int,
    brand: User,
    update_data: CampaignUpdate
) -> Campaign:
    campaign = get_campaign_by_id(db, campaign_id)

    if campaign.brand_id != brand.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own campaigns"
        )

    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(campaign, key, value)

    campaign.updated_at = now_utc()
    db.commit()
    db.refresh(campaign)
    return campaign


# ─── Delete Campaign ──────────────────────────────────────────

def delete_campaign(
    db: Session,
    campaign_id: int,
    brand: User
) -> dict:
    campaign = get_campaign_by_id(db, campaign_id)

    if campaign.brand_id != brand.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own campaigns"
        )

    campaign.status = CampaignStatus.cancelled
    db.commit()
    return {"message": "Campaign cancelled successfully"}