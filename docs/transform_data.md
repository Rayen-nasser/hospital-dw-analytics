# Data Transformation Documentation
## Project: Hospital Data Warehouse Analytics
## Task: Transform Data (Task #3)
## Status: ✓ Completed

### 1. Objective
Transform the cleaned diabetes dataset by creating derived metrics and enriching it with new calculated fields for analysis, machine learning, and Power BI dashboard visualization.

### 2. Transformation Steps & Explanations

#### Step 3.1: Length of Stay Categories
- **New column**: `stay_category`
- **Logic**: 
  - Short stay: 1-3 days
  - Medium stay: 4-7 days
  - Long stay: 8+ days
- **Why**: Creates easy-to-understand categories for hospital performance dashboards. Short stays suggest efficient care, long stays may indicate complications.

#### Step 3.2: Readmission Binary Target (for ML)
- **New column**: `readmitted_binary`
- **Logic**: 1 if `readmitted == "<30"` (readmitted within 30 days), else 0
- **Why**: Creates a binary classification target for machine learning models predicting readmission risk.

#### Step 3.3: Patient Complexity Score
- **New column**: `complexity_score`
- **Logic**: `num_lab_procedures` + `num_procedures` + `num_medications`
- **Why**: Single metric summarizing how complex a patient's care was. Higher scores = more resource-intensive patients.

#### Step 3.4: Prior Utilization Score
- **New column**: `prior_utilization`
- **Logic**: `number_outpatient` + `number_emergency` + `number_inpatient`
- **Why**: Measures how much healthcare the patient used in the prior year. High utilization = potentially higher risk patients.

#### Step 3.5: Age Numeric Conversion
- **New column**: `age_numeric`
- **Logic**: Convert age groups to midpoints:
  - `[0-10)` → 5, `[10-20)` → 15, ..., `[90-100)` → 95
- **Why**: Converts categorical age groups to numeric values for correlation analysis and ML models.

#### Step 3.6: Clinical Indicators to Numeric
- **New column**: `A1Cresult_numeric`
  - `>7` → 8, `"Normal"` → 6, `"None"` → 0, `"Unknown"` → -1
- **New column**: `max_glu_serum_numeric`
  - `>200` → 250, `>300` → 350, `"Normal"` → 100, `"None"` → 0, `"Unknown"` → -1
- **Why**: Converts clinical indicators to numeric values for predictive modeling.

#### Step 3.7: Medication Intensity
- **New column**: `medication_count`
- **Logic**: Counts how many diabetes medications are active (not "No")
- **Why**: Measures treatment intensity. More medications = more complex management.

#### Step 3.8: Readmission Risk Category
- **New column**: `readmission_risk`
- **Logic**: Maps `readmitted` to risk levels:
  - `"NO"` → "Low"
  - `"<30"` → "High"
  - `">30"` → "Medium"
- **Why**: Creates a three-level risk category for dashboard visualization and stratified analysis.

#### Step 3.9: Patient Encounter Count
- **New column**: `patient_encounter_count`
- **Logic**: Counts how many hospital encounters each patient (`patient_nbr`) has
- **Why**: Identifies frequent visitors vs. first-time patients. High counts may indicate chronic conditions or poor care management.

### 3. Transformation Results
- **Input**: `data/raw/cleaned_diabetes.csv` (101,766 rows, 50 columns)
- **Output**: `data/raw/transformed_diabetes.csv` (101,766 rows, **60 columns**)
- **New columns added**: 10 derived metrics
- **File size**: ~24.4 MB

### 4. New Columns Summary
| New Column | Description | Used For |
|------------|-------------|----------|
| `stay_category` | Short/Medium/Long stay | Dashboard categorization |
| `readmitted_binary` | 1 if readmitted <30 days | ML binary target |
| `complexity_score` | Sum of procedures + meds | Patient complexity metric |
| `prior_utilization` | Prior year visit count | Risk stratification |
| `age_numeric` | Age group midpoint | Correlation analysis |
| `A1Cresult_numeric` | Numeric A1C result | Clinical modeling |
| `max_glu_serum_numeric` | Numeric glucose result | Clinical modeling |
| `medication_count` | Active diabetes med count | Treatment intensity |
| `readmission_risk` | Low/Medium/High risk | Dashboard KPI |
| `patient_encounter_count` | Number of patient visits | Patient journey analysis |

### 5. Dashboard & ML Applications
- **Power BI Dashboard**:
  - Average stay length by category (`stay_category`)
  - Readmission rate by risk level (`readmission_risk`)
  - Patient complexity distribution (`complexity_score`)
  - Prior utilization vs. readmission correlation

- **Machine Learning Models**:
  - **Binary classifier**: Predict `readmitted_binary` using clinical + demographic features
  - **Multiclass classifier**: Predict `readmission_risk` (Low/Medium/High)
  - **Regression**: Predict `time_in_hospital` (length of stay)

### 6. Task Status
- **Task #3 - Transform data**: Marked as completed ✓
- **Next tasks available**:
  - Task #4: Train model (predict readmission risk)
  - Task #5: Load to warehouse (database loading)
  - Task #6: Build Power BI dashboard
  - Task #7: Add CI/CD pipeline
