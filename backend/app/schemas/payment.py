from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentStatus

class PaymentCreate(BaseModel):
    campaign_id:   int
    influencer_id: int
    amount:        float

class PaymentResponse(BaseModel):
    id:                    int
    campaign_id:           int
    influencer_id:         int
    amount:                float
    payment_status:        PaymentStatus
    transaction_reference: Optional[str]
    stripe_payment_id:     Optional[str]
    created_at:            datetime
    released_at:           Optional[datetime]

    class Config:
        from_attributes = True

class PaymentIntentResponse(BaseModel):
    client_secret:  str
    payment_id:     int
    amount:         float
    currency:       str