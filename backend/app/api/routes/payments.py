from fastapi import APIRouter, Depends, status, BackgroundTasks
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
from app.services.email_service import send_payment_released_email

router = APIRouter(prefix="/api/payments", tags=["Payments"])


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
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    payment = release_payment(db, payment_id, current_user)

    # Send email to influencer
    influencer = db.query(User).filter(
        User.id == payment.influencer_id
    ).first()
    campaign = db.query(
        __import__('app.models.campaign', fromlist=['Campaign']).Campaign
    ).filter_by(id=payment.campaign_id).first()

    if influencer and campaign:
        background_tasks.add_task(
            send_payment_released_email,
            influencer.email,
            influencer.full_name,
            campaign.title,
            payment.amount
        )
    return payment


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


@router.get("/my-earnings", response_model=List[PaymentResponse])
def get_my_earnings(
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return get_influencer_payments(db, current_user.id)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_payment_by_id(db, payment_id)