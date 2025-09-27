from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core import config, data, features, models, backtest, strategy, metrics, utils
from services import pipeline, storage
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Commodity Price Predictor", version="1.0")

# Allow frontend origin (adjust as needed)
origins = [
    "http://localhost:8000",
    "https://your-github-pages-domain.github.io"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYMBOLS = ["CL=F", "NG=F", "GC=F"]

# --- Pydantic Schemas ---
class DataLoadRequest(BaseModel):
    symbol: str
    start: str
    end: str
    offline: bool = False

class FeaturesBuildRequest(BaseModel):
    symbol: str
    start: str
    end: str
    offline: bool = False

class ModelTrainRequest(BaseModel):
    symbol: str
    target: str
    model: str
    train_start: str
    train_end: str
    params: dict = {}

class ModelPredictRequest(BaseModel):
    model_id: str
    start: str
    end: str

class BacktestRunRequest(BaseModel):
    symbol: str
    target: str
    model: str
    params: dict = {}
    train_window_days: int
    test_window_days: int
    start: str
    end: str

class StrategyRunRequest(BaseModel):
    preds: list
    rule: str
    threshold: float = 0.0
    fee_bps: float = 0.05

class PortfolioAggregateRequest(BaseModel):
    series: list
    weights: dict

class ScenarioWhatIfRequest(BaseModel):
    symbol: str
    date: str
    price_shock_pct: float
    vol_mult: float

# --- API Endpoints ---

@app.post("/data/load")
def load_data_api(req: DataLoadRequest):
    df = data.load_data(req.symbol, req.start, req.end, req.offline)
    summary = {
        "start_date": df["Date"].min() if "Date" in df else None,
        "end_date": df["Date"].max() if "Date" in df else None,
        "n_rows": len(df),
        "n_missing": int(df.isna().sum().sum()),
        "zeros": int((df == 0).sum().sum()),
    }
    rows = df.head(100).to_dict("records")
    return {"summary": summary, "rows": rows}

@app.post("/features/build")
def build_features_api(req: FeaturesBuildRequest):
    df = data.load_data(req.symbol, req.start, req.end, req.offline)
    feats = features.build_features(df)
    columns = list(feats.columns)
    preview = feats.head(100).to_dict("records")
    info = {"nan_count_by_col": feats.isna().sum().to_dict()}
    return {"columns": columns, "preview": preview, "info": info}

@app.post("/models/train")
def train_model_api(req: ModelTrainRequest):
    df = data.load_data(req.symbol, req.train_start, req.train_end, offline=False)
    feats = features.build_features(df)
    X = feats.drop(["Date", "Close"], axis=1)
    y = feats["Close"]
    model = pipeline.train_model(req.model, X, y, req.params)
    if model is not None:
        model_id = storage.save_model(model, req.symbol, req.target, req.model)
    else:
        model_id = f"{req.symbol}_{req.target}_{req.model}"
    y_pred = pipeline.predict_model(req.model, model, X, y)
    train_metrics = {
        "mae": metrics.mae(y, y_pred),
        "rmse": metrics.rmse(y, y_pred),
        "mape": metrics.mape(y, y_pred)
    }
    return {"train_metrics": train_metrics, "model_id": model_id}

@app.post("/models/predict")
def predict_model_api(req: ModelPredictRequest):
    symbol, target, model_type = req.model_id.split("_")
    model = storage.load_model(symbol, target, model_type)
    df = data.load_data(symbol, req.start, req.end, offline=False)
    feats = features.build_features(df)
    X = feats.drop(["Date", "Close"], axis=1)
    y = feats["Close"]
    y_pred = pipeline.predict_model(model_type, model, X, y)
    preds = [{"date": d, "y_true": yt, "y_pred": yp} for d, yt, yp in zip(feats["Date"], y, y_pred)]
    return {"predictions": preds}

@app.post("/backtest/run")
def backtest_run_api(req: BacktestRunRequest):
    df = data.load_data(req.symbol, req.start, req.end, offline=False)
    feats = features.build_features(df)
    def model_fn(train):
        X = train.drop(["Date", "Close"], axis=1)
        y = train["Close"]
        return pipeline.train_model(req.model, X, y, req.params)
    def predict_fn(model, test):
        X = test.drop(["Date", "Close"], axis=1)
        y = test["Close"]
        return pipeline.predict_model(req.model, model, X, y)
    results = backtest.walk_forward(feats, req.train_window_days, req.test_window_days, model_fn, predict_fn)
    y_true = [r["y_true"] for r in results]
    y_pred = [r["y_pred"] for r in results]
    metrics_out = {
        "mae": metrics.mae(y_true, y_pred),
        "rmse": metrics.rmse(y_true, y_pred),
        "mape": metrics.mape(y_true, y_pred)
    }
    equity = np.cumsum(np.array(y_pred) - np.array(y_true)).tolist()
    equity_curve = [{"date": r["date"], "equity": e} for r, e in zip(results, equity)]
    return {"metrics": metrics_out, "equity": equity_curve, "preds": results}

@app.post("/strategy/run")
def strategy_run_api(req: StrategyRunRequest):
    if req.rule == "regression_threshold":
        trades = strategy.regression_threshold(req.preds, req.threshold)
    elif req.rule == "class_long":
        trades = strategy.class_long(req.preds)
    else:
        trades = []
    equity = [t["signal"] for t in trades]
    stats = {
        "trades": len(trades),
        "win_rate": float(np.mean(equity)) if equity else 0.0
    }
    return {"trades": trades, "equity": equity, "stats": stats}

@app.post("/portfolio/aggregate")
def portfolio_aggregate_api(req: PortfolioAggregateRequest):
    portfolio_equity = []
    dates = None
    for s in req.series:
        eq = [e["value"] for e in s["equity"]]
        if dates is None:
            dates = [e["date"] for e in s["equity"]]
        if not portfolio_equity:
            portfolio_equity = np.array(eq) * req.weights.get(s["symbol"], 0)
        else:
            portfolio_equity += np.array(eq) * req.weights.get(s["symbol"], 0)
    stats = {
        "cagr": metrics.cagr(portfolio_equity),
        "max_drawdown": metrics.max_drawdown(portfolio_equity)
    }
    out = [{"date": d, "value": float(v)} for d, v in zip(dates, portfolio_equity)]
    return {"portfolio_equity": out, "stats": stats}

@app.get("/models/list")
def models_list_api():
    files = os.listdir(config.MODEL_DIR)
    models_out = [f.replace(".joblib","") for f in files if f.endswith(".joblib")]
    return models_out

@app.post("/scenarios/whatif")
def scenarios_whatif_api(req: ScenarioWhatIfRequest):
    df = data.load_data(req.symbol, req.date, req.date, offline=False)
    if df.empty:
        return {"new_features": {}, "one_step_pred": None}
    df["Close"] *= (1 + req.price_shock_pct / 100)
    df["Volume"] *= req.vol_mult
    feats = features.build_features(df)
    X = feats.drop(["Date", "Close"], axis=1)
    y = feats["Close"]
    model_id = f"{req.symbol}_regression_linreg"
    model = storage.load_model(req.symbol, "regression", "linreg")
    pred = pipeline.predict_model("linreg", model, X, y)
    return {"new_features": feats.iloc[-1].to_dict(), "one_step_pred": float(pred[-1]) if len(pred) else None}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Commodity Price Predictor", version="1.0")

# Allow frontend origin (adjust as needed)
origins = [
    "http://localhost:8000",
    "https://your-github-pages-domain.github.io"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYMBOLS = ["CL=F", "NG=F", "GC=F"]

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "version": app.version}

@app.get("/symbols")
def get_symbols():
    """Return supported commodity symbols."""
    return SYMBOLS
