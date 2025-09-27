"""
Strategy: signal rules, MA crossover.
"""
import pandas as pd

def regression_threshold(preds, threshold=0.0):
    """Long if predicted return > threshold."""
    trades = []
    for p in preds:
        signal = 1 if p["y_pred"] > threshold else 0
        trades.append({"date": p["date"], "signal": signal})
    return trades

def class_long(preds):
    """Long if predicted class is up."""
    trades = []
    for p in preds:
        signal = 1 if p["y_pred"] > 0 else 0
        trades.append({"date": p["date"], "signal": signal})
    return trades

def ma_crossover(df):
    """Simple MA crossover strategy."""
    df = df.copy()
    df["signal"] = (df["sma_5"] > df["sma_20"]).astype(int)
    return df[["Date", "signal"]]
