# Hospital Readmission Risk: Diabetic Patients

An end-to-end project that predicts which diabetic patients are likely to return to hospital within 30 days of discharge. It combines **data analysis**, **machine learning** and **generative AI** in one interactive dashboard.

**Live demo:** _add your Streamlit link here after deploying_

| Part | What it does | Tools |
|---|---|---|
| 1. Data analysis | Loads 101,766 hospital visits into MySQL, cleans them and finds the patterns behind early readmission | MySQL, pandas, Plotly, Cufflinks |
| 2. Machine learning | Compares 11 models and uses the best one (XGBoost) to predict each patient's readmission risk | scikit-learn, XGBoost, LightGBM, CatBoost |
| 3. Generative AI | Turns the risk score into a plain-language summary for the care team and the patient | Google Gemini API |
| Dashboard | Filters, charts, risk predictor and AI summary in one web app | Streamlit |

---

## The problem

When a diabetic patient is readmitted within 30 days of leaving hospital, it harms the patient and costs the hospital money. This project uses about 100,000 real (anonymized) hospital visits from 130 US hospitals to find which patients are at high risk, so hospitals can give them extra follow-up care before and after discharge.

### Questions answered

1. What percentage of visits end in a 30-day readmission, and how does it change with age?
2. Is the length of the hospital stay related to early readmission?
3. Are patients with more previous inpatient visits more likely to come back?
4. Does the discharge destination (home, care facility, etc.) matter?
5. How do diabetes treatment factors (A1C testing, insulin changes, number of medications) relate to readmission?
6. Which primary diagnoses have the highest readmission rates?
7. Can a machine learning model predict a patient's risk, and which model works best?

---

## Dataset

**Diabetes 130-US hospitals for years 1999–2008**, from the UCI Machine Learning Repository (also on Kaggle).

- `data/diabetic_data.csv`: 101,766 hospital visits, 50 columns
- `data/IDs_mapping.csv`: descriptions for the admission type, discharge destination and admission source codes
- `data/encounters_clean.parquet`: the cleaned data (99,340 visits), used by the live dashboard

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
| `readmitted` | Target: `<30` days, `>30` days, or `NO` |

---

## Project structure

```
├── app.py                       Streamlit dashboard (charts, risk predictor, AI summary)
├── ai_helper.py                 Generative AI: builds the prompt and calls Gemini
├── config.py                    MySQL connection (password read from secrets.toml)
├── load_data.py                 Creates the database and loads the CSV into MySQL
├── export_clean_data.py         Saves the cleaned data to a file for the live dashboard
├── requirements.txt             Python libraries
├── .gitignore                   Keeps passwords, keys and the virtual environment off GitHub
├── .streamlit/
│   ├── config.toml              Dashboard colours
│   └── secrets.toml             Your MySQL password and Gemini key (private, not uploaded)
├── data/
│   ├── diabetic_data.csv
│   ├── IDs_mapping.csv
│   └── encounters_clean.parquet
├── sql/
│   ├── create_database.sql      Database, 3 lookup tables and the main table
│   └── verify_and_explore.sql   Load checks and SQL-only analysis
└── notebooks/
    ├── analysis.ipynb           Part 1: cleaning, analysis, charts, observations
    ├── ml_model.ipynb           Part 2: Linear vs Logistic Regression
    └── model_comparison.ipynb   Part 2: 11 models compared, XGBoost saved
```

---

## How to run it on your computer

**You need:** Python 3.11 or newer and MySQL Server 8.

1. **Install the libraries** (in the project folder):
   ```
   python -m pip install -r requirements.txt
   ```
2. **Add your private settings** in `.streamlit/secrets.toml`:
   ```toml
   MYSQL_PASSWORD = "your-mysql-password"
   GEMINI_API_KEY = "your-gemini-key"    # free key from aistudio.google.com
   ```
3. **Create the database and load the data:**
   ```
   python load_data.py
   ```
4. **Run the notebooks** in order with **Run All**: `analysis.ipynb` (saves the cleaned table `encounters_clean` to MySQL), then `ml_model.ipynb` and `model_comparison.ipynb` (saves the XGBoost model).
5. **Save the backup data file** (needed for the live dashboard):
   ```
   python export_clean_data.py
   ```
6. **Start the dashboard:**
   ```
   python -m streamlit run app.py
   ```

The dashboard reads from MySQL when it is available and from `data/encounters_clean.parquet` when it isn't. If the saved model file is missing, it trains XGBoost itself in a few seconds.

---

## Part 1: Data analysis

### Database design

