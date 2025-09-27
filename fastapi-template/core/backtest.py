"""
Backtest: rolling walk-forward.
"""
import numpy as np
import pandas as pd

def walk_forward(df, train_days, test_days, model_fn, predict_fn):
    """Walk-forward backtest."""
    results = []
    n = len(df)
    i = 0
    while i + train_days + test_days <= n:
        train = df.iloc[i:i+train_days]
        test = df.iloc[i+train_days:i+train_days+test_days]
        model = model_fn(train)
        preds = predict_fn(model, test)
        for idx, row in test.iterrows():
            results.append({
                "date": row["Date"],
                "y_true": row["Close"],
                "y_pred": preds[idx - (i+train_days)]
            })
        i += test_days
    return results
