from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class SubscriptionPlan(str, enum.Enum):
    free    = "free"
    premium = "premium"  # for brands
    pro     = "pro"      # for influencers

class SubscriptionStatus(str, enum.Enum):
    active   = "active"
    inactive = "inactive"
    expired  = "expired"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id                    = Column(Integer, primary_key=True, index=True)
    user_id               = Column(Integer, ForeignKey("users.id"), unique=True)
    plan                  = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.free)
    status                = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.active)
    stripe_subscription_id = Column(String, nullable=True)
    created_at            = Column(DateTime, default=datetime.utcnow)
    expires_at            = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="subscription")