"""
Application Configuration
Centralized configuration for the entire application
"""

import os
from pathlib import Path

# Base directories (project root)
# config.py lives in backend/app/core/, so walk up to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# File paths
# Use corrected filename in project data dir
CSV_FILE = DATA_DIR / "cc_delinquency.csv"
# If CSV not present in data directory, fallback to project root CSV (legacy location)
if not CSV_FILE.exists():
	# check legacy locations including project root and backend/data
	alt_locations = [
		BASE_DIR / "cc_delinquency.csv",
		BASE_DIR / "backend" / "data" / "cc_deliquency.csv",
		BASE_DIR / "data" / "cc_delinquency.csv",
		# Keep fallback to old misspelled name for compatibility
		BASE_DIR / "cc_deliquency.csv",
		BASE_DIR / "backend" / "data" / "cc_deliquency.csv",
	]
	for alt in alt_locations:
		if alt.exists():
			CSV_FILE = alt
			break

# API settings
API_V1_PREFIX = "/api/v1"
API_TITLE = "Early Risk Signals - Credit Card Delinquency System"
API_DESCRIPTION = "API for identifying early behavioral signals of credit card delinquency"
API_VERSION = "1.0.0"

# CORS settings
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Model training parameters
MODEL_RANDOM_STATE = 42
GB_N_ESTIMATORS = 100
GB_LEARNING_RATE = 0.1

# Risk scoring thresholds
RISK_HIGH_THRESHOLD = 3
RISK_MEDIUM_THRESHOLD = 2

# Signal detection thresholds
SPEND_DECLINE_THRESHOLD = -10
UTILIZATION_HIGH_THRESHOLD = 80
UTILIZATION_MEDIUM_THRESHOLD = 70
CASH_WITHDRAWAL_THRESHOLD = 15
PAYMENT_RATIO_HIGH_THRESHOLD = 40
PAYMENT_RATIO_MEDIUM_THRESHOLD = 60
MIN_DUE_PAID_FREQUENCY_THRESHOLD = 30
MERCHANT_MIX_THRESHOLD = 0.4

# Intervention costs and revenue
HIGH_INTERVENTION_COST = 20.0
MEDIUM_INTERVENTION_COST = 7.50
LOW_INTERVENTION_COST = 0.50
AVG_LOSS_PER_DEFAULT = 5000.0

# Intervention effectiveness rates
HIGH_PREVENTION_RATE = 0.40
MEDIUM_PREVENTION_RATE = 0.25
LOW_PREVENTION_RATE = 0.07
