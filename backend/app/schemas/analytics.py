from pydantic import BaseModel
from typing import List, Optional

class BrandAnalytics(BaseModel):
    # Campaign stats
    total_campaigns:      int
    active_campaigns:     int
    completed_campaigns:  int
    cancelled_campaigns:  int

    # Application stats
    total_applications:   int
    approved_applications: int
    rejected_applications: int
    pending_applications:  int

    # Payment stats
    total_budget_spent:   float
    total_payments_made:  int
    escrowed_amount:      float

    # Deliverable stats
    total_deliverables:   int
    approved_deliverables: int
    pending_deliverables:  int

class InfluencerAnalytics(BaseModel):
    # Application stats
    total_applications:   int
    approved_applications: int
    rejected_applications: int
    pending_applications:  int

    # Earnings stats
    total_earnings:       float
    pending_earnings:     float
    released_earnings:    float

    # Deliverable stats
    total_deliverables:        int
    approved_deliverables:     int
    rejected_deliverables:     int
    deliverable_success_rate:  float

class CampaignPerformance(BaseModel):
    campaign_id:    int
    campaign_title: str
    budget:         float
    applications:   int
    approved:       int
    deliverables:   int
    amount_paid:    float

    class Config:
        from_attributes = True