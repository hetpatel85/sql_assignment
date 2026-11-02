"""
export_clean_data.py
--------------------
Saves the cleaned MySQL table `encounters_clean` to data/encounters_clean.parquet.

Why: the live website (Streamlit Community Cloud) cannot reach the MySQL running
on your laptop, so the dashboard reads this file there instead.
Parquet is a compressed table format: much smaller than CSV and keeps the column types.

Run once from the project folder, after running notebooks/analysis.ipynb:
    python export_clean_data.py
"""

from pathlib import Path

import pandas as pd

from config import get_engine

OUTPUT = Path(__file__).resolve().parent / "data" / "encounters_clean.parquet"

df = pd.read_sql("SELECT * FROM encounters_clean", get_engine())
df.to_parquet(OUTPUT, index=False)

print(f"Saved {len(df):,} rows and {df.shape[1]} columns to {OUTPUT}")
print(f"File size: {OUTPUT.stat().st_size / 1_000_000:.1f} MB")
