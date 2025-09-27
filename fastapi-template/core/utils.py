"""
Utils: seeds, date helpers, returns, split.
"""
import numpy as np
import random
import pandas as pd

def set_seeds(seed=42):
    """Set random seeds."""
    np.random.seed(seed)
    random.seed(seed)

def date_range(start, end):
    """Generate date range."""
    return pd.date_range(start, end)

def calc_returns(prices):
    """Calculate returns."""
    prices = np.array(prices)
    return np.diff(prices) / (prices[:-1] + 1e-9)

def train_test_split(df, test_size=0.2):
    """Split DataFrame into train/test."""
    n = int(len(df) * (1 - test_size))
    return df.iloc[:n], df.iloc[n:]
