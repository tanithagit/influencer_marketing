from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum

class PaymentStatus(str, enum.Enum):
    pending   = "pending"
    escrowed  = "escrowed"
    released  = "released"
    refunded  = "refunded"
    failed    = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id                    = Column(Integer, primary_key=True, index=True)
    campaign_id           = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    influencer_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount                = Column(Float, nullable=False)
    payment_status        = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    transaction_reference = Column(String, nullable=True)
    stripe_payment_id     = Column(String, nullable=True)
    created_at            = Column(DateTime, default=datetime.utcnow)
    released_at           = Column(DateTime, nullable=True)

    # Relationships
    campaign   = relationship("Campaign", back_populates="payments")
    influencer = relationship("User", back_populates="payments")