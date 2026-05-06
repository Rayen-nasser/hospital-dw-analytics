#!/usr/bin/env python3
"""
Clean the diabetes dataset: handle missing values, convert types, remove duplicates
"""
import pandas as pd
import os

def main():
    # Read dataset from raw directory, treating "?" as missing values
    # scripts/ is one level below project root, so one ".." gets to project root
    project_root = os.path.join(os.path.dirname(__file__), "..")
    raw_path = os.path.join(project_root, "data", "raw", "diabetes.csv")
    df = pd.read_csv(raw_path, na_values="?")

    print(f"Original rows: {len(df)}")
    print(f"Missing values per column:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

    # Handle missing values
    # Drop rows where key columns are missing
    key_cols = ["patient_nbr", "encounter_id"]
    df.dropna(subset=key_cols, inplace=True)
    print(f"Rows after dropping missing keys: {len(df)}")

    # Fill missing numeric values with 0
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Fill missing categorical values with "Unknown"
    cat_cols = df.select_dtypes(include=["object"]).columns
    df[cat_cols] = df[cat_cols].fillna("Unknown")

    # Convert data types
    df["time_in_hospital"] = df["time_in_hospital"].astype(int)
    df["readmitted"] = df["readmitted"].astype("category")
    df["patient_nbr"] = df["patient_nbr"].astype(int)
    df["encounter_id"] = df["encounter_id"].astype(int)

    # Remove duplicates based on patient_nbr and encounter_id
    before_dedup = len(df)
    df.drop_duplicates(subset=["patient_nbr", "encounter_id"], inplace=True)
    print(f"Rows after removing duplicates: {len(df)} (removed {before_dedup - len(df)})")

    # Save cleaned dataset
    cleaned_path = os.path.join(project_root, "data", "raw", "cleaned_diabetes.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"\nCleaned dataset saved to: {cleaned_path}")
    print(f"Final rows: {len(df)}")

if __name__ == "__main__":
    main()