# Download Dataset Documentation
## Project: Hospital Data Warehouse Analytics
## Task: Download Dataset (Task #1)
## Status: ✓ Completed

### 1. Dataset Selection
- **Dataset**: Diabetes 130-US Hospitals (1999-2008)
- **Kaggle URL**: https://www.kaggle.com/datasets/brandao/diabetes
- **Why this dataset**:
  - 101,766 patient encounters across 130 US hospitals
  - Contains patient flow data (admission, discharge, readmissions)
  - Includes hospital performance metrics (length of stay, procedures, diagnoses)
  - Key columns: `encounter_id`, `patient_nbr`, `time_in_hospital`, `readmitted`, demographics, clinical data

### 2. Kaggle API Setup (One-time setup required from user)
1. **Create Kaggle account**: Visit https://www.kaggle.com and sign up/log in
2. **Generate API token**:
   - Go to Account Settings → API section → Click "Create New API Token"
   - Downloaded file: `kaggle.json`
3. **Place credentials file**:
   - Windows: `C:\Users\Rayen\.kaggle\kaggle.json`
   - Create folder if it doesn't exist

### 3. Script Development
- **File**: `scripts/download_dataset.py`
- **Initial version**: Placeholder script generating dummy CSV with `patient_id` and `stay_days`
- **Final version**: Uses Kaggle API to download real dataset

#### Key code changes:
```python
# Before (placeholder):
df = pd.DataFrame({"patient_id": [1, 2, 3], "stay_days": [5, 6, 7]})

# After (Kaggle API):
import kaggle
kaggle.api.dataset_download_files(
    "brandao/diabetes",
    path=raw_dir,
    unzip=True,
    force=True
)
```

### 4. Path Correction Issue
- **Problem**: Initial script used two `..` from `scripts/` which navigated to `Documents` instead of project root
- **Error**: `FileNotFoundError` when trying to save to wrong directory
- **Fix**: Changed to single `..` to reach project root
  ```python
  # Before:
  raw_dir = os.path.join("..", "..", "data", "raw")  # Wrong
  
  # After:
  project_root = os.path.join(os.path.dirname(__file__), "..")
  raw_dir = os.path.join(project_root, "data", "raw")  # Correct
  ```

### 5. Download Results
- **Command**: `python scripts/download_dataset.py`
- **Output file**: `data/raw/diabetes.csv`
- **Dataset size**: 101,766 rows, 50 columns
- **File size**: ~19.2 MB
- **Additional files downloaded**: `description.pdf` (dataset documentation)

### 6. Verification
- Verified file exists in correct location: `data/raw/diabetes.csv`
- Confirmed row count: 101,766 rows (excluding header)
- Dataset ready for cleaning step

### 7. Task Status
- **Task #1 - Download dataset**: Marked as completed ✓
- **Next task**: Task #2 - Clean data (already completed)
- **Current task**: Task #3 - Transform data (pending)
