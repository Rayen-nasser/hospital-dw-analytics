#!/usr/bin/env python3
"""
FastAPI service for real‑time readmission risk prediction.
Usage: uvicorn src.ml.api:app --reload
"""
import os
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Any, Dict

app = FastAPI(title="Readmission Risk API", description="API to predict 30-day hospital readmission risk. View /docs for Swagger UI.")

# Mount static files for frontend
static_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(static_dir, "index.html"))

# Load model on startup – path relative to this file
model_path = os.path.join(os.path.dirname(__file__), "..", "..", "model", "readmission_model.pkl")
model = joblib.load(model_path)

class PredictionRequest(BaseModel):
    """Generic payload – must contain all features the model expects."""
    data: Dict[str, Any] = Field(..., description="Feature key‑value pairs (names must match training)")

@app.post("/predict")
def predict(request: PredictionRequest):
    # Convert input dict to single‑row DataFrame
    df = pd.DataFrame([request.data])
    # Predict (pipeline handles preprocessing internally)
    proba = model.predict_proba(df)[0]
    prediction = int(model.predict(df)[0])
    return {
        "prediction": prediction,          # 0 = not readmitted, 1 = readmitted <30 days
        "probability_readmitted": float(proba[1]),
        "probability_not_readmitted": float(proba[0])
    }

@app.get("/health")
def health():
    return {"status": "ok"}
