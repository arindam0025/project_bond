"""
Storage: joblib save/load models per symbol+target.
"""
import os
import joblib
from core.config import MODEL_DIR

def save_model(model, symbol, target, model_type):
    """Save model artifact."""
    fname = f"{symbol}_{target}_{model_type}.joblib"
    path = os.path.join(MODEL_DIR, fname)
    joblib.dump(model, path)
    return path

def load_model(symbol, target, model_type):
    """Load model artifact."""
    fname = f"{symbol}_{target}_{model_type}.joblib"
    path = os.path.join(MODEL_DIR, fname)
    if os.path.exists(path):
        return joblib.load(path)
    return None
