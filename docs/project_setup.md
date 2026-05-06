# Project Setup Documentation
## Project: Hospital Data Warehouse Analytics
## Task: Initial Project Structure Setup

### 1. Objective
Set up a clean project structure for a data warehouse and analytics pipeline focused on patient flow and hospital performance analysis using Kaggle datasets, ETL processes, AI/ML, and Power BI dashboards.

### 2. Steps Completed

#### Step 1: Create Project Folder Structure
- **Action**: Created `hospital-dw-analytics` folder and moved all project files into it
- **Directories created**:
  - `data/raw/` - Raw datasets from Kaggle
  - `data/` - All data files (raw, processed, cleaned)
  - `src/etl/` - ETL (Extract, Transform, Load) scripts
  - `src/ml/` - Machine learning models
  - `src/load/` - Data loading to warehouse/database
  - `reports/` - Power BI dashboards and reports
  - `tests/` - Unit tests
  - `scripts/` - Utility scripts (download, clean, transform)
  - `docs/` - Documentation files

- **Files initialized**:
  - `src/etl/__init__.py`, `src/ml/__init__.py`, `src/load/__init__.py` - Python package markers
  - `tests/__init__.py` - Test package marker
  - `data/raw/placeholder.txt`, `reports/placeholder.txt` - Placeholder files

#### Step 2: Configure Dependencies (requirements.txt)
- **Initial dependencies added**:
  ```
  pandas
  scikit-learn
  pyodbc
  python-dotenv
  ```
- **Purpose**:
  - `pandas` - Data manipulation and analysis
  - `scikit-learn` - Machine learning models
  - `pyodbc` - Database connectivity (SQL Server, Azure SQL)
  - `python-dotenv` - Environment variable management

#### Step 3: Create Initial Download Script
- **File**: `scripts/download_dataset.py`
- **Initial version**: Created a placeholder script that generates dummy CSV data
- **Purpose**: Template for the actual Kaggle dataset download

#### Step 4: Add Kaggle Package
- **Action**: Added `kaggle` to requirements.txt
- **Final requirements.txt**:
  ```
  pandas
  scikit-learn
  pyodbc
  python-dotenv
  kaggle
  ```
- **Why**: Kaggle API package needed to programmatically download datasets

#### Step 5: Install Dependencies
- **Command**: `pip install -r requirements.txt`
- **Result**: All packages installed successfully (pandas, scikit-learn, pyodbc, python-dotenv, kaggle, plus dependencies)

### 3. Final Project Structure
```
hospital-dw-analytics/
├── data/
│   └── raw/           # Raw datasets
├── docs/              # Documentation
├── reports/           # Dashboards and reports
├── src/
│   ├── etl/          # ETL scripts
│   ├── load/         # Data loading scripts
│   └── ml/           # Machine learning models
├── tests/            # Unit tests
├── scripts/          # Utility scripts
├── requirements.txt  # Python dependencies
└── README.md         # Project overview (if exists)
```

### 4. Next Steps
- Task #1: Download dataset from Kaggle ✓
- Task #2: Clean data ✓
- Task #3: Transform data (pending)
