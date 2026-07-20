"""
Downloads the Zomato Restaurants Data dataset via kagglehub and copies the
CSV into data/zomato_restaurants.csv, where setup_bigquery.sh expects it.

Requires: pip install kagglehub
Requires Kaggle API credentials configured (kaggle.json), see kagglehub's
own docs if you haven't set that up before.
"""

import shutil
from pathlib import Path

import kagglehub

DATASET = "shrutimehta/zomato-restaurants-data"
DEST = Path(__file__).resolve().parent.parent / "data" / "zomato_restaurants.csv"


def main():
    print(f"Downloading {DATASET} via kagglehub...")
    path = kagglehub.dataset_download(DATASET)
    print("Path to dataset files:", path)

    csv_files = list(Path(path).glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            f"No CSV file found in {path}. Check the download manually and "
            f"copy the right file to {DEST} by hand."
        )
    if len(csv_files) > 1:
        print(
            f"Found multiple CSVs: {[f.name for f in csv_files]}. "
            f"Using the first one, {csv_files[0].name}. "
            f"Double-check this is the right file."
        )

    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(csv_files[0], DEST)
    print(f"Copied to {DEST}")


if __name__ == "__main__":
    main()
