# Dataset Column Reference
## Diabetes 130-US Hospitals (1999-2008) - Column Explanations

### Core Identifiers
| Column | Meaning | Used For |
|--------|---------|----------|
| **encounter_id** | Unique ID for each hospital admission | Track individual stays, detect duplicates |
| **patient_nbr** | Unique patient ID (same patient = multiple encounters) | Link multiple visits by same patient |

### Hospital Performance Metrics
| Column | Meaning | Example | Why It Matters |
|--------|---------|---------|----------------|
| **time_in_hospital** | Days stayed in hospital | 1, 3, 14 | Shorter stays = better efficiency |
| **readmitted** | Readmission within 30 days | "NO", "<30", ">30" | **Key KPI** - high readmission = poor care |
| **admission_type_id** | Type of admission | 1=Emergency, 2=Urgent, 3=Elective | Performance tracking |
| **discharge_disposition_id** | Where patient went after discharge | 1=Home, 2=Another hospital | Patient flow analysis |
| **admission_source_id** | How patient arrived | 1=Physician referral, 7=ER | Patient flow analysis |

### Demographic Features
| Column | Meaning | Values |
|--------|---------|--------|
| **race** | Patient race/ethnicity | Caucasian, AfricanAmerican, Asian, etc. |
| **gender** | Patient gender | Male, Female |
| **age** | Age group | [0-10), [10-20), ..., [80-90), [90-100) |

### Clinical Features
| Column | Meaning | Values |
|--------|---------|--------|
| **diag_1, diag_2, diag_3** | Primary, secondary, tertiary diagnoses (ICD-9 codes) | 250.83 (diabetes), 276, 648, etc. |
| **A1Cresult** | Glycated hemoglobin (diabetes control) | ">7", "Normal", "None" |
| **max_glu_serum** | Maximum serum glucose | ">200", "Normal", "None" |
| **num_lab_procedures** | Number of lab tests performed | 41, 59, 11 |
| **num_procedures** | Number of medical procedures | 0, 5, 1 |
| **num_medications** | Number of medications prescribed | 1, 18, 13 |

### Treatment Features
| Column | Meaning | Values |
|--------|---------|--------|
| **metformin** | Metformin prescription status | "No", "Steady", "Up", "Down" |
| **insulin** | Insulin prescription status | "No", "Steady", "Up", "Down" |
| **diabetesMed** | Any diabetes medication prescribed? | Yes, No |
| **change** | Diabetes medications changed? | "Ch" (changed), "No" |

### Patient History (Prior Year)
| Column | Meaning | Example |
|--------|---------|--------|
| **number_outpatient** | Outpatient visits in prior year | 0, 2, 1 |
| **number_emergency** | Emergency visits in prior year | 0, 2 |
| **number_inpatient** | Inpatient visits in prior year | 0, 1, 2 |

### Missing Values
- These columns use "?" to denote missing data: `weight`, `payer_code`, `medical_specialty`, `diag_1/2/3`, `max_glu_serum`, `A1Cresult`
- During cleaning, "?" was converted to `NaN`, then filled with `0` (numeric) or `"Unknown"` (categorical)

### Key Insights for Your Project
1. **Patient Journey**: `patient_nbr` + `encounter_id` tracks a patient's multiple hospital visits
2. **Hospital Performance**: `time_in_hospital` + `readmitted` are core KPIs
3. **Resource Usage**: `num_lab_procedures`, `num_procedures`, `num_medications` show hospital workload
4. **Risk Prediction**: Use demographics + clinical features + history to predict `readmitted`
5. **Power BI Dashboard**: Visualize average stay length, readmission rates, by hospital/department
