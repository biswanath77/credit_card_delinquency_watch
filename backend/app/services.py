"""
Service Layer for Business Logic
Handles core business operations and calculations
"""

import pandas as pd
from typing import List, Dict, Tuple
from .core.config import (
    RISK_HIGH_THRESHOLD,
    RISK_MEDIUM_THRESHOLD,
    HIGH_INTERVENTION_COST,
    MEDIUM_INTERVENTION_COST,
    LOW_INTERVENTION_COST,
    AVG_LOSS_PER_DEFAULT,
    HIGH_PREVENTION_RATE,
    MEDIUM_PREVENTION_RATE,
    LOW_PREVENTION_RATE
)


class RiskScoringService:
    """Handle risk scoring and analysis"""
    
    def __init__(self, df: pd.DataFrame, signal_cols: List[str]):
        """
        Initialize with prepared data
        
        Args:
            df: DataFrame with engineered features
            signal_cols: List of signal column names
        """
        self.df = df
        self.signal_cols = signal_cols
    
    def get_portfolio_summary(self) -> Dict:
        """Get portfolio-level summary statistics"""
        total_customers = len(self.df)
        total_delinquent = (self.df['is_delinquent'] == 1).sum()
        delinquency_rate = (total_delinquent / total_customers * 100)
        
        tier_breakdown = self.df['risk_tier'].value_counts().to_dict()
        
        result = {
            "total_customers": int(total_customers),
            "total_delinquent": int(total_delinquent),
            "delinquency_rate": round(delinquency_rate, 2),
            "tier_breakdown": {
                "HIGH": int(tier_breakdown.get('HIGH', 0)),
                "MEDIUM": int(tier_breakdown.get('MEDIUM', 0)),
                "LOW": int(tier_breakdown.get('LOW', 0))
            }
        }
        
        # Add tier-specific metrics
        for tier in ['HIGH', 'MEDIUM', 'LOW']:
            tier_data = self.df[self.df['risk_tier'] == tier]
            result[f"{tier.lower()}_risk"] = {
                "count": int(len(tier_data)),
                "delinquency_rate": round(tier_data['is_delinquent'].mean() * 100, 1)
            }
        
        return result
    
    def get_signal_effectiveness(self) -> List[Dict]:
        """Analyze effectiveness of each behavioral signal"""
        signals_data = []
        
        for signal in self.signal_cols:
            flagged = self.df[self.df[signal] == 1]
            unflagged = self.df[self.df[signal] == 0]
            
            flag_del_rate = flagged['is_delinquent'].mean() * 100 if len(flagged) > 0 else 0
            unflag_del_rate = unflagged['is_delinquent'].mean() * 100
            lift = flag_del_rate / unflag_del_rate if unflag_del_rate > 0 else 1
            
            signals_data.append({
                "name": signal.replace('signal_', '').replace('_', ' ').title(),
                "code": signal,
                "prevalence": int(self.df[signal].sum()),
                "prevalence_pct": round(self.df[signal].sum() / len(self.df) * 100, 1),
                "delinquency_rate_when_present": round(flag_del_rate, 1),
                "delinquency_rate_when_absent": round(unflag_del_rate, 1),
                "risk_lift": round(lift, 2)
            })
        
        return sorted(signals_data, key=lambda x: x['risk_lift'], reverse=True)
    
    def get_risk_distribution(self) -> Dict:
        """Get risk score and tier distribution"""
        risk_score_dist = self.df['risk_score'].value_counts().sort_index().to_dict()
        
        tier_dist = []
        for tier in ['HIGH', 'MEDIUM', 'LOW']:
            tier_data = self.df[self.df['risk_tier'] == tier]
            tier_dist.append({
                "tier": tier,
                "count": int(len(tier_data)),
                "percentage": round(len(tier_data) / len(self.df) * 100, 1),
                "delinquency_rate": round(tier_data['is_delinquent'].mean() * 100, 1),
                "avg_utilization": round(tier_data['Utilisation %'].mean(), 1),
                "avg_payment_ratio": round(tier_data['Avg Payment Ratio'].mean(), 1),
                "avg_spend_change": round(tier_data['Recent Spend Change %'].mean(), 1),
                "avg_cash_withdrawal": round(tier_data['Cash Withdrawal %'].mean(), 1)
            })
        
        return {
            "risk_score_distribution": risk_score_dist,
            "tier_distribution": tier_dist
        }


