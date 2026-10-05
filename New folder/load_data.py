"""
load_data.py
------------
Workflow Step 3: Load the dataset into MySQL.

What this script does:
  1. Runs sql/create_database.sql  (creates the database + tables)
  2. Reads data/diabetic_data.csv with pandas
  3. Renames columns so they match the MySQL table
  4. Inserts all rows into the patient_encounters table
  5. Runs verification queries (row count, sample rows, null checks)

Run it from the project folder:
    python load_data.py
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from config import get_engine

PROJECT_DIR = Path(__file__).resolve().parent
CSV_PATH = PROJECT_DIR / "data" / "diabetic_data.csv"
SQL_PATH = PROJECT_DIR / "sql" / "create_database.sql"


def run_sql_file(path: Path) -> None:
    """Run every statement in a .sql file, one at a time."""
    engine = get_engine(with_database=False)   # database may not exist yet

    # Remove comment lines, then split the file into single statements
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
             if not ln.strip().startswith("--")]
    statements = [s.strip() for s in "\n".join(lines).split(";") if s.strip()]

    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
    print(f"[1/4] Ran {len(statements)} SQL statements from {path.name}")


def read_and_prepare_csv(path: Path) -> pd.DataFrame:
    """Read the CSV and make the columns match the MySQL table."""
    # In this dataset a missing value is written as '?'.
    # keep_default_na=False stops pandas from turning the text "None"
    # (which means "test not done" in this data) into a missing value.
    df = pd.read_csv(path, na_values=["?"], keep_default_na=False,
                     low_memory=False)

    df.columns = (df.columns
                  .str.replace("-", "_", regex=False)
                  .str.strip())
    df = df.rename(columns={
        "A1Cresult": "a1c_result",
        "diabetesMed": "diabetes_med",
        "change": "med_change",          # CHANGE is a reserved word in MySQL
    })

    print(f"[2/4] Read {len(df):,} rows and {df.shape[1]} columns from {path.name}")
    return df


def load_into_mysql(df: pd.DataFrame) -> None:
    """Insert the DataFrame into the existing patient_encounters table."""
    engine = get_engine()
    df.to_sql(
        "patient_encounters",
        con=engine,
        if_exists="append",   # table already exists (created by the SQL file)
        index=False,
        chunksize=5000,       # send 5,000 rows at a time
        method="multi",
    )
    print(f"[3/4] Inserted {len(df):,} rows into patient_encounters")


def verify_load() -> None:
    """Basic checks to confirm the data arrived correctly."""
    engine = get_engine()
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM patient_encounters")).scalar()
        print(f"[4/4] Verification\n      Row count in MySQL: {total:,}")

        sample = pd.read_sql(
            "SELECT encounter_id, age, gender, time_in_hospital, readmitted "
            "FROM patient_encounters LIMIT 5", conn)
        print("\n      Sample rows:\n", sample.to_string(index=False))

        nulls = pd.read_sql("""
            SELECT
                SUM(race IS NULL)              AS race_nulls,
                SUM(weight IS NULL)            AS weight_nulls,
                SUM(payer_code IS NULL)        AS payer_code_nulls,
                SUM(medical_specialty IS NULL) AS specialty_nulls,
                SUM(diag_1 IS NULL)            AS diag_1_nulls
            FROM patient_encounters""", conn).astype(int)
        print("\n      NULL counts:\n", nulls.to_string(index=False))


if __name__ == "__main__":
    if not CSV_PATH.exists():
        raise SystemExit(f"CSV not found: {CSV_PATH}\n"
                         "Download diabetic_data.csv and put it in the data/ folder.")
    run_sql_file(SQL_PATH)
    data = read_and_prepare_csv(CSV_PATH)
    load_into_mysql(data)
    verify_load()
    print("\nDone! The data is now in MySQL.")
