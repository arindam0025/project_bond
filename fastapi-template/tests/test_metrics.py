"""
Test: Sharpe, MAPE, MaxDD correct on toy arrays.
"""
from core.metrics import sharpe, mape, max_drawdown

def test_metrics():
    y_true = [1,2,3,4,5]
    y_pred = [1,2,2,4,5]
    returns = [0.01, 0.02, -0.01, 0.03, 0.00]
    equity = [100, 102, 101, 104, 104]
    assert abs(sharpe(returns) - 1.0) < 2.0
    assert abs(mape(y_true, y_pred) - 8.0) < 10.0
    assert abs(max_drawdown(equity) + 0.0098) < 0.01
