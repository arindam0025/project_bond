"""
Data loading and caching. Loads from yfinance or local CSV fallback.
"""
import pandas as pd
import yfinance as yf
import os
from core.config import SYMBOLS, CSV_FILES

def load_data(symbol: str, start: str, end: str, offline: bool = False) -> pd.DataFrame:
    """Load data from yfinance or local CSV."""
    if symbol not in SYMBOLS:
        raise ValueError("Invalid symbol")
    if not offline:
        try:
            df = yf.download(symbol, start=start, end=end)
            if not df.empty:
                df.reset_index(inplace=True)
                return df
        except Exception:
            pass
    # Fallback to CSV
    csv_path = CSV_FILES.get(symbol)
    if csv_path and os.path.exists(csv_path):
        df = pd.read_csv(csv_path, parse_dates=["Date"])
        return df[(df["Date"] >= start) & (df["Date"] <= end)].copy()
    raise FileNotFoundError(f"No data for {symbol}")

def save_cache(symbol: str, df: pd.DataFrame):
    """Save DataFrame to CSV cache."""
    csv_path = CSV_FILES.get(symbol)
    if csv_path:
        df.to_csv(csv_path, index=False)