| Table | Rows | Purpose |
|---|---|---|
| `patient_encounters` | 101,766 | Raw visits loaded from the CSV (`?` stored as NULL) |
| `admission_types` | 8 | Lookup: admission type ID → description |
| `discharge_dispositions` | 30 | Lookup: discharge ID → description |
| `admission_sources` | 25 | Lookup: admission source ID → description |
| `encounters_clean` | 99,340 | Cleaned data created by the notebook |

### Cleaning

- Dropped `weight` (97% missing) and `payer_code` (40% missing)
- Filled missing `race` and `medical_specialty` with "Unknown"
- Removed 3 rows with invalid gender
- Removed 2,423 visits where the patient died or went to hospice, because they cannot be readmitted and would make the rate look lower than it really is
- Checked for duplicates (none found)
- Kept outliers such as high medication counts, since they are medically real
- Created new columns: readable age group, 30-day readmission flag (target), disease group from 700+ ICD-9 codes, grouped discharge destination and admission type, A1C tested flag, total prior visits

### Key findings

1. About **1 in 9 visits (11.4%)** ends in a readmission within 30 days.
2. **Previous inpatient stays are the strongest warning sign:** 8.6% readmission with none in the previous year vs **37.1% with 5 or more**.
3. Patients discharged to a **care or rehab facility (16.5%)** or **another hospital (16.0%)** return more often than those sent **home (9.3%)**.
4. Readmission rises with **length of stay**, from 8.4% (1 day) to about 14–15% (8–10 days).
5. **Insulin dose changes** (up 13.3%, down 14.2%) carry more risk than no insulin (10.2%).
6. The **A1C test was skipped in 83% of visits**; tested patients had lower readmission (9.8–10.2% vs 11.7%).
7. Patients admitted **for diabetes itself** have the highest diagnosis-group rate (13.1%).
8. **Gender makes almost no difference** (11.5% vs 11.3%).

### Recommendations

- Automatically flag patients with 2+ inpatient stays in the past year for a follow-up within a week of discharge.
- Improve discharge hand-offs to rehab and nursing facilities.
- Make A1C testing standard for diabetic admissions.
- Give extra support to patients whose insulin dose changed.

---

## Part 2: Machine learning

**Problem type:** binary classification. The target `readmitted_30` is 1 (readmitted within 30 days) or 0.

### How the models were tested fairly

- **No data leakage:** ID columns and every column that contains the answer in another form (`readmitted`, `readmit_status`) were removed from the inputs.
- **Split by patient:** one patient can have many visits, so the 80% train / 20% test split keeps each patient on one side only (`GroupShuffleSplit`). Otherwise the model would be tested on patients it had already seen.
- **Same preparation for every model:** `StandardScaler` for number columns and `OneHotEncoder` for text columns, inside a scikit-learn `Pipeline`.
- **Main score: ROC-AUC**, which measures how well a model ranks risky patients above safe ones (0.5 = guessing, 1.0 = perfect). Accuracy is misleading here: always predicting "No" already gives 88.7% accuracy, because only 11% of patients are readmitted.

### Step 1: Linear vs Logistic Regression (`ml_model.ipynb`)

| Model | Test ROC-AUC | Accuracy | Recall | Predictions below 0 |
|---|---|---|---|---|
| Linear Regression | 0.663 | 0.887 | 0.011 | 65 |
| Logistic Regression | 0.661 | 0.888 | 0.020 | 0 |

Both rank patients about equally well, but Linear Regression is built to predict numbers and gave 65 impossible negative "probabilities". Logistic Regression always outputs a valid probability between 0 and 1, so it is the right tool for a yes/no target.

### Step 2: 11 models compared (`model_comparison.ipynb`)

| Rank | Model | Test ROC-AUC | Train ROC-AUC | Train time |
|---|---|---|---|---|
| 1 | **XGBoost** | **0.675** | 0.720 | 2 s |
| 2 | CatBoost | 0.673 | 0.700 | 5 s |
| 3 | Random Forest | 0.671 | 0.800 | 52 s |
| 4 | Gradient Boosting | 0.670 | 0.677 | 14 s |
| 5 | LightGBM | 0.669 | 0.771 | 2 s |
| 6 | Linear Regression | 0.663 | 0.664 | 2 s |
| 7 | Logistic Regression | 0.661 | 0.662 | 1 s |
| 8 | AdaBoost | 0.657 | 0.655 | 18 s |
| 9 | Decision Tree (max depth 6) | 0.655 | 0.660 | 1 s |
| 10 | KNN | 0.634 | 0.710 | ~6 min to predict |
| 11 | SVM (10,000-patient sample) | 0.569 | 0.968 | 8 s |
| – | Decision Tree (no depth limit) | 0.535 | 1.000 | 14 s |

