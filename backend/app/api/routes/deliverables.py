from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_current_brand,
    get_current_influencer
)
from app.models.user import User
from app.models.deliverable import DeliverableStatus
from app.schemas.deliverable import DeliverableResponse, DeliverableReview
from app.services.deliverable_service import (
    submit_deliverable,
    get_campaign_deliverables,
    get_influencer_deliverables,
    get_deliverable_by_id,
    review_deliverable
)

router = APIRouter(prefix="/api/deliverables", tags=["Deliverables"])


# ─── Influencer Routes ────────────────────────────────────────

@router.post(
    "/campaign/{campaign_id}",
    response_model=DeliverableResponse,
    status_code=status.HTTP_201_CREATED
)
def submit_campaign_deliverable(
    campaign_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return submit_deliverable(
        db,
        current_user,
        campaign_id,
        file,
        description
    )


@router.get("/my-deliverables", response_model=List[DeliverableResponse])
def get_my_deliverables(
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return get_influencer_deliverables(db, current_user.id)


# ─── Brand Routes ─────────────────────────────────────────────

@router.get(
    "/campaign/{campaign_id}",
    response_model=List[DeliverableResponse]
)
def list_campaign_deliverables(
    campaign_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return get_campaign_deliverables(db, campaign_id, current_user)


@router.put("/{deliverable_id}/approve", response_model=DeliverableResponse)
def approve_deliverable(
    deliverable_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return review_deliverable(
        db,
        deliverable_id,
        DeliverableStatus.approved,
        current_user
    )


@router.put("/{deliverable_id}/reject", response_model=DeliverableResponse)
def reject_deliverable(
    deliverable_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return review_deliverable(
        db,
        deliverable_id,
        DeliverableStatus.rejected,
        current_user
    )


# ─── Shared Route ─────────────────────────────────────────────

@router.get("/{deliverable_id}", response_model=DeliverableResponse)
def get_deliverable(
    deliverable_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_deliverable_by_id(db, deliverable_id)