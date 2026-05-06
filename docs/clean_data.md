# Data Cleaning Documentation
## Project: Hospital Data Warehouse Analytics
## Dataset: Diabetes 130-US Hospitals (1999-2008)
## Task: Clean Data (Task #2)

### 1. Dataset Overview
- **Source**: Kaggle (brandao/diabetes)
- **Original size**: 101,766 rows, 50 columns
- **Key columns**: `encounter_id`, `patient_nbr`, `time_in_hospital`, `readmitted`, demographic and clinical features
- **Missing value marker**: "?" (required special handling during import)

### 2. Cleaning Steps & Explanations

#### Step 2.1: Data Import with Missing Value Handling
- **Action**: Read `diabetes.csv` using pandas with `na_values="?"` to treat all "?" entries as NaN (missing values)
- **Why**: The dataset uses "?" to denote missing data; without this flag, these would be treated as strings, causing type errors later
- **Issue fixed**: Initial script didn't specify missing value marker, leading to incorrect data types

#### Step 2.2: Missing Value Treatment
- **Numeric columns** (e.g., `time_in_hospital`, `num_lab_procedures`): Filled with `0`
  - *Why*: These are count/integer columns where 0 is a valid placeholder for missing numeric data
- **Categorical columns** (e.g., `race`, `payer_code`, `diag_1`): Filled with `"Unknown"`
  - *Why*: Categorical data requires a valid string value for analysis; "Unknown" preserves the missing status while allowing processing
- **Key columns** (`patient_nbr`, `encounter_id`): No missing values found, so no rows dropped

- **Missing value counts (before cleaning)**:
  | Column | Missing Count |
  |--------|---------------|
  | max_glu_serum | 96,420 |
  | A1Cresult | 84,748 |
  | weight | 98,569 |
  | payer_code | 40,256 |
  | medical_specialty | 49,949 |
  | race | 2,273 |
  | diag_3 | 1,423 |
  | diag_2 | 358 |
  | diag_1 | 21 |

#### Step 2.3: Data Type Conversion
- `time_in_hospital` → int: Length of hospital stay should be integer
- `readmitted` → category: Binary/categorical variable (No/<30/>30)
- `patient_nbr`, `encounter_id` → int: ID columns should be numeric integers
- **Why**: Correct data types are required for accurate analysis, modeling, and database loading

#### Step 2.4: Duplicate Removal
- **Action**: Removed duplicates based on `patient_nbr` + `encounter_id` (unique encounter identifier)
- **Result**: 0 duplicates found, so no rows removed
- **Why**: Each row should represent a unique hospital encounter; duplicates would skew analysis

#### Step 2.5: Output Path Correction
- **Issue**: Initial script saved cleaned data to wrong directory (due to incorrect relative path: two `..` from `scripts/` instead of one)
- **Fix**: Adjusted path to use single `..` from `scripts/` to reach project root, then `data/raw/`
- **Result**: Cleaned dataset saved to correct location: `data/raw/cleaned_diabetes.csv`

### 3. Cleaning Results
- **Original rows**: 101,766
- **Final rows**: 101,766 (no rows dropped, 0 duplicates)
- **Output file**: `data/raw/cleaned_diabetes.csv` (20.8 MB)
- **Status**: Task #2 marked as completed

### 4. Next Steps
- Proceed to Task #3: Transform data (derive metrics, enrich dataset)
- Load cleaned data to warehouse for Power BI integration
