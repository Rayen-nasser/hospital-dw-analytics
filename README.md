# Hospital Data Warehouse Analytics

## Overview
The **Hospital Data Warehouse Analytics** project is a comprehensive end-to-end data pipeline and analytics solution focused on hospital performance, patient flow, and readmission risk prediction.

This project encompasses everything from extracting raw health data from Kaggle, processing and transforming it using an ETL pipeline, and deploying a Machine Learning model as a FastAPI service for real-time predictions. The insights derived from the data are also intended to be visualized in Power BI dashboards.

## Features
- **ETL Pipeline**: Extracts hospital dataset (e.g., Diabetes patient records), cleans missing or invalid values, and transforms it for analytical and predictive modeling.
- **Machine Learning**: Features a trained classification model to predict 30-day patient readmission risk (`readmission_model.pkl`).
- **FastAPI Service**: A real-time REST API that accepts patient parameters and returns a readmission risk probability.
- **CI/CD Integration**: Automated workflows with GitHub Actions (`ci_cd.yml`) to ensure continuous integration.
- **Data Analytics**: Designed to integrate with Data Warehouse solutions (SQL Server/Azure) and Power BI for reporting.

## Project Structure
```text
hospital-dw-analytics/
├── data/
│   ├── raw/           # Raw datasets downloaded from Kaggle
│   └── ...            # Cleaned and transformed datasets
├── docs/              # Detailed project documentation
├── model/             # Serialized ML models (.pkl)
├── reports/           # Power BI dashboards and reports
├── src/
│   ├── etl/           # ETL (Extract, Transform, Load) scripts
│   ├── load/          # Data loading to warehouse/database
│   └── ml/            # Machine learning model API and training scripts
├── tests/             # Unit tests
├── .github/workflows/ # CI/CD pipelines
├── requirements.txt   # Python dependencies
└── README.md          # Project overview
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- [Kaggle API credentials](https://github.com/Kaggle/kaggle-api) (for dataset downloading)
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:Rayen-nasser/hospital-dw-analytics.git
   cd hospital-dw-analytics
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

The Machine Learning Readmission Risk API is built with FastAPI. To start the local development server:

```bash
uvicorn src.ml.api:app --reload
```

The API will be available at `http://localhost:8000`. You can explore the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## Documentation
For more detailed information regarding the individual components, please refer to the files located in the `docs/` folder:
- `docs/project_setup.md`: Initial project setup and architecture details.
- `docs/api.md`: API endpoints documentation.
- `docs/clean_data.md` & `docs/transform_data.md`: ETL process specifics.
