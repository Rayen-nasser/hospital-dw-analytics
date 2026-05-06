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

# Load model on startup
model_path = os.path.join(os.path.dirname(__file__), "..", "..", "model", "readmission_model.pkl")
model = joblib.load(model_path)

# Load a single template row from the dataset to handle missing columns
data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "transformed_diabetes.csv")
try:
    template_df = pd.read_csv(data_path, nrows=1)
    # Drop identifiers and target just like in training
    cols_to_drop = ["readmitted_binary", "encounter_id", "patient_nbr"]
    template_df = template_df.drop(columns=[c for c in cols_to_drop if c in template_df.columns], errors="ignore")
    template_row = template_df.iloc[0].to_dict()
except Exception as e:
    print(f"Warning: Could not load template row from data: {e}")
    template_row = {}

class PredictionRequest(BaseModel):
    """Generic payload – must contain all features the model expects."""
    data: Dict[str, Any] = Field(..., description="Feature key‑value pairs (names must match training)")

@app.post("/predict")
def predict(request: PredictionRequest):
    # Start with default template and update with provided data
    payload = template_row.copy()
    payload.update(request.data)
    
    # Convert input dict to single‑row DataFrame
    df = pd.DataFrame([payload])
    
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
