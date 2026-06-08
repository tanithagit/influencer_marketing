from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.campaign import CampaignStatus

class CampaignCreate(BaseModel):
    title:        str
    description:  Optional[str] = None
    requirements: Optional[str] = None
    budget:       float
    niche:        Optional[str] = None
    start_date:   datetime
    end_date:     datetime


class CampaignUpdate(BaseModel):
    title:        Optional[str] = None
    description:  Optional[str] = None
    requirements: Optional[str] = None
    budget:       Optional[float] = None
    niche:        Optional[str] = None
    start_date:   Optional[datetime] = None
    end_date:     Optional[datetime] = None

class CampaignResponse(BaseModel):
    id:           int
    brand_id:     int
    title:        str
    description:  Optional[str]
    requirements: Optional[str]
    budget:       float
    niche:        Optional[str]
    start_date:   datetime
    end_date:     datetime
    status:       CampaignStatus
    created_at:   datetime
    updated_at:   datetime

    class Config:
        from_attributes = True


class CampaignWithBrand(CampaignResponse):
    brand_name:  Optional[str] = None

    class Config:
        from_attributes = True
