"""
Test: features build, no NaNs and expected columns exist.
"""
import pandas as pd
from core.features import build_features

def test_features_build():
    df = pd.DataFrame({"Close": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]})
    out = build_features(df)
    expected = ["pct_change_1d", "pct_change_5d", "sma_5", "sma_20", "std_10", "rsi_14", "macd_line", "macd_signal", "close_lag1", "close_lag5"]
    for col in expected:
        assert col in out.columns
    assert not out.isna().any().any()