class InterventionService:
    """Calculate intervention costs and ROI"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with data"""
        self.df = df
    
    def calculate_roi(self) -> Dict:
        """Calculate ROI for intervention strategy"""
        high_tier = self.df[self.df['risk_tier'] == 'HIGH']
        medium_tier = self.df[self.df['risk_tier'] == 'MEDIUM']
        low_tier = self.df[self.df['risk_tier'] == 'LOW']
        
        # Calculate prevented defaults
        high_prevented = (
            len(high_tier) * HIGH_PREVENTION_RATE * 
            (high_tier['is_delinquent'].mean())
        )
        medium_prevented = (
            len(medium_tier) * MEDIUM_PREVENTION_RATE * 
            (medium_tier['is_delinquent'].mean())
        )
        low_prevented = (
            len(low_tier) * LOW_PREVENTION_RATE * 
            (low_tier['is_delinquent'].mean())
        )
        total_prevented = high_prevented + medium_prevented + low_prevented
        
        # Cost calculation
        high_cost = len(high_tier) * HIGH_INTERVENTION_COST
        medium_cost = len(medium_tier) * MEDIUM_INTERVENTION_COST
        low_cost = len(low_tier) * LOW_INTERVENTION_COST
        total_cost = high_cost + medium_cost + low_cost
        
        # Revenue impact
        revenue_impact = total_prevented * AVG_LOSS_PER_DEFAULT
        roi = (revenue_impact - total_cost) / total_cost * 100 if total_cost > 0 else 0
        
        return {
            "program_cost": {
                "high_tier": float(high_cost),
                "medium_tier": float(medium_cost),
                "low_tier": float(low_cost),
                "total": float(total_cost)
            },
            "prevented_defaults": round(total_prevented, 1),
            "revenue_protected": float(revenue_impact),
            "net_benefit": float(revenue_impact - total_cost),
            "roi_percentage": round(roi, 1),
            "per_dollar_yield": round(revenue_impact / total_cost, 2) if total_cost > 0 else 0
        }
    
    def get_intervention_recommendations(self, risk_tier: str) -> List[str]:
        """Get intervention recommendations for a risk tier"""
        recommendations = {
            'HIGH': [
                'Direct phone outreach within 24-48 hours',
                'Offer payment plan or credit limit review',
                'Connect with financial counselor',
                'Monitor weekly for 3 months'
            ],
            'MEDIUM': [
                'Automated email with account health summary',
                'Offer payment flexibility or rate reduction',
                'Push financial wellness resources',
                'Monitor monthly for 2 months'
            ],
            'LOW': [
                'Educational email campaign',
                'Highlight available resources',
                'Quarterly monitoring',
                'Standard customer service'
            ]
        }
        return recommendations.get(risk_tier, [])


class CustomerService:
    """Manage customer data and queries"""
    
    def __init__(self, df: pd.DataFrame, model_trainer):
        """
        Initialize with data and model
        
        Args:
            df: DataFrame with customer data
            model_trainer: Trained ModelTrainer instance
        """
        self.df = df
        self.model_trainer = model_trainer
    
    def score_customer(self, customer_data: Dict) -> Dict:
        """
        Score a single customer
        
        Args:
            customer_data: Dictionary with customer features
        
        Returns:
            Risk score and recommendations
        """
        # Build feature vector
        customer_features = [
            customer_data['Utilisation %'],
            customer_data['Avg Payment Ratio'],
            customer_data['Min Due Paid Frequency'],
            customer_data['Merchant Mix Index'],
            customer_data['Cash Withdrawal %'],
            customer_data['Recent Spend Change %'],
            int(customer_data.get('signal_spend_decline', 0)),
            int(customer_data.get('signal_high_utilization', 0)),
            int(customer_data.get('signal_payment_decline', 0)),
            int(customer_data.get('signal_cash_surge', 0)),
            int(customer_data.get('signal_low_merchant_mix', 0))
        ]
        
        # Get probability
        probability = self.model_trainer.predict_proba(customer_features)
        
        # Calculate risk score
        risk_score = sum([
            customer_data.get('signal_spend_decline', 0),
            customer_data.get('signal_high_utilization', 0),
            customer_data.get('signal_payment_decline', 0),
            customer_data.get('signal_cash_surge', 0),
            customer_data.get('signal_low_merchant_mix', 0)
        ])
        
        # Classify tier
        if risk_score >= RISK_HIGH_THRESHOLD:
            risk_tier = 'HIGH'
        elif risk_score >= RISK_MEDIUM_THRESHOLD:
            risk_tier = 'MEDIUM'
        else:
            risk_tier = 'LOW'
        
        # Get recommendations
        intervention_service = InterventionService(self.df)
        recommendations = intervention_service.get_intervention_recommendations(risk_tier)
        
        # Identify signals
        triggered_signals = []
        if customer_data.get('signal_spend_decline'):
            triggered_signals.append('Spending Decline')
        if customer_data.get('signal_high_utilization'):
            triggered_signals.append('High Utilization')
        if customer_data.get('signal_payment_decline'):
            triggered_signals.append('Payment Decline')
        if customer_data.get('signal_cash_surge'):
            triggered_signals.append('Cash Surge')
        if customer_data.get('signal_low_merchant_mix'):
            triggered_signals.append('Low Merchant Mix')
        
        return {
            "customer_id": customer_data.get('customer_id', 'UNKNOWN'),
            "risk_score": int(risk_score),
            "risk_tier": risk_tier,
            "delinquency_probability": round(probability, 3),
            "triggered_signals": triggered_signals,
            "recommendations": recommendations,
            "confidence": round(abs(probability - 0.5) * 2, 3)
        }
    
    def get_customers(self, tier: str = None, limit: int = 20) -> List[Dict]:
        """Get customer list with scores"""
        data = self.df.copy()
        
        if tier:
            data = data[data['risk_tier'] == tier]
        
        customers = []
        for _, row in data.head(limit).iterrows():
            customers.append({
                "customer_id": row['Customer ID'],
                "risk_tier": row['risk_tier'],
                "risk_score": int(row['risk_score']),
                "utilization": round(row['Utilisation %'], 1),
                "payment_ratio": round(row['Avg Payment Ratio'], 1),
                "spend_change": round(row['Recent Spend Change %'], 1),
                "is_delinquent": bool(row['is_delinquent']),
                "credit_limit": int(row['Credit Limit'])
            })
        
        return customers
