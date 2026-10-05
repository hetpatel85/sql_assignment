# Project Guide: How It Works and How to Explain It

This guide is for **you**, not for submission. Read it tonight so you can run the project and answer questions about it confidently.

---

## 1. The project in one minute

> "Hospitals lose money and patients suffer when diabetic patients come back within 30 days of discharge. I took 100,000 real hospital visits, loaded them into MySQL, cleaned and analysed them with pandas, and visualised the results with Plotly and Cufflinks. I found that the strongest warning sign is previous hospital stays: patients with 5 or more stays in the past year were readmitted 37% of the time, compared with 9% for patients with none. Discharge destination, length of stay and insulin changes also matter. I built a Streamlit dashboard so anyone can filter the data and explore these patterns."

Practise saying this out loud a few times.

---

## 2. How the pieces connect

```
 diabetic_data.csv
        │
        ▼   load_data.py  (runs create_database.sql, then inserts the rows)
 MySQL: patient_encounters  + 3 lookup tables
        │
        ▼   analysis.ipynb  (reads with a SQL JOIN → pandas)
 Cleaning → Analysis → Charts → Observations
        │
        ▼   last notebook cell saves the result
 MySQL: encounters_clean
        │
        ▼   app.py  (reads encounters_clean)
 Streamlit dashboard in the browser
```

**Why MySQL in the middle?** In real companies, data lives in databases, not CSV files. Loading it into MySQL first shows you can work the way a real data team does. Saving the cleaned table back to MySQL means the dashboard and the notebook always use the same clean data.

---

## 3. What each file does

**`config.py`**: Holds the MySQL login details in one place. `get_engine()` creates a SQLAlchemy "engine", which is the object that opens connections to MySQL. All other files import it, so you only change your password once.

**`sql/create_database.sql`**: Creates the database `hospital_readmission` and 4 tables. The 3 small lookup tables translate ID numbers into words (1 → "Emergency"). Things to mention:
- `encounter_id` is the **PRIMARY KEY** (unique for every visit)
- **Indexes** on `patient_nbr`, `readmitted` and `age` make filtering faster
- The column `change` was renamed `med_change` because CHANGE is a reserved word in MySQL

**`load_data.py`**: Runs the SQL file, reads the CSV with pandas (turning `?` into NULL), renames columns to match the table, inserts all rows with `to_sql()` in chunks of 5,000, then checks the row count, sample rows and NULL counts.

**`sql/verify_and_explore.sql`**: Queries to run in MySQL Workbench. Part A checks the load. Part B answers questions using `GROUP BY`, `AVG()`, and `JOIN`.

**`notebooks/analysis.ipynb`**: The main analysis. Sections: setup → load from MySQL → first look → cleaning → analysis and charts with an observation under each → save clean data → key observations → recommendations → limitations.

**`app.py`**: The dashboard. Loads `encounters_clean` once (cached), applies sidebar filters, shows 5 metrics and 11 charts across 5 tabs.

---

## 4. Key ideas you should understand

**30-day readmission rate.** We created a column `readmitted_30` that is 1 if the patient came back within 30 days and 0 if not. The *average* of a 0/1 column is the percentage of 1s. So `df.groupby("age_group")["readmitted_30"].mean()` gives the readmission rate for each age group. This one trick powers almost every chart.

**Why we removed patients who died or went to hospice.** They can never be readmitted, so leaving them in would make readmission rates look lower than they really are.

**Why we kept outliers.** A patient with 81 medications is unusual but medically real. Removing such patients would hide the complex cases hospitals care about most.

**Why ICD-9 grouping.** The diagnosis column has 700+ different codes. Grouping them into 9 disease groups (Circulatory, Respiratory, Diabetes, etc.) makes the pattern readable.

**Correlation.** A number from -1 to 1 showing how two columns move together. The highest with readmission is `number_inpatient` at 0.17, which is weak. That means no single factor explains readmission, and a combination of factors (a machine learning model) is the logical next step.

**Pandas vs Cufflinks vs Plotly.** Pandas does the calculations. Plotly draws interactive charts. Cufflinks is a shortcut that lets you call `.iplot()` directly on a pandas table to get a Plotly chart. In the notebook, `asFigure=True` returns the chart as a Plotly figure so we can add things like the average line and then call `fig.show()`.

