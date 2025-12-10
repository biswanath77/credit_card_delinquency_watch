"""
API Routes
Main application endpoints
"""

from fastapi import APIRouter, HTTPException, Query, Request
from typing import Optional
from ..models import (
    RiskSignal, CustomerScore, PortfolioSummary, ROIAnalysis, CustomerScoreRequest
)

# This router will be initialized in main.py with dependencies
router = APIRouter(tags=["risk-analysis"])


def create_routes():
    """
    Factory function to create routes with injected dependencies
    
    Args:
        risk_service: RiskScoringService instance
        intervention_service: InterventionService instance
        customer_service: CustomerService instance
    
    Returns:
        Configured APIRouter
    """
    
    @router.get("/portfolio-summary", response_model=PortfolioSummary)
    async def portfolio_summary(request: Request):
        """Get portfolio summary statistics"""
        risk_service = request.app.state.risk_service
        if risk_service is None:
            raise HTTPException(status_code=503, detail="Risk service not available")
        return risk_service.get_portfolio_summary()
    
    @router.get("/signals", response_model=list[RiskSignal])
    async def get_signals(request: Request):
        """Get all behavioral signals and their effectiveness"""
        risk_service = request.app.state.risk_service
        if risk_service is None:
            raise HTTPException(status_code=503, detail="Risk service not available")
        return risk_service.get_signal_effectiveness()
    
    @router.get("/feature-importance")
    async def get_feature_importance(request: Request, top: int = 10):
        """Get top predictive features from the trained model

        Accesses `request.app.state.model_trainer` which is initialized
        during startup. Returns a list of {'feature','importance'} dicts.
        """
        model_trainer = getattr(request.app.state, 'model_trainer', None)
        if model_trainer is None:
            raise HTTPException(status_code=503, detail="Model trainer not available (server still starting?)")

        try:
            df_top = model_trainer.get_top_features(n=top)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        # Convert DataFrame to list of dicts
        try:
            result = df_top.to_dict(orient='records')
        except Exception:
            # Fallback in case feature_importance is not a DataFrame
            result = df_top

        return {"top_features": result}
    
    @router.get("/risk-distribution")
    async def risk_distribution(request: Request):
        """Get risk score and tier distribution"""
        risk_service = request.app.state.risk_service
        if risk_service is None:
            raise HTTPException(status_code=503, detail="Risk service not available")
        return risk_service.get_risk_distribution()
    
    @router.post("/score-customer", response_model=CustomerScore)
    async def score_customer(request: Request, customer_data: dict):
        """Score a single customer based on behavioral data"""
        customer_service = request.app.state.customer_service
        if customer_service is None:
            raise HTTPException(status_code=503, detail="Customer service not available")
        try:
            return customer_service.score_customer(customer_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.get("/customers")
    async def get_customers(request: Request, tier: Optional[str] = None, limit: int = Query(20, le=100)):
        """Get customer list with scores"""
        customer_service = request.app.state.customer_service
        if customer_service is None:
            raise HTTPException(status_code=503, detail="Customer service not available")
        return customer_service.get_customers(tier=tier, limit=limit)
    
    @router.get("/intervention-roi", response_model=ROIAnalysis)
    async def intervention_roi(request: Request):
        """Get ROI analysis for intervention strategy"""
        intervention_service = request.app.state.intervention_service
        if intervention_service is None:
            raise HTTPException(status_code=503, detail="Intervention service not available")
        return intervention_service.calculate_roi()
    
    @router.get("/dashboard-stats")
    async def dashboard_stats(request: Request):
        """Get all stats for dashboard"""
        risk_service = request.app.state.risk_service
        intervention_service = request.app.state.intervention_service
        if risk_service is None or intervention_service is None:
            raise HTTPException(status_code=503, detail="Services not available")
        return {
            "portfolio": risk_service.get_portfolio_summary(),
            "roi": intervention_service.calculate_roi(),
            "top_signals": risk_service.get_signal_effectiveness()[:3]
        }
    
    return router
