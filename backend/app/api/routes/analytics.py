from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import (
    get_current_brand,
    get_current_influencer,
    get_current_admin
)
from app.models.user import User
from app.schemas.analytics import (
    BrandAnalytics,
    InfluencerAnalytics,
    CampaignPerformance
)
from app.services.analytics_service import (
    get_brand_analytics,
    get_campaign_performance,
    get_influencer_analytics
)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# ─── Brand Analytics ──────────────────────────────────────────

@router.get("/brand/dashboard", response_model=BrandAnalytics)
def brand_dashboard(
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return get_brand_analytics(db, current_user.id)


@router.get("/brand/campaign-performance", response_model=List[CampaignPerformance])
def campaign_performance(
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return get_campaign_performance(db, current_user.id)


# ─── Influencer Analytics ─────────────────────────────────────

@router.get("/influencer/dashboard", response_model=InfluencerAnalytics)
def influencer_dashboard(
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return get_influencer_analytics(db, current_user.id)


# ─── Admin Analytics ──────────────────────────────────────────

@router.get("/admin/overview")
def admin_overview(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from app.models.campaign import Campaign
    from app.models.application import CampaignApplication
    from app.models.payment import Payment
    from app.models.user import User as UserModel

    total_users      = db.query(UserModel).count()
    total_brands     = db.query(UserModel).filter(UserModel.role == "brand").count()
    total_influencers = db.query(UserModel).filter(UserModel.role == "influencer").count()
    total_campaigns  = db.query(Campaign).count()
    total_payments   = db.query(Payment).count()

    total_revenue = sum(
        p.amount for p in db.query(Payment).all()
        if str(p.payment_status) in ["released", "PaymentStatus.released"]
    )

    return {
        "total_users":        total_users,
        "total_brands":       total_brands,
        "total_influencers":  total_influencers,
        "total_campaigns":    total_campaigns,
        "total_payments":     total_payments,
        "total_revenue":      total_revenue
    }