**Streamlit caching.** `@st.cache_data` stores the loaded data so MySQL is not queried every time a filter changes, which keeps the dashboard fast.

---

## 5. Run checklist for tomorrow

Do this **tonight** so there are no surprises.

1. Open the `readmission-project` folder in VS Code (File → Open Folder).
2. Open the terminal (View → Terminal) and install everything:
   ```
   python -m pip install -r requirements.txt
   ```
   Using `python -m pip` makes sure the libraries go into the same Python that runs your code (this avoids the "No module named pandas" problem you had).
3. Put your MySQL password in `config.py`.
4. Make sure MySQL is running, then:
   ```
   python load_data.py
   ```
   You should see `Row count in MySQL: 101,766`.
5. Open `notebooks/analysis.ipynb`, click **Select Kernel** (top right) and pick the same Python, then click **Run All**. The last code cell should say `Saved 99,340 rows to MySQL table 'encounters_clean'`.
6. In the terminal:
   ```
   streamlit run app.py
   ```
   The dashboard opens in your browser. Try a few filters.
7. Optional: open `sql/verify_and_explore.sql` in MySQL Workbench and run it.

---

## 6. If something goes wrong

| Error | Fix |
|---|---|
| `No module named 'pandas'` (or any module) in the notebook | Run `%pip install -r ../requirements.txt` in a notebook cell, then click Restart |
| `Access denied for user 'root'` | The password in `config.py` is wrong |
| `Can't connect to MySQL server` | MySQL isn't running. On Windows: press Win+R, type `services.msc`, find MySQL80, click Start |
| `cryptography package is required` | `python -m pip install cryptography` |
| `Invalid value ... np.float64(1.0)` or `titlefont` error | Plotly version is wrong: `python -m pip install plotly==5.24.1` |
| Charts don't show in the VS Code notebook | `python -m pip install nbformat`, then restart the kernel |
| Dashboard says it cannot read `encounters_clean` | Run the whole notebook first; its last section creates that table |
| `streamlit` is not recognised | Use `python -m streamlit run app.py` |

---

## 7. Questions you might be asked

**Why did you choose this project?**
Hospital readmission is a real, expensive problem, and the dataset is large, real and messy, which gave me practice with real cleaning decisions.

**What was the hardest part of cleaning?**
Deciding what to do with each problem: dropping columns that were 97% empty, removing patients who died, translating "None" into "Not tested" for the A1C test, and grouping 700+ diagnosis codes.

**What is your most important finding?**
Previous inpatient stays. Patients with 5 or more stays in the past year were readmitted 37.1% of the time vs 8.6% for those with none, more than four times higher.

**Does doing the A1C test *cause* fewer readmissions?**
Not necessarily. It's an association. It could be that hospitals that test more also give better care in general. Proving cause would need a controlled study.

**Why is the readmission rate 11.4% and not 11.2% like the raw data?**
I removed 2,423 visits where the patient died or went to hospice, because they can't be readmitted. That makes the rate more accurate.

**Why use MySQL instead of just reading the CSV?**
Real company data lives in databases. It also let me use JOINs with the lookup tables and share one clean table between the notebook and the dashboard.

**What are the limitations?**
Old data (1999–2008), associations not causes, and frequent patients appear many times.

**What would you do next?**
Build a machine learning model (like XGBoost) to give every patient one risk score, since no single factor is strong on its own, then use generative AI to explain each score in plain language for doctors.

---

## 8. Where each workflow step lives

| Workflow step | Where it's done |
|---|---|
| 1. Finalise the idea | README "The problem" and the notebook's first cell |
| 2. Identify the dataset | README "Dataset" (source + column descriptions) |
| 3. Load into MySQL | `sql/create_database.sql`, `load_data.py`, `sql/verify_and_explore.sql` |
| 4. Analysis in notebook | `notebooks/analysis.ipynb` sections 2–5 |
| 5. Observations | Under every chart, plus sections 7–9 of the notebook |
| 6. Streamlit app | `app.py` |
| Deliverables 1–5 | SQL scripts, notebook, `app.py`, `requirements.txt`, `README.md` |
