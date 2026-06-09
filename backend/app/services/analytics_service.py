from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.campaign import Campaign, CampaignStatus
from app.models.application import CampaignApplication, ApplicationStatus
from app.models.deliverable import Deliverable, DeliverableStatus
from app.models.payment import Payment, PaymentStatus
from app.models.user import User


# ─── Brand Analytics ──────────────────────────────────────────

def get_brand_analytics(db: Session, brand_id: int) -> dict:

    # ── Campaign Stats ──
    total_campaigns = db.query(Campaign).filter(
        Campaign.brand_id == brand_id
    ).count()

    active_campaigns = db.query(Campaign).filter(
        Campaign.brand_id == brand_id,
        Campaign.status == CampaignStatus.active
    ).count()

    completed_campaigns = db.query(Campaign).filter(
        Campaign.brand_id == brand_id,
        Campaign.status == CampaignStatus.completed
    ).count()

    cancelled_campaigns = db.query(Campaign).filter(
        Campaign.brand_id == brand_id,
        Campaign.status == CampaignStatus.cancelled
    ).count()

    # ── Get all campaign ids for this brand ──
    campaign_ids = [
        c.id for c in db.query(Campaign.id).filter(
            Campaign.brand_id == brand_id
        ).all()
    ]

    # ── Application Stats ──
    total_applications = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id.in_(campaign_ids)
    ).count()

    approved_applications = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id.in_(campaign_ids),
        CampaignApplication.status == ApplicationStatus.approved
    ).count()

    rejected_applications = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id.in_(campaign_ids),
        CampaignApplication.status == ApplicationStatus.rejected
    ).count()

    pending_applications = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id.in_(campaign_ids),
        CampaignApplication.status == ApplicationStatus.pending
    ).count()

    # ── Payment Stats ──
    payments = db.query(Payment).filter(
        Payment.campaign_id.in_(campaign_ids)
    ).all()

    total_budget_spent = sum(
        p.amount for p in payments
        if p.payment_status == PaymentStatus.released
    )

    escrowed_amount = sum(
        p.amount for p in payments
        if p.payment_status == PaymentStatus.escrowed
    )

    total_payments_made = len([
        p for p in payments
        if p.payment_status == PaymentStatus.released
    ])

    # ── Deliverable Stats ──
    total_deliverables = db.query(Deliverable).filter(
        Deliverable.campaign_id.in_(campaign_ids)
    ).count()

    approved_deliverables = db.query(Deliverable).filter(
        Deliverable.campaign_id.in_(campaign_ids),
        Deliverable.status == DeliverableStatus.approved
    ).count()

    pending_deliverables = db.query(Deliverable).filter(
        Deliverable.campaign_id.in_(campaign_ids),
        Deliverable.status == DeliverableStatus.pending_review
    ).count()

    return {
        "total_campaigns":        total_campaigns,
        "active_campaigns":       active_campaigns,
        "completed_campaigns":    completed_campaigns,
        "cancelled_campaigns":    cancelled_campaigns,
        "total_applications":     total_applications,
        "approved_applications":  approved_applications,
        "rejected_applications":  rejected_applications,
        "pending_applications":   pending_applications,
        "total_budget_spent":     total_budget_spent,
        "total_payments_made":    total_payments_made,
        "escrowed_amount":        escrowed_amount,
        "total_deliverables":     total_deliverables,
        "approved_deliverables":  approved_deliverables,
        "pending_deliverables":   pending_deliverables,
    }


# ─── Campaign Performance ─────────────────────────────────────

def get_campaign_performance(
    db: Session,
    brand_id: int
) -> list:
    campaigns = db.query(Campaign).filter(
        Campaign.brand_id == brand_id
    ).all()

    result = []
    for campaign in campaigns:
        applications = db.query(CampaignApplication).filter(
            CampaignApplication.campaign_id == campaign.id
        ).count()

        approved = db.query(CampaignApplication).filter(
            CampaignApplication.campaign_id == campaign.id,
            CampaignApplication.status == ApplicationStatus.approved
        ).count()

        deliverables = db.query(Deliverable).filter(
            Deliverable.campaign_id == campaign.id
        ).count()

        amount_paid = db.query(
            func.sum(Payment.amount)
        ).filter(
            Payment.campaign_id == campaign.id,
            Payment.payment_status == PaymentStatus.released
        ).scalar() or 0.0

        result.append({
            "campaign_id":    campaign.id,
            "campaign_title": campaign.title,
            "budget":         campaign.budget,
            "applications":   applications,
            "approved":       approved,
            "deliverables":   deliverables,
            "amount_paid":    amount_paid
        })

    return result


# ─── Influencer Analytics ─────────────────────────────────────

def get_influencer_analytics(
    db: Session,
    influencer_id: int
) -> dict:

    # ── Application Stats ──
    total_applications = db.query(CampaignApplication).filter(
        CampaignApplication.influencer_id == influencer_id
    ).count()

    approved_applications = db.query(CampaignApplication).filter(
        CampaignApplication.influencer_id == influencer_id,
        CampaignApplication.status == ApplicationStatus.approved
    ).count()

    rejected_applications = db.query(CampaignApplication).filter(
        CampaignApplication.influencer_id == influencer_id,
        CampaignApplication.status == ApplicationStatus.rejected
    ).count()

    pending_applications = db.query(CampaignApplication).filter(
        CampaignApplication.influencer_id == influencer_id,
        CampaignApplication.status == ApplicationStatus.pending
    ).count()

    # ── Earnings Stats ──
    payments = db.query(Payment).filter(
        Payment.influencer_id == influencer_id
    ).all()

    total_earnings = sum(
        p.amount for p in payments
    )

    released_earnings = sum(
        p.amount for p in payments
        if p.payment_status == PaymentStatus.released
    )

    pending_earnings = sum(
        p.amount for p in payments
        if p.payment_status == PaymentStatus.escrowed
    )

    # ── Deliverable Stats ──
    total_deliverables = db.query(Deliverable).filter(
        Deliverable.influencer_id == influencer_id
    ).count()

    approved_deliverables = db.query(Deliverable).filter(
        Deliverable.influencer_id == influencer_id,
        Deliverable.status == DeliverableStatus.approved
    ).count()

    rejected_deliverables = db.query(Deliverable).filter(
        Deliverable.influencer_id == influencer_id,
        Deliverable.status == DeliverableStatus.rejected
    ).count()

    # Calculate success rate
    success_rate = 0.0
    if total_deliverables > 0:
        success_rate = round(
            (approved_deliverables / total_deliverables) * 100, 2
        )

    return {
        "total_applications":      total_applications,
        "approved_applications":   approved_applications,
        "rejected_applications":   rejected_applications,
        "pending_applications":    pending_applications,
        "total_earnings":          total_earnings,
        "released_earnings":       released_earnings,
        "pending_earnings":        pending_earnings,
        "total_deliverables":      total_deliverables,
        "approved_deliverables":   approved_deliverables,
        "rejected_deliverables":   rejected_deliverables,
        "deliverable_success_rate": success_rate
    }