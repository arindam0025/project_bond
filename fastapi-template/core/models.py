"""
Models: Naive, Linear Regression, ARIMA-lite, XGBoost.
"""
import numpy as np
from sklearn.linear_model import Ridge
from statsmodels.tsa.arima.model import ARIMA
import xgboost as xgb

def naive_regression(y):
    """Predict next close = today close."""
    return np.roll(y, 1)

def naive_classification(y):
    """Majority class prediction."""
    return np.full_like(y, np.round(np.mean(y)))

def linreg_train(X, y):
    """Train Ridge regression."""
    model = Ridge(alpha=1.0)
    model.fit(X, y)
    return model

def linreg_predict(model, X):
    """Predict with Ridge regression."""
    return model.predict(X)

def arima_train(y, order=(1,0,0)):
    """Train ARIMA-lite."""
    model = ARIMA(y, order=order)
    fit = model.fit()
    return fit

def arima_predict(fit, steps=1):
    """Predict with ARIMA-lite."""
    return fit.forecast(steps=steps)

def xgb_train(X, y):
    """Train XGBoost small model."""
    model = xgb.XGBRegressor(n_estimators=20, max_depth=3, verbosity=0)
    model.fit(X, y)
    return model

def xgb_predict(model, X):
    """Predict with XGBoost."""
    return model.predict(X)
