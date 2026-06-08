from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.application import ApplicationStatus

class ApplicationCreate(BaseModel):
    proposal_message: Optional[str] = None
    proposed_rate:    Optional[int] = None

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationResponse(BaseModel):
    id:               int
    campaign_id:      int
    influencer_id:    int
    proposal_message: Optional[str]
    proposed_rate:    Optional[int]
    status:           ApplicationStatus
    applied_at:       datetime
    updated_at:       datetime

    class Config:
        from_attributes = True

class ApplicationWithDetails(ApplicationResponse):
    influencer_name:  Optional[str] = None
    campaign_title:   Optional[str] = None

    class Config:
        from_attributes = True