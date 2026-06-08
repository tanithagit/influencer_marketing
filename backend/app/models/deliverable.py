from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class DeliverableStatus(str, enum.Enum):
    pending_review = "pending_review"
    approved       = "approved"
    rejected       = "rejected"

class Deliverable(Base):
    __tablename__ = "deliverables"

    id            = Column(Integer, primary_key=True, index=True)
    campaign_id   = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    influencer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_url   = Column(String, nullable=False)
    description   = Column(Text, nullable=True)
    submitted_at  = Column(DateTime, default=datetime.utcnow)
    reviewed_at   = Column(DateTime, nullable=True)
    status        = Column(Enum(DeliverableStatus), default=DeliverableStatus.pending_review)

    # Relationships
    campaign   = relationship("Campaign", back_populates="deliverables")
    influencer = relationship("User", back_populates="deliverables")