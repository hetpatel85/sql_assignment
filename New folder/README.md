# Hospital Readmission Analysis: Diabetic Patients

A data analysis project that finds which diabetic patients are most likely to return to hospital within 30 days of discharge, using MySQL, pandas, Plotly/Cufflinks and Streamlit.

## The problem

When a diabetic patient is readmitted within 30 days of leaving hospital, it harms the patient and costs the hospital money. This project analyses about 100,000 hospital visits from 130 US hospitals to find the patient details, hospital-stay patterns and treatments linked to early readmission, so hospitals know which patients need extra follow-up.

### Questions answered

1. What percentage of visits end in a 30-day readmission, and how does it change with age?
2. Is the length of the hospital stay related to early readmission?
3. Are patients with more previous inpatient visits more likely to come back?
4. Does the discharge destination (home, care facility, etc.) matter?
5. How do diabetes treatment factors (A1C testing, insulin changes, number of medications) relate to readmission?
6. Which primary diagnoses have the highest readmission rates?

## Dataset

**Diabetes 130-US hospitals for years 1999–2008**, from the UCI Machine Learning Repository (also on Kaggle).

- `diabetic_data.csv`: 101,766 hospital visits, 50 columns
- `IDs_mapping.csv`: descriptions for the admission type, discharge destination and admission source ID codes

Main columns used:

| Column | Meaning |
|---|---|
| `encounter_id`, `patient_nbr` | Visit ID and patient ID |
| `race`, `gender`, `age` | Patient details (age in 10-year bands) |
| `admission_type_id`, `discharge_disposition_id`, `admission_source_id` | How the patient arrived and where they went after discharge |
| `time_in_hospital` | Length of stay in days (1–14) |
| `num_lab_procedures`, `num_procedures`, `num_medications` | Tests, procedures and medications during the visit |
| `number_outpatient`, `number_emergency`, `number_inpatient` | Visits of each type in the previous year |
| `diag_1`, `diag_2`, `diag_3` | Primary and secondary diagnoses (ICD-9 codes) |
| `max_glu_serum`, `A1Cresult` | Blood sugar test results (`None` = test not done) |
| `metformin` … `insulin` (23 columns) | Whether each diabetes drug was given and whether the dose changed |
| `change`, `diabetesMed` | Any medication change / any diabetes medication |
| `readmitted` | Target: `<30` days, `>30` days, or `NO` |

## Project structure

```
readmission-project/
├── config.py                  MySQL connection settings (edit your password here)
├── load_data.py               Creates the database and loads the CSV into MySQL
├── app.py                     Streamlit dashboard
├── requirements.txt           Python libraries
├── README.md                  This file
├── .streamlit/config.toml     Dashboard colours
├── data/
│   ├── diabetic_data.csv
│   └── IDs_mapping.csv
├── sql/
│   ├── create_database.sql    Creates the database, 3 lookup tables and the main table
│   └── verify_and_explore.sql Checks the load and answers some questions in SQL
└── notebooks/
    └── analysis.ipynb         Cleaning, analysis, visuals and observations
```

## How to run

**Requirements:** Python 3.10 or newer, and MySQL Server 8 running on your computer.

1. **Install the libraries** (run in the project folder):
   ```
   python -m pip install -r requirements.txt
   ```

2. **Set your MySQL password** in `config.py`:
   ```python
   "password": "YOUR_MYSQL_PASSWORD",
   ```

3. **Create the database and load the data:**
   ```
   python load_data.py
   ```
   This runs `sql/create_database.sql`, loads all 101,766 rows into MySQL, and prints verification checks. (You can also run the SQL file in MySQL Workbench first.)

4. **Run the analysis notebook:** open `notebooks/analysis.ipynb` in VS Code or Jupyter, select your Python kernel, and click **Run All**. The last section saves the cleaned data to a new MySQL table, `encounters_clean`.

5. **Start the dashboard:**
   ```
   streamlit run app.py
   ```
   It opens in your browser at `http://localhost:8501`.

Optional: open `sql/verify_and_explore.sql` in MySQL Workbench to see verification checks and SQL-only analysis.

## Database design

| Table | Rows | Purpose |
|---|---|---|
| `patient_encounters` | 101,766 | Raw visits, loaded from the CSV (`?` stored as NULL) |
| `admission_types` | 8 | Lookup: admission type ID → description |
| `discharge_dispositions` | 30 | Lookup: discharge ID → description |
| `admission_sources` | 25 | Lookup: admission source ID → description |
| `encounters_clean` | 99,340 | Cleaned data created by the notebook and used by the dashboard |

## Cleaning steps

- Dropped `weight` (97% missing) and `payer_code` (40% missing)
- Filled missing `race` and `medical_specialty` with "Unknown"
- Removed 3 rows with invalid gender
- Removed 2,423 visits where the patient died or went to hospice (they cannot be readmitted)
- Checked for duplicates (none found)
- Kept outliers such as high medication counts, since they are medically real
- Created new columns: readable age group, 30-day readmission flag, disease group from ICD-9 codes, grouped discharge destination and admission type, A1C tested flag, total prior visits

## Key findings

1. About **1 in 9 visits (11.4%)** ends in a readmission within 30 days.
2. **Previous inpatient stays are the strongest warning sign:** 8.6% readmission with none in the previous year vs **37.1% with 5 or more**.
3. Patients discharged to a **care or rehab facility (16.5%)** or **another hospital (16.0%)** return more often than those sent **home (9.3%)**.
4. Readmission rises with **length of stay**, from 8.4% (1 day) to about 14–15% (8–10 days).
5. **Insulin dose changes** (up 13.3%, down 14.2%) carry more risk than no insulin (10.2%).
6. The **A1C test was skipped in 83% of visits**; tested patients had lower readmission (9.8–10.2% vs 11.7%).
7. Patients admitted **for diabetes itself** have the highest diagnosis-group rate (13.1%).
8. **Gender makes almost no difference** (11.5% vs 11.3%).

## Recommendations

- Automatically flag patients with 2+ inpatient stays in the past year for a follow-up within a week of discharge.
- Improve discharge hand-offs to rehab and nursing facilities.
- Make A1C testing standard for diabetic admissions.
- Give extra support to patients whose insulin dose changed.

## Dashboard features

- Five key metrics at the top (visits, unique patients, 30-day readmission rate compared with all patients, average stay, average medications)
- Sidebar filters: age group, gender, admission type, discharge destination, primary diagnosis, days in hospital, A1C test
- Tabs: Overview, History and stay, Treatment, Key findings, Data (with CSV download)

## Limitations

- The data is from 1999–2008, so current hospital practice may differ.
- Findings are associations, not proof of cause.
- Some patients appear many times, which gives frequent visitors more weight.

## Future work

- **Machine learning:** combine all factors into one risk score per patient (e.g. XGBoost, explained with SHAP).
- **Generative AI:** use a language model to turn each risk score into a plain-language summary for doctors and patients.

## Tech stack

MySQL · Python · pandas · NumPy · SQLAlchemy / PyMySQL · Plotly · Cufflinks · Streamlit

## Data citation

Strack, B., DeShazo, J. P., Gennings, C., Olmo, J. L., Ventura, S., Cios, K. J., & Clore, J. N. (2014). *Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records.* BioMed Research International. Dataset available from the UCI Machine Learning Repository.
