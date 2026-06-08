from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_current_brand,
    get_current_influencer
)
from app.models.user import User
from app.models.application import ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse
)
from app.services.application_service import (
    apply_to_campaign,
    get_campaign_applications,
    get_influencer_applications,
    get_application_by_id,
    review_application
)

router = APIRouter(prefix="/api/applications", tags=["Applications"])


# ─── Influencer Routes ────────────────────────────────────────

@router.post(
    "/campaign/{campaign_id}",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def apply_campaign(
    campaign_id: int,
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return apply_to_campaign(db, current_user, campaign_id, application_data)


@router.get("/my-applications", response_model=List[ApplicationResponse])
def get_my_applications(
    current_user: User = Depends(get_current_influencer),
    db: Session = Depends(get_db)
):
    return get_influencer_applications(db, current_user.id)


# ─── Brand Routes ─────────────────────────────────────────────

@router.get(
    "/campaign/{campaign_id}",
    response_model=List[ApplicationResponse]
)
def list_campaign_applications(
    campaign_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return get_campaign_applications(db, campaign_id, current_user)


@router.put("/{application_id}/approve", response_model=ApplicationResponse)
def approve_application(
    application_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return review_application(
        db,
        application_id,
        ApplicationStatus.approved,
        current_user
    )


@router.put("/{application_id}/reject", response_model=ApplicationResponse)
def reject_application(
    application_id: int,
    current_user: User = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    return review_application(
        db,
        application_id,
        ApplicationStatus.rejected,
        current_user
    )


# ─── Shared Route ─────────────────────────────────────────────

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_application_by_id(db, application_id)