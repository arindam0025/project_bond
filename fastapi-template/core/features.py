"""
Feature engineering: indicators and lags.
"""
import pandas as pd
import numpy as np

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add indicators and lags. Drop NaNs after build."""
    df = df.copy()
    df["pct_change_1d"] = df["Close"].pct_change(1)
    df["pct_change_5d"] = df["Close"].pct_change(5)
    df["sma_5"] = df["Close"].rolling(5).mean()
    df["sma_20"] = df["Close"].rolling(20).mean()
    df["std_10"] = df["Close"].rolling(10).std()
    df["rsi_14"] = calc_rsi(df["Close"], 14)
    df["macd_line"], df["macd_signal"] = calc_macd(df["Close"])
    df["close_lag1"] = df["Close"].shift(1)
    df["close_lag5"] = df["Close"].shift(5)
    return df.dropna().reset_index(drop=True)

def calc_rsi(series, period=14):
    """Calculate RSI indicator."""
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(period).mean()
    avg_loss = pd.Series(loss).rolling(period).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    return 100 - (100 / (1 + rs))

def calc_macd(series):
    """Calculate MACD line and signal."""
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    macd_signal = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, macd_signal
