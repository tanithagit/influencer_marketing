from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class CampaignStatus(str, enum.Enum):
    draft     = "draft"
    active    = "active"
    paused    = "paused"
    completed = "completed"
    cancelled = "cancelled"

class Campaign(Base):
    __tablename__ = "campaigns"

    id           = Column(Integer, primary_key=True, index=True)
    brand_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    title        = Column(String, nullable=False)
    description  = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    budget       = Column(Float, nullable=False)
    niche        = Column(String, nullable=True)
    start_date   = Column(DateTime, nullable=False)
    end_date     = Column(DateTime, nullable=False)
    status       = Column(Enum(CampaignStatus), default=CampaignStatus.draft)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    brand        = relationship("User", back_populates="campaigns")
    applications = relationship("CampaignApplication", back_populates="campaign")
    deliverables = relationship("Deliverable", back_populates="campaign")
    payments     = relationship("Payment", back_populates="campaign")