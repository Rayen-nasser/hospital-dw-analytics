#!/usr/bin/env python3
"""
Transform the cleaned diabetes dataset: create derived metrics and enrich data
"""
import pandas as pd
import os

def main():
    # Read cleaned dataset
    project_root = os.path.join(os.path.dirname(__file__), "..")
    cleaned_path = os.path.join(project_root, "data", "raw", "cleaned_diabetes.csv")
    df = pd.read_csv(cleaned_path)

    print(f"Original rows: {len(df)}")
    print(f"Original columns: {len(df.columns)}")

    # 1. Length of stay categories
    def categorize_stay(days):
        if days <= 3:
            return "Short"
        elif days <= 7:
            return "Medium"
        else:
            return "Long"

    df["stay_category"] = df["time_in_hospital"].apply(categorize_stay)

    # 2. Readmission target (binary for ML)
    df["readmitted_binary"] = df["readmitted"].apply(lambda x: 1 if x == "<30" else 0)

    # 3. Patient complexity score
    df["complexity_score"] = df["num_lab_procedures"] + df["num_procedures"] + df["num_medications"]

    # 4. Prior utilization score
    df["prior_utilization"] = df["number_outpatient"] + df["number_emergency"] + df["number_inpatient"]

    # 5. Age numeric (convert age groups to midpoints)
    age_map = {
        "[0-10)": 5, "[10-20)": 15, "[20-30)": 25, "[30-40)": 35,
        "[40-50)": 45, "[50-60)": 55, "[60-70)": 65, "[70-80)": 75,
        "[80-90)": 85, "[90-100)": 95
    }
    df["age_numeric"] = df["age"].map(age_map)

    # 6. Clinical indicators - convert to numeric
    a1c_map = {">7": 8, "Normal": 6, "None": 0, "Unknown": -1}
    df["A1Cresult_numeric"] = df["A1Cresult"].map(a1c_map)

    glu_map = {">200": 250, ">300": 350, "Normal": 100, "None": 0, "Unknown": -1}
    df["max_glu_serum_numeric"] = df["max_glu_serum"].map(glu_map)

    # 7. Medication intensity (count active diabetes medications)
    med_cols = ["metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride",
                "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone",
                "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide",
                "examide", "citoglipton", "insulin", "glyburide-metformin",
                "glipizide-metformin", "glimepiride-pioglitazone",
                "metformin-rosiglitazone", "metformin-pioglitazone"]

    df["medication_count"] = df[med_cols].apply(lambda row: sum(1 for v in row if v != "No"), axis=1)

    # 8. Readmission risk category (multiclass target)
    df["readmission_risk"] = df["readmitted"].map({"NO": "Low", "<30": "High", ">30": "Medium"})

    # 9. Patient encounter count (how many times same patient visited)
    patient_encounter_count = df.groupby("patient_nbr")["encounter_id"].count().reset_index()
    patient_encounter_count.columns = ["patient_nbr", "patient_encounter_count"]
    df = df.merge(patient_encounter_count, on="patient_nbr", how="left")

    # Save transformed dataset
    transformed_path = os.path.join(project_root, "data", "raw", "transformed_diabetes.csv")
    df.to_csv(transformed_path, index=False)

    print(f"\nTransformed dataset saved to: {transformed_path}")
    print(f"Final rows: {len(df)}")
    print(f"Final columns: {len(df.columns)}")
    print(f"\nNew derived columns added:")
    original_cols = pd.read_csv(cleaned_path, nrows=1).columns
    new_cols = [col for col in df.columns if col not in original_cols]
    for col in new_cols:
        print(f"  - {col}")

if __name__ == "__main__":
    main()