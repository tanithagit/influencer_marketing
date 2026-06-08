from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.models.application import CampaignApplication, ApplicationStatus
from app.models.campaign import Campaign, CampaignStatus
from app.models.subscription import Subscription, SubscriptionPlan
from app.models.user import User
from app.schemas.application import ApplicationCreate


def now_utc():
    return datetime.now(timezone.utc)

def make_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


# ─── Subscription Limit Check ─────────────────────────────────

def check_application_limit(db: Session, influencer_id: int):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == influencer_id
    ).first()

    # Pro influencers have unlimited applications
    if subscription and subscription.plan == SubscriptionPlan.pro:
        return

    # Free influencers max 10 applications per month
    from datetime import timedelta
    month_start = now_utc().replace(day=1, hour=0, minute=0, second=0)

    monthly_count = db.query(CampaignApplication).filter(
        CampaignApplication.influencer_id == influencer_id,
        CampaignApplication.applied_at >= month_start
    ).count()

    if monthly_count >= 10:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Free plan allows maximum 10 applications per month. Upgrade to Pro."
        )


# ─── Apply to Campaign ────────────────────────────────────────

def apply_to_campaign(
    db: Session,
    influencer: User,
    campaign_id: int,
    application_data: ApplicationCreate
) -> CampaignApplication:

    # Check campaign exists
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # Check campaign is active
    if campaign.status != CampaignStatus.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign is not active"
        )

    # Check campaign has not ended
    campaign_end = make_aware(campaign.end_date)
    if campaign_end <= now_utc():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign has already ended"
        )

    # Check duplicate application
    existing = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id == campaign_id,
        CampaignApplication.influencer_id == influencer.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied to this campaign"
        )

    # Check subscription limit
    check_application_limit(db, influencer.id)

    # Create application
    application = CampaignApplication(
        campaign_id=campaign_id,
        influencer_id=influencer.id,
        proposal_message=application_data.proposal_message,
        proposed_rate=application_data.proposed_rate,
        status=ApplicationStatus.pending
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


# ─── Get Applications ─────────────────────────────────────────

def get_campaign_applications(
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

    return db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id == campaign_id
    ).all()


def get_influencer_applications(
    db: Session,
    influencer_id: int
):
    return db.query(CampaignApplication).filter(
        CampaignApplication.influencer_id == influencer_id
    ).all()


def get_application_by_id(
    db: Session,
    application_id: int
) -> CampaignApplication:
    application = db.query(CampaignApplication).filter(
        CampaignApplication.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return application


# ─── Review Application ───────────────────────────────────────

def review_application(
    db: Session,
    application_id: int,
    new_status: ApplicationStatus,
    brand: User
) -> CampaignApplication:

    application = get_application_by_id(db, application_id)

    # Verify brand owns the campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == application.campaign_id,
        Campaign.brand_id == brand.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this campaign"
        )

    # Can only review pending applications
    if application.status != ApplicationStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Application is already {application.status}"
        )

    application.status     = new_status
    application.updated_at = now_utc()

    db.commit()
    db.refresh(application)
    return application