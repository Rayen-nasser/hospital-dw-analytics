#!/usr/bin/env python3
"""
Train a readmission risk model using the transformed diabetes dataset.
Outputs a serialized model at model/readmission_model.pkl.
"""
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import joblib

def main():
    # Path to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(project_root, "data", "raw", "transformed_diabetes.csv")
    model_dir = os.path.join(project_root, "model")
    os.makedirs(model_dir, exist_ok=True)

    # Load data
    df = pd.read_csv(data_path)

    # Target variable: binary readmission within 30 days
    target = "readmitted_binary"
    y = df[target]
    X = df.drop(columns=[target])

    # Drop identifiers that shouldn't be used for modeling
    X = X.drop(columns=["encounter_id", "patient_nbr"], errors="ignore")

    # Identify column types
    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

    # Preprocess: impute missing, scale numeric, one‑hot encode categoricals
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # Model: Random Forest (good baseline, handles mixed data well)
    clf = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )

    # Build pipeline
    model = Pipeline(steps=[("preprocess", preprocessor), ("clf", clf)])

    # Train‑test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Fit model
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    print(f"Accuracy: {acc:.4f}")
    print(f"ROC AUC: {auc:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    # Save the pipeline
    model_path = os.path.join(model_dir, "readmission_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")

if __name__ == "__main__":
    main()
