"""
Model Training Module
Trains and manages machine learning models for delinquency prediction
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from typing import Tuple, List
from .config import (
    MODEL_RANDOM_STATE,
    GB_N_ESTIMATORS,
    GB_LEARNING_RATE
)


class ModelTrainer:
    """Train and manage ML models"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_importance = None
        self.features_list = None
    
    def train(self, df: pd.DataFrame, signal_cols: List[str]) -> None:
        """
        Train Gradient Boosting model for delinquency prediction
        
        Args:
            df: DataFrame with all features and target
            signal_cols: List of signal column names
        """
        # Define features for model
        self.features_list = [
            'Utilisation %', 'Avg Payment Ratio', 'Min Due Paid Frequency',
            'Merchant Mix Index', 'Cash Withdrawal %', 'Recent Spend Change %'
        ] + signal_cols
        
        # Prepare training data
        X = df[self.features_list].copy()
        y = df['is_delinquent'].copy()
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model = GradientBoostingClassifier(
            n_estimators=GB_N_ESTIMATORS,
            learning_rate=GB_LEARNING_RATE,
            random_state=MODEL_RANDOM_STATE
        )
        self.model.fit(X, y)
        
        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'Feature': self.features_list,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)
    
    def predict_proba(self, features: List[float]) -> float:
        """
        Predict delinquency probability for a customer
        
        Args:
            features: List of feature values
        
        Returns:
            Probability of delinquency (0-1)
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        return self.model.predict_proba([features])[0][1]
    
    def get_top_features(self, n: int = 10) -> pd.DataFrame:
        """Get top N important features"""
        if self.feature_importance is None:
            raise ValueError("Feature importance not calculated")
        
        return self.feature_importance.head(n)
