"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class CustomerScoreRequest(BaseModel):
    """Customer data for risk scoring"""
    customer_id: str = Field(..., description="Unique customer identifier")
    utilisation_pct: float = Field(..., alias='Utilisation %')
    avg_payment_ratio: float = Field(..., alias='Avg Payment Ratio')
    min_due_paid_frequency: float = Field(..., alias='Min Due Paid Frequency')
    merchant_mix_index: float = Field(..., alias='Merchant Mix Index')
    cash_withdrawal_pct: float = Field(..., alias='Cash Withdrawal %')
    recent_spend_change_pct: float = Field(..., alias='Recent Spend Change %')
    
    class Config:
        populate_by_name = True


class RiskSignal(BaseModel):
    """Individual behavioral risk signal"""
    name: str
    code: str
    prevalence: int
    prevalence_pct: float
    delinquency_rate_when_present: float
    delinquency_rate_when_absent: float
    risk_lift: float


class CustomerScore(BaseModel):
    """Risk score for a customer"""
    customer_id: str
    risk_score: int
    risk_tier: str
    delinquency_probability: float
    triggered_signals: List[str]
    recommendations: List[str]
    confidence: float


class PortfolioSummary(BaseModel):
    """Portfolio-level statistics"""
    total_customers: int
    total_delinquent: int
    delinquency_rate: float
    tier_breakdown: Dict[str, int]
    high_risk: Dict[str, float]
    medium_risk: Dict[str, float]
    low_risk: Dict[str, float]


class ROIAnalysis(BaseModel):
    """Return on Investment analysis"""
    program_cost: Dict[str, float]
    prevented_defaults: float
    revenue_protected: float
    net_benefit: float
    roi_percentage: float
    per_dollar_yield: float
