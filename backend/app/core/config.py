"""
Application Configuration
Centralized configuration for the entire application.
"""

import os
from pathlib import Path


# ---------------------------------------------------------
# Base Directories (safe for Render / Docker / local dev)
# ---------------------------------------------------------

# config.py lives in: backend/app/core/
# Go up to project root
BASE_DIR = Path(__file__).resolve().parents[3]

# Allow Render or Docker to override paths using environment variables
ENV_MODELS_DIR = os.getenv("MODEL_DIR", "")
ENV_DATA_DIR = os.getenv("DATA_DIR", "")

# Default directories inside repo (safe & writable)
DEFAULT_MODELS_DIR = BASE_DIR / "models"
DEFAULT_DATA_DIR = BASE_DIR / "data"

# Choose final directories
MODELS_DIR = Path(ENV_MODELS_DIR) if ENV_MODELS_DIR else DEFAULT_MODELS_DIR
DATA_DIR = Path(ENV_DATA_DIR) if ENV_DATA_DIR else DEFAULT_DATA_DIR


# ---------------------------------------------------------
# Safe Directory Creation (with fallback for Render)
# ---------------------------------------------------------
def safe_mkdir(path: Path) -> Path:
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except PermissionError:
        # Render sometimes does not allow writing under /app
        fallback = Path("/tmp") / path.name
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


MODELS_DIR = safe_mkdir(MODELS_DIR)
DATA_DIR = safe_mkdir(DATA_DIR)


# ---------------------------------------------------------
# CSV File Resolution Logic (supports legacy file names)
# ---------------------------------------------------------

CSV_FILE = DATA_DIR / "cc_delinquency.csv"

if not CSV_FILE.exists():
    legacy_locations = [
        BASE_DIR / "cc_delinquency.csv",
        BASE_DIR / "data" / "cc_delinquency.csv",
        BASE_DIR / "backend" / "data" / "cc_delinquency.csv",

        # Misspelled fallback (for backwards compatibility)
        BASE_DIR / "cc_deliquency.csv",
        BASE_DIR / "backend" / "data" / "cc_deliquency.csv",
    ]

    for alt in legacy_locations:
        if alt.exists():
            CSV_FILE = alt
            break


# ---------------------------------------------------------
# API Settings
# ---------------------------------------------------------

API_V1_PREFIX = "/api/v1"
API_TITLE = "Early Risk Signals - Credit Card Delinquency System"
API_DESCRIPTION = "API for identifying early behavioral signals of credit card delinquency"
API_VERSION = "1.0.0"


# ---------------------------------------------------------
# CORS Settings
# ---------------------------------------------------------

# Replace "*" with your frontend URL for production
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]


# ---------------------------------------------------------
# Model Training Parameters
# ---------------------------------------------------------

MODEL_RANDOM_STATE = 42
GB_N_ESTIMATORS = 100
GB_LEARNING_RATE = 0.1


# ---------------------------------------------------------
# Risk Scoring Thresholds
# ---------------------------------------------------------

RISK_HIGH_THRESHOLD = 3           # >= 3
RISK_MEDIUM_THRESHOLD = 2         # 2 – 2.99


# ---------------------------------------------------------
# Signal Detection Thresholds
# ---------------------------------------------------------

SPEND_DECLINE_THRESHOLD = -10
UTILIZATION_HIGH_THRESHOLD = 80
UTILIZATION_MEDIUM_THRESHOLD = 70
CASH_WITHDRAWAL_THRESHOLD = 15
PAYMENT_RATIO_HIGH_THRESHOLD = 40
PAYMENT_RATIO_MEDIUM_THRESHOLD = 60
MIN_DUE_PAID_FREQUENCY_THRESHOLD = 30
MERCHANT_MIX_THRESHOLD = 0.4


# ---------------------------------------------------------
# Intervention Costs & Effectiveness
# ---------------------------------------------------------

HIGH_INTERVENTION_COST = 20.0
MEDIUM_INTERVENTION_COST = 7.50
LOW_INTERVENTION_COST = 0.50
AVG_LOSS_PER_DEFAULT = 5000.0

HIGH_PREVENTION_RATE = 0.40
MEDIUM_PREVENTION_RATE = 0.25
LOW_PREVENTION_RATE = 0.07
