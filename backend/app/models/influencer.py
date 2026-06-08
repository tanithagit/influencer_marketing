from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class InfluencerProfile(Base):
    __tablename__ = "influencer_profiles"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), unique=True)
    niche            = Column(String, nullable=True)
    bio              = Column(String, nullable=True)
    followers_count  = Column(Integer, default=0)
    engagement_rate  = Column(Float, default=0.0)
    portfolio_url    = Column(String, nullable=True)
    media_kit_url    = Column(String, nullable=True)
    instagram_handle = Column(String, nullable=True)
    youtube_channel  = Column(String, nullable=True)
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="influencer_profile")