from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InfluencerProfileCreate(BaseModel):
    niche:            Optional[str] = None
    bio:              Optional[str] = None
    followers_count:  Optional[int] = 0
    engagement_rate:  Optional[float] = 0.0
    instagram_handle: Optional[str] = None
    youtube_channel:  Optional[str] = None

class InfluencerProfileUpdate(BaseModel):
    niche:            Optional[str] = None
    bio:              Optional[str] = None
    followers_count:  Optional[int] = None
    engagement_rate:  Optional[float] = None
    instagram_handle: Optional[str] = None
    youtube_channel:  Optional[str] = None

class InfluencerProfileResponse(BaseModel):
    id:               int
    user_id:          int
    niche:            Optional[str]
    bio:              Optional[str]
    followers_count:  int
    engagement_rate:  float
    portfolio_url:    Optional[str]
    media_kit_url:    Optional[str]
    instagram_handle: Optional[str]
    youtube_channel:  Optional[str]
    created_at:       datetime

    class Config:
        from_attributes = True

class InfluencerWithUser(BaseModel):
    id:          int
    email:       str
    full_name:   str
    is_verified: bool
    profile:     Optional[InfluencerProfileResponse]

    class Config:
        from_attributes = True