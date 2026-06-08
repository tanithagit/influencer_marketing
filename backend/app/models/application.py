from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class ApplicationStatus(str, enum.Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"

class CampaignApplication(Base):
    __tablename__ = "campaign_applications"

    id               = Column(Integer, primary_key=True, index=True)
    campaign_id      = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    influencer_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    proposal_message = Column(Text, nullable=True)
    proposed_rate    = Column(Integer, nullable=True)
    status           = Column(Enum(ApplicationStatus), default=ApplicationStatus.pending)
    applied_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    campaign   = relationship("Campaign", back_populates="applications")
    influencer = relationship("User", back_populates="applications")