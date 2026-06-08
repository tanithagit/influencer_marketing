from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    brand = "brand"
    influencer = "influencer"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name       = Column(String, nullable=False)
    role            = Column(Enum(UserRole), nullable=False)
    is_verified     = Column(Boolean, default=False)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime, default=datetime.utcnow)

    # Relationships
    influencer_profile = relationship("InfluencerProfile", back_populates="user", uselist=False)
    campaigns          = relationship("Campaign", back_populates="brand")
    applications       = relationship("CampaignApplication", back_populates="influencer")
    deliverables       = relationship("Deliverable", back_populates="influencer")
    payments           = relationship("Payment", back_populates="influencer")
    subscription       = relationship("Subscription", back_populates="user", uselist=False)