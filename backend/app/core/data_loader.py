"""
Data Loading and Feature Engineering Module
Handles data loading, preprocessing, and feature creation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, List
from .config import (
    CSV_FILE,
    SPEND_DECLINE_THRESHOLD,
    UTILIZATION_HIGH_THRESHOLD,
    UTILIZATION_MEDIUM_THRESHOLD,
    CASH_WITHDRAWAL_THRESHOLD,
    PAYMENT_RATIO_HIGH_THRESHOLD,
    PAYMENT_RATIO_MEDIUM_THRESHOLD,
    MIN_DUE_PAID_FREQUENCY_THRESHOLD,
    MERCHANT_MIX_THRESHOLD,
    RISK_HIGH_THRESHOLD,
    RISK_MEDIUM_THRESHOLD,
)


class DataLoader:
    """Load and preprocess customer data"""
    
    @staticmethod
    def load_data(csv_path: str = None) -> pd.DataFrame:
        """
        Load customer data from CSV
        
        Args:
            csv_path: Path to CSV file. Uses config path if None.
        
        Returns:
            DataFrame with customer data
        """
        path = Path(csv_path) if csv_path else CSV_FILE
        
        if not path.exists():
            raise FileNotFoundError(f"Data file not found at {path}")
        
        df = pd.read_csv(path)
        return df
    
    @staticmethod
    def create_target_variable(df: pd.DataFrame) -> pd.DataFrame:
        """Create target variable for delinquency prediction"""
        df['is_delinquent'] = (df['DPD Bucket Next Month'] > 0).astype(int)
        return df
    
    @staticmethod
    def engineer_signals(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Engineer behavioral risk signals
        
        Returns:
            DataFrame with signals and list of signal column names
        """
        df_features = df.copy()
        
        # Signal 1: Spending Decline
        df_features['signal_spend_decline'] = (
            df_features['Recent Spend Change %'] < SPEND_DECLINE_THRESHOLD
        ).astype(int)
        
        # Signal 2: High Utilization
        df_features['signal_high_utilization'] = (
            (df_features['Utilisation %'] > UTILIZATION_HIGH_THRESHOLD) | 
            ((df_features['Utilisation %'] > UTILIZATION_MEDIUM_THRESHOLD) & 
             (df_features['Cash Withdrawal %'] > CASH_WITHDRAWAL_THRESHOLD))
        ).astype(int)
        
        # Signal 3: Payment Decline
        df_features['signal_payment_decline'] = (
            (df_features['Avg Payment Ratio'] < PAYMENT_RATIO_HIGH_THRESHOLD) | 
            ((df_features['Avg Payment Ratio'] < PAYMENT_RATIO_MEDIUM_THRESHOLD) & 
             (df_features['Min Due Paid Frequency'] < MIN_DUE_PAID_FREQUENCY_THRESHOLD))
        ).astype(int)
        
        # Signal 4: Cash Surge
        df_features['signal_cash_surge'] = (
            df_features['Cash Withdrawal %'] > CASH_WITHDRAWAL_THRESHOLD
        ).astype(int)
        
        # Signal 5: Low Merchant Mix
        df_features['signal_low_merchant_mix'] = (
            df_features['Merchant Mix Index'] < MERCHANT_MIX_THRESHOLD
        ).astype(int)
        
        signal_cols = [
            'signal_spend_decline',
            'signal_high_utilization',
            'signal_payment_decline',
            'signal_cash_surge',
            'signal_low_merchant_mix'
        ]
        
        return df_features, signal_cols
    
    @staticmethod
    def calculate_risk_score(df: pd.DataFrame, signal_cols: List[str]) -> pd.DataFrame:
        """
        Calculate composite risk score from signals
        
        Args:
            df: DataFrame with signal columns
            signal_cols: List of signal column names
        
        Returns:
            DataFrame with risk_score and risk_tier columns
        """
        df['risk_score'] = df[signal_cols].sum(axis=1)
        
        def classify_risk(score):
            if score >= RISK_HIGH_THRESHOLD:
                return 'HIGH'
            elif score >= RISK_MEDIUM_THRESHOLD:
                return 'MEDIUM'
            else:
                return 'LOW'
        
        df['risk_tier'] = df['risk_score'].apply(classify_risk)
        return df


def prepare_data() -> Tuple[pd.DataFrame, List[str]]:
    """
    Complete data preparation pipeline
    
    Returns:
        Tuple of (DataFrame with engineered features, signal column names)
    """
    df = DataLoader.load_data()
    df = DataLoader.create_target_variable(df)
    df, signal_cols = DataLoader.engineer_signals(df)
    df = DataLoader.calculate_risk_score(df, signal_cols)
    
    return df, signal_cols
