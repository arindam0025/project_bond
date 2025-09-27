# Commodity Price Predictor Frontend

## How to run
Open `index.html` in your browser, or use a local server (e.g. Python's `http.server`).

## How to deploy
Push to GitHub, then enable GitHub Pages (main branch, root).
Set backend URL in Settings page.

## Pages
- Overview: summary and price chart
- Data: table preview
- Features: columns and NaN report
- Models: train and metrics
- Backtest: run and show equity curve
- Strategy: run and show stats
- Portfolio: combine equity series
- Scenarios: price shock and vol mult
- Explain: model info
- Settings: backend URL and offline toggle

## Charting
Uses Plotly.js via CDN.

## API
Calls backend FastAPI endpoints.
