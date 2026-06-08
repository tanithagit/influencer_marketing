from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.deliverable import DeliverableStatus

class DeliverableCreate(BaseModel):
    description: Optional[str] = None

class DeliverableResponse(BaseModel):
    id:            int
    campaign_id:   int
    influencer_id: int
    content_url:   str
    description:   Optional[str]
    submitted_at:  datetime
    reviewed_at:   Optional[datetime]
    status:        DeliverableStatus

    class Config:
        from_attributes = True

class DeliverableReview(BaseModel):
    status:  DeliverableStatus
    comment: Optional[str] = None