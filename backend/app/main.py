"""
Application initialization and configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import traceback
import os

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

# Project and frontend public folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_PUBLIC = PROJECT_ROOT / "frontend" / "public"


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION
    )

    # CORS middleware - ensure list type
    allow_origins = CORS_ORIGINS if isinstance(CORS_ORIGINS, (list, tuple)) else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static frontend files at /static (so /static/style.css and /static/app.js work)
    if FRONTEND_PUBLIC.exists():
        app.mount("/static", StaticFiles(directory=str(FRONTEND_PUBLIC)), name="static")
        print(f"✅ Mounted static frontend: /static -> {FRONTEND_PUBLIC}")
    else:
        # fallback to frontend directory if public missing
        alt_frontend = PROJECT_ROOT / "frontend"
        if alt_frontend.exists():
            app.mount("/static", StaticFiles(directory=str(alt_frontend)), name="static")
            print(f"✅ Mounted static frontend (fallback): /static -> {alt_frontend}")
        else:
            print("⚠️ Frontend public folder not found. Static files won't be served from /static.")

    # Application state placeholders
    app.state.df = None
    app.state.signal_cols = None
    app.state.model_trainer = None
    app.state.risk_service = None
    app.state.intervention_service = None
    app.state.customer_service = None

    @app.on_event("startup")
    async def startup_event():
        """Initialize models and data on app startup (safe defaults)"""
        print("🚀 Starting application (startup_event) ...")

        # Load & prepare data (safe)
        try:
            df, signal_cols = prepare_data()
            app.state.df = df
            app.state.signal_cols = signal_cols
            print(f"✅ Data loaded: {len(df)} customers")
        except Exception:
            print("❌ Failed to prepare data on startup:")
            traceback.print_exc()
            app.state.df = None
            app.state.signal_cols = None

        # Model init: try to load pre-trained model; do NOT train by default in deployment
        try:
            trainer = ModelTrainer()
            model_loaded = False

            try:
                # Optional MODELS_DIR import if present in core/config
                from .core import MODELS_DIR
                candidate = Path(MODELS_DIR) / "rf_3class_model.joblib"
                if candidate.exists():
                    try:
                        trainer.load(str(candidate))
                        model_loaded = True
                        print(f"✅ Loaded model from {candidate}")
                    except Exception:
                        print("⚠️ Model found but failed to load:")
                        traceback.print_exc()
            except Exception:
                # MODELS_DIR not available or load not needed
                pass

            # Only train at startup if explicitly allowed (use env var to avoid slow startup)
            if not model_loaded:
                allow_training = os.getenv("ALLOW_STARTUP_TRAINING", "false").lower() in ("1", "true", "yes")
                if allow_training and app.state.df is not None and app.state.signal_cols is not None:
                    print("🔔 ALLOW_STARTUP_TRAINING enabled — training model at startup...")
                    trainer.train(app.state.df, app.state.signal_cols)
                    try:
                        from .core import MODELS_DIR
                        save_path = Path(MODELS_DIR) / "rf_3class_model.joblib"
                        trainer.save(save_path)
                        print(f"✅ Model trained and saved to {save_path}")
                    except Exception:
                        print("⚠️ Model trained but could not be saved (check MODELS_DIR).")
                        traceback.print_exc()
                else:
                    print("ℹ️ No pre-trained model loaded and startup training disabled.")
            app.state.model_trainer = trainer
        except Exception:
            print("❌ Model initialization failed during startup:")
            traceback.print_exc()
            app.state.model_trainer = None

        # Initialize services (should handle missing data/model gracefully)
        try:
            app.state.risk_service = RiskScoringService(app.state.df, app.state.signal_cols)
            app.state.intervention_service = InterventionService(app.state.df)
            app.state.customer_service = CustomerService(app.state.df, app.state.model_trainer)
            print("✅ Services initialized")
        except Exception:
            print("⚠️ Failed to initialize one or more services:")
            traceback.print_exc()

    # Register API routes
    routes = create_routes()
    app.include_router(routes, prefix=API_V1_PREFIX)

    @app.get("/", include_in_schema=False)
    async def root():
        """Serve the dashboard index.html if present"""
        index_path = FRONTEND_PUBLIC / "index.html"
        if index_path.exists():
            return FileResponse(index_path, media_type="text/html")
        return {"message": "Early Risk Signals API - Credit Card Delinquency System. Frontend not found."}

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
