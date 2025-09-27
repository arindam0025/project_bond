"""
Test: short synthetic series 60 rows, 2 steps, metrics keys present.
"""
import pandas as pd
from core.backtest import walk_forward

def test_backtest():
    df = pd.DataFrame({
        "Date": pd.date_range("2022-01-01", periods=60),
        "Close": range(60)
    })
    def model_fn(train):
        return None
    def predict_fn(model, test):
        return test["Close"].values
    results = walk_forward(df, train_days=20, test_days=10, model_fn=model_fn, predict_fn=predict_fn)
    assert len(results) > 0
    for r in results:
        assert "date" in r and "y_true" in r and "y_pred" in r
