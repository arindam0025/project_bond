"""
Pipeline: end-to-end train → predict helpers.
"""
from core.models import linreg_train, linreg_predict, naive_regression, naive_classification, arima_train, arima_predict, xgb_train, xgb_predict

def train_model(model_type, X, y, params=None):
    """Train model by type."""
    if model_type == "naive":
        return None  # Naive doesn't need fitting
    elif model_type == "linreg":
        return linreg_train(X, y)
    elif model_type == "arima":
        order = params.get("order", (1,0,0)) if params else (1,0,0)
        return arima_train(y, order=order)
    elif model_type == "xgb":
        return xgb_train(X, y)
    else:
        raise ValueError("Unknown model type")

def predict_model(model_type, model, X, y=None):
    """Predict by model type."""
    if model_type == "naive":
        return naive_regression(y) if y is not None else None
    elif model_type == "linreg":
        return linreg_predict(model, X)
    elif model_type == "arima":
        return arima_predict(model, steps=len(y)) if y is not None else None
    elif model_type == "xgb":
        return xgb_predict(model, X)
    else:
        raise ValueError("Unknown model type")
