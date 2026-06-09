from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import (
    get_current_brand,
    get_current_influencer,
    get_current_user
)
from app.models.user import User
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentIntentResponse
)
from app.services.payment_service import (
    create_payment_intent,
    release_payment,
    get_campaign_payments,
    get_influencer_payments,
    get_payment_by_id
)

router = APIRouter(prefix="/api/payments", tags=["Payments"])


# ─── Brand Routes ─────────────────────────────────────────────

@router.post(
    "/create-intent",
    response_model=PaymentIntentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_escrow_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return create_payment_intent(
        db,
        current_user,
        payment_data.campaign_id,
        payment_data.influencer_id,
        payment_data.amount
    )


@router.put("/{payment_id}/release", response_model=PaymentResponse)
def release_escrow_payment(
    payment_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return release_payment(db, payment_id, current_user)


@router.get(
    "/campaign/{campaign_id}",
    response_model=List[PaymentResponse]
)
def list_campaign_payments(
    campaign_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return get_campaign_payments(db, campaign_id, current_user)


# ─── Influencer Routes ────────────────────────────────────────

@router.get("/my-earnings", response_model=List[PaymentResponse])
def get_my_earnings(
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return get_influencer_payments(db, current_user.id)


# ─── Shared Route ─────────────────────────────────────────────

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_payment_by_id(db, payment_id)