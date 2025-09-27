"""
Config: constants, symbols, paths, CORS settings.
"""
import os

# Supported symbols
SYMBOLS = ["CL=F", "NG=F", "GC=F"]

# Data and model paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

# CORS origins for frontend
CORS_ORIGINS = [
    "http://localhost:8000",
    "https://your-github-pages-domain.github.io"
]

# Default CSV files
CSV_FILES = {
    "CL=F": os.path.join(DATA_DIR, "CL=F.csv"),
    "NG=F": os.path.join(DATA_DIR, "NG=F.csv"),
    "GC=F": os.path.join(DATA_DIR, "GC=F.csv"),
}

# Default API version
API_VERSION = "1.0"