**What the comparison showed:**
- **Boosting models and Random Forest are the best group.** They combine many small trees, so they can find combinations of factors.
- **The top models are basically tied.** Re-run on 5 different patient splits, XGBoost and CatBoost averaged 0.667 and LightGBM and Random Forest 0.666, but all of them **beat Logistic Regression (0.654) on every split**.
- **Overfitting is visible:** the Decision Tree with no limit scored 1.000 on training data but 0.535 on test data, because it memorised the patients. SVM did the same.
- **KNN and SVM are a poor fit:** slow on 80,000 patients and the weakest scores.

### Final model: XGBoost

XGBoost is tied for the best test score, trains in about 2 seconds and has a small train/test gap. It powers the dashboard's **Risk predictor**.

**Risk levels**, checked on test patients the model had never seen:

| Risk level | Predicted risk | Share of patients | Actually readmitted |
|---|---|---|---|
| Low | under 8% | 37% | 5.6% |
| Medium | 8–15% | 41% | 11.0% |
| High | 15% or more | 22% | 21.5% |

Patients the model rates **High** were really readmitted almost **4 times as often** as those rated **Low**.

---

## Part 3: Generative AI

After the Risk predictor scores a patient, the **Write AI summary** button sends the result to **Google Gemini** (free plan, model `gemini-flash-latest`), which writes:

- **For the care team:** the risk level, the main reasons and practical follow-up steps
- **For the patient:** simple advice on what to watch for at home and when to call the doctor

**How the AI is kept accurate (`ai_helper.py`):**
- The prompt only contains facts from this project: the predicted risk, the average risk, and the patient's warning signs, each with the readmission rate measured in Part 1.
- The AI is told not to invent test results or diagnoses and not to prescribe medicines or doses.
- Every summary ends with a note that it is AI-generated and not medical advice.

**Privacy:** the dataset is anonymized, and only general details (age group, visit counts, etc.) are sent. On the free plan Google may use requests to improve its products, so real patient data should never be sent. In a real hospital, a model running on the hospital's own servers would keep patient data private.

---

## Dashboard features

- **Key metrics:** visits, unique patients, 30-day readmission rate (compared with all patients), average stay, average medications
- **Filters:** age group, gender, admission type, discharge destination, primary diagnosis, days in hospital, A1C test
- **Tabs:**
  - Overview, History and stay, Treatment: interactive charts from the analysis
  - Key findings: observations and recommendations
  - **Risk predictor:** enter a patient's details → risk %, risk level, warning signs and AI summary
  - Data: filtered table with CSV download

---

## Deployment (live link)

1. Run `python export_clean_data.py` so `data/encounters_clean.parquet` exists.
2. Upload the project to a GitHub repository. `.gitignore` keeps `secrets.toml`, `.venv` and model files out.
3. On [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, click **Create app**, choose the repository and set the main file to `app.py`.
4. Under **Advanced settings**, choose **Python 3.12**, and in **Secrets** paste `GEMINI_API_KEY = "your-key"`.
5. Click **Deploy**. The live app reads the backup data file (MySQL stays on your computer) and trains the XGBoost model on startup.

---

## Limitations

- The data is from 1999–2008, so current hospital practice may differ.
- Findings are associations, not proof of cause.
- All 11 models reach a ROC-AUC between about 0.65 and 0.68. Since very different models hit the same ceiling, the limit comes from the data itself. Better predictions would need extra information such as lab values or social factors.
- At the default 0.5 cutoff, every model catches only a small share of readmissions, because readmissions are rare (11%). The dashboard uses risk levels instead of a single yes/no answer.
- Some patients appear many times, which gives frequent visitors more weight.
- AI summaries can still contain mistakes and must be checked by a clinician.

## Future work

- Improve recall for the rare readmitted group.
- Explain each individual prediction with SHAP values.
- Add a RAG chatbot that answers questions from real discharge-care guidelines and shows its sources.

---

## Tech stack

MySQL · Python · pandas · NumPy · SQLAlchemy / PyMySQL · Plotly · Cufflinks · scikit-learn · XGBoost · LightGBM · CatBoost · Google Gemini API · Streamlit

## Data citation

Strack, B., DeShazo, J. P., Gennings, C., Olmo, J. L., Ventura, S., Cios, K. J., & Clore, J. N. (2014). *Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records.* BioMed Research International. Dataset available from the UCI Machine Learning Repository.

## Disclaimer

This is a learning project. It is not a medical device and must not be used to make real medical decisions.
