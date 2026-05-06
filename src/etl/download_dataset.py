#!/usr/bin/env python3
"""
Download the Diabetes 130-US Hospitals (1999-2008) dataset from Kaggle
and save it to data/raw/diabetes.csv
"""
import os
import sys
import kaggle

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    out_path = os.path.join(raw_dir, "diabetes.csv")

    try:
        # Authenticate (requires ~/.kaggle/kaggle.json)
        kaggle.api.dataset_download_files(
            "brandao/diabetes",
            path=raw_dir,
            unzip=True,
            force=True
        )

        # Kaggle API saves the file as "diabetic_data.csv" in this dataset
        src = os.path.join(raw_dir, "diabetic_data.csv")
        if os.path.exists(src):
            os.replace(src, out_path)
            print(f"Dataset downloaded and saved to: {out_path}")
            print(f"Rows: {sum(1 for _ in open(out_path)) - 1}")
        else:
            # fallback: try listing downloaded files
            candidates = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
            if candidates:
                print(f"Found CSV(s): {candidates}")
            else:
                print("Warning: CSV not found after download. Check Kaggle authentication.")
                sys.exit(1)

    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Make sure ~/.kaggle/kaggle.json is present and valid.")
        sys.exit(1)

if __name__ == "__main__":
    main()
