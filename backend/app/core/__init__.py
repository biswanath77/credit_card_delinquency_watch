"""
Core module initialization
"""

from .config import (
    API_V1_PREFIX,
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    CORS_ORIGINS,
    RISK_HIGH_THRESHOLD,
    RISK_MEDIUM_THRESHOLD
)
from .data_loader import prepare_data, DataLoader
from .model_trainer import ModelTrainer

__all__ = [
    'API_V1_PREFIX',
    'API_TITLE',
    'API_DESCRIPTION',
    'API_VERSION',
    'CORS_ORIGINS',
    'prepare_data',
    'DataLoader',
    'ModelTrainer'
]
