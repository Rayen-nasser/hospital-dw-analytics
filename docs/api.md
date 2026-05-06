# API Documentation
## Readmission Risk Prediction API

### Endpoints

#### `GET /health`
Check if API is running.
```json
{"status": "ok"}
```

#### `POST /predict`
Predict readmission risk within 30 days.

**Request body:**
```json
{
  "data": {
    "race": "Caucasian",
    "gender": "Female",
    "age": "[40-50)",
    "time_in_hospital": 3,
    "stay_category": "Short",
    "readmitted_binary": 0,
    "complexity_score": 20,
    "prior_utilization": 1,
    "age_numeric": 45,
    "A1Cresult_numeric": -1,
    "max_glu_serum_numeric": -1,
    "medication_count": 2,
    "readmission_risk": "Low",
    "patient_encounter_count": 1
  }
}
```

**Response:**
```json
{
  "prediction": 0,
  "probability_readmitted": 0.15,
  "probability_not_readmitted": 0.85
}
```

### Run the server
```bash
python -m uvicorn src.ml.api:app --host 127.0.0.1 --port 8000 --reload
```

### Test with curl
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"data\": {\"time_in_hospital\": 3, \"age_numeric\": 45}}"
```

### Swagger UI
Visit: http://127.0.0.1:8000/docs
