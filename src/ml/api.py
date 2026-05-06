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
    
    # Recalculate derived features so the model sees the correct state!
    try:
        # 1. Length of stay categories
        days = int(payload.get("time_in_hospital", 0))
        if days <= 3:
            payload["stay_category"] = "Short"
        elif days <= 7:
            payload["stay_category"] = "Medium"
        else:
            payload["stay_category"] = "Long"
            
        # 2. Patient complexity score
        payload["complexity_score"] = int(payload.get("num_lab_procedures", 0)) + int(payload.get("num_procedures", 0)) + int(payload.get("num_medications", 0))
        
        # 3. Prior utilization score
        payload["prior_utilization"] = int(payload.get("number_outpatient", 0)) + int(payload.get("number_emergency", 0)) + int(payload.get("number_inpatient", 0))
        
        # 4. Age numeric
        age = str(payload.get("age", ""))
        age_map = {
            "[0-10)": 5, "[10-20)": 15, "[20-30)": 25, "[30-40)": 35,
            "[40-50)": 45, "[50-60)": 55, "[60-70)": 65, "[70-80)": 75,
            "[80-90)": 85, "[90-100)": 95
        }
        if age in age_map:
            payload["age_numeric"] = age_map[age]
            
        # 5. Clinical indicators
        a1c_map = {">7": 8, "Normal": 6, "None": 0, "Unknown": -1}
        if payload.get("A1Cresult") in a1c_map:
            payload["A1Cresult_numeric"] = a1c_map[payload.get("A1Cresult")]
            
        glu_map = {">200": 250, ">300": 350, "Normal": 100, "None": 0, "Unknown": -1}
        if payload.get("max_glu_serum") in glu_map:
            payload["max_glu_serum_numeric"] = glu_map[payload.get("max_glu_serum")]
            
        # 6. Medication intensity
        med_cols = ["metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride",
                    "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone",
                    "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide",
                    "examide", "citoglipton", "insulin", "glyburide-metformin",
                    "glipizide-metformin", "glimepiride-pioglitazone",
                    "metformin-rosiglitazone", "metformin-pioglitazone"]
        payload["medication_count"] = sum(1 for m in med_cols if str(payload.get(m, "No")).strip() != "No")
    except Exception as e:
        print(f"Warning: Failed to recalculate some features: {e}")
    
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
