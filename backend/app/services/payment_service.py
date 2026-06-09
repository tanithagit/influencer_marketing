from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
import stripe
import uuid
from app.models.payment import Payment, PaymentStatus
from app.models.deliverable import Deliverable, DeliverableStatus
from app.models.campaign import Campaign
from app.models.application import CampaignApplication, ApplicationStatus
from app.models.user import User
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def now_utc():
    return datetime.now(timezone.utc)


# ─── Create Escrow Payment ────────────────────────────────────

def create_payment_intent(
    db: Session,
    brand: User,
    campaign_id: int,
    influencer_id: int,
    amount: float
) -> dict:

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

    # Verify influencer has approved application
    application = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id == campaign_id,
        CampaignApplication.influencer_id == influencer_id,
        CampaignApplication.status == ApplicationStatus.approved
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Influencer does not have an approved application"
        )

    # Check no duplicate payment
    existing = db.query(Payment).filter(
        Payment.campaign_id == campaign_id,
        Payment.influencer_id == influencer_id,
        Payment.payment_status.in_([
            PaymentStatus.escrowed,
            PaymentStatus.released
        ])
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already exists for this collaboration"
        )

    try:
        # Create Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe uses cents
            currency="usd",
            metadata={
                "campaign_id":   str(campaign_id),
                "influencer_id": str(influencer_id),
                "brand_id":      str(brand.id)
            }
        )

        # Save payment record
        payment = Payment(
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            amount=amount,
            payment_status=PaymentStatus.escrowed,
            stripe_payment_id=intent.id,
            transaction_reference=str(uuid.uuid4())
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return {
            "client_secret": intent.client_secret,
            "payment_id":    payment.id,
            "amount":        amount,
            "currency":      "usd"
        }

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )


# ─── Release Payment ──────────────────────────────────────────

def release_payment(
    db: Session,
    payment_id: int,
    brand: User
) -> Payment:

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    # Verify brand owns the campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == payment.campaign_id,
        Campaign.brand_id == brand.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this campaign"
        )

    # CRITICAL: Check deliverable is approved before releasing
    approved_deliverable = db.query(Deliverable).filter(
        Deliverable.campaign_id == payment.campaign_id,
        Deliverable.influencer_id == payment.influencer_id,
        Deliverable.status == DeliverableStatus.approved
    ).first()

    if not approved_deliverable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot release payment — deliverable not approved yet"
        )

    # Check payment is in escrow
    if payment.payment_status != PaymentStatus.escrowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment cannot be released — status is {payment.payment_status}"
        )

    # Update payment status
    payment.payment_status = PaymentStatus.released
    payment.released_at    = now_utc()

    db.commit()
    db.refresh(payment)
    return payment


# ─── Get Payments ─────────────────────────────────────────────

def get_campaign_payments(
    db: Session,
    campaign_id: int,
    brand: User
):
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.brand_id == brand.id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found or you don't own it"
        )

    return db.query(Payment).filter(
        Payment.campaign_id == campaign_id
    ).all()


def get_influencer_payments(
    db: Session,
    influencer_id: int
):
    return db.query(Payment).filter(
        Payment.influencer_id == influencer_id
    ).all()


def get_payment_by_id(
    db: Session,
    payment_id: int
) -> Payment:
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment