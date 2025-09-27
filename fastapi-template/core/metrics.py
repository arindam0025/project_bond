"""
Metrics: MAE, RMSE, MAPE, Sharpe, MaxDD, CAGR, hit rate.
"""
import numpy as np

def mae(y_true, y_pred):
    """Mean Absolute Error."""
    return float(np.mean(np.abs(np.array(y_true) - np.array(y_pred))))

def rmse(y_true, y_pred):
    """Root Mean Squared Error."""
    return float(np.sqrt(np.mean((np.array(y_true) - np.array(y_pred)) ** 2)))

def mape(y_true, y_pred):
    """Mean Absolute Percentage Error."""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return float(np.mean(np.abs((y_true - y_pred) / (y_true + 1e-9))) * 100)

def sharpe(returns, rf=0.0):
    """Sharpe ratio."""
    excess = np.array(returns) - rf
    return float(np.mean(excess) / (np.std(excess) + 1e-9))

def max_drawdown(equity):
    """Max drawdown."""
    equity = np.array(equity)
    peak = np.maximum.accumulate(equity)
    dd = (equity - peak) / (peak + 1e-9)
    return float(dd.min())

def cagr(equity, periods_per_year=252):
    """Compound Annual Growth Rate."""
    equity = np.array(equity)
    years = len(equity) / periods_per_year
    return float((equity[-1] / equity[0]) ** (1 / years) - 1)

def hit_rate(y_true, y_pred):
    """Hit rate (directional accuracy)."""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return float(np.mean(np.sign(y_true[1:] - y_true[:-1]) == np.sign(y_pred[1:] - y_pred[:-1])))
