"""
Application initialization and configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

from .core import (
    prepare_data,
    ModelTrainer,
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_V1_PREFIX,
    CORS_ORIGINS,
)
from .api import create_routes
from .services import RiskScoringService, InterventionService, CustomerService


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        Configured FastAPI instance
    """
    
    # Initialize app
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Global state for models and data
    app.state.df = None
    app.state.signal_cols = None
    app.state.model_trainer = None
    app.state.risk_service = None
    app.state.intervention_service = None
    app.state.customer_service = None
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize models and data on app startup"""
        print("🚀 Starting up application...")
        
        # Load and prepare data
        app.state.df, app.state.signal_cols = prepare_data()
        print(f"✅ Data loaded: {len(app.state.df)} customers")
        
        # Train model
        app.state.model_trainer = ModelTrainer()
        app.state.model_trainer.train(app.state.df, app.state.signal_cols)
        print("✅ Model trained successfully")
        
        # Initialize services
        app.state.risk_service = RiskScoringService(app.state.df, app.state.signal_cols)
        app.state.intervention_service = InterventionService(app.state.df)
        app.state.customer_service = CustomerService(app.state.df, app.state.model_trainer)
        print("✅ Services initialized")
        
        # Mount frontend (project root / frontend)
        project_root = Path(__file__).resolve().parent.parent.parent
        frontend_path = project_root / "frontend"
        if frontend_path.exists():
            app.mount("/frontend", StaticFiles(directory=str(frontend_path)), name="frontend")
            print("✅ Frontend mounted")
    
    # Register API routes (routes will fetch services from app.state at request time)
    routes = create_routes()
    app.include_router(routes, prefix=API_V1_PREFIX)
    
    @app.get("/")
    async def root():
        """Serve the dashboard"""
        project_root = Path(__file__).resolve().parent.parent.parent
        frontend_path = project_root / "frontend" / "public" / "index.html"
        if frontend_path.exists():
            return FileResponse(frontend_path, media_type="text/html")
        return {"message": "Early Risk Signals API - Credit Card Delinquency System"}
    
    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "data_loaded": app.state.df is not None,
            "model_trained": app.state.model_trainer is not None
        }
    
    return app


# Create the application instance
app = create_app()
