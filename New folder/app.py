"""
app.py
------
Workflow Step 6: Streamlit dashboard for the hospital readmission analysis.

Reads the cleaned table `encounters_clean` from MySQL
(created by the last section of notebooks/analysis.ipynb).

Run from the project folder:
    streamlit run app.py
"""

from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text

import ai_helper
from config import get_engine

# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(page_title="Diabetic Readmission Dashboard",
                   page_icon="🏥", layout="wide")

BLUE, RED, GREY = "#1F5A85", "#C0392B", "#8A99A8"
OUTCOME_COLORS = {"Within 30 days": RED, "After 30 days": BLUE, "Not readmitted": GREY}
AGE_ORDER = ["0-10", "10-20", "20-30", "30-40", "40-50",
             "50-60", "60-70", "70-80", "80-90", "90-100"]


# ------------------------------------------------------------------
# Data loading (cached so MySQL is queried only once)
# ------------------------------------------------------------------
@st.cache_resource
def connect():
    return get_engine()


BACKUP_DATA = Path(__file__).resolve().parent / "data" / "encounters_clean.parquet"


@st.cache_data(show_spinner="Loading data...")
def load_data():
    """
    Read the cleaned data from MySQL. If MySQL is not available (for example on the
    live website, which cannot reach the MySQL on your laptop), read the backup copy
    data/encounters_clean.parquet made by export_clean_data.py.
    Returns the data and where it came from.
    """
    try:
        with connect().connect() as conn:
            return pd.read_sql(text("SELECT * FROM encounters_clean"), conn), "MySQL"
    except Exception:
        if BACKUP_DATA.exists():
            return pd.read_parquet(BACKUP_DATA), "backup file"
        raise


MODEL_PATH = Path(__file__).resolve().parent / "models" / "xgboost_model.joblib"


@st.cache_resource(show_spinner="Preparing the prediction model...")
def load_model(_data):
    """
    Load the XGBoost model saved by model_comparison.ipynb.
    If the file is missing or can't be loaded (for example on the live website),
    train the same XGBoost model here from the data. It only takes a few seconds,
    and cache_resource makes sure it happens just once.
    """
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass

    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from xgboost import XGBClassifier

    drop_cols = ["encounter_id", "patient_nbr", "readmitted", "readmit_status",
                 "readmitted_30", "a1c_tested"]
    X = _data.drop(columns=drop_cols)
    y = _data["readmitted_30"]
    num_cols = X.select_dtypes(include="number").columns.tolist()
    cat_cols = X.select_dtypes(exclude="number").columns.tolist()
    X[cat_cols] = X[cat_cols].fillna("Unknown")

    prep = ColumnTransformer([("num", StandardScaler(), num_cols),
                              ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)])
    model = Pipeline([("prep", prep),
                      ("model", XGBClassifier(n_estimators=300, learning_rate=0.05,
                                              max_depth=5, random_state=42, n_jobs=-1))])
    return model.fit(X, y)


try:
    data, data_source = load_data()
except Exception as err:
    st.error(
        "Could not read the table `encounters_clean` from MySQL, "
        "and no backup file data/encounters_clean.parquet was found.\n\n"
        "Check that:\n"
        "1. MySQL is running and MYSQL_PASSWORD in `.streamlit/secrets.toml` is correct\n"
        "2. You ran `python load_data.py`\n"
        "3. You ran the whole notebook `notebooks/analysis.ipynb` "
        "(its last section creates `encounters_clean`)\n\n"
        f"Error details: {err}"
    )
    st.stop()


def readmit_rate(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Visits and 30-day readmission rate (%) for each value of a column."""
    out = (df.groupby(column, observed=True)
             .agg(visits=("readmitted_30", "size"),
                  readmit_rate=("readmitted_30", "mean"))
             .reset_index())
    out["readmit_rate"] = (out["readmit_rate"] * 100).round(2)
    return out


def show(fig, height=380):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, width="stretch")


# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.header("Filters")
st.sidebar.caption("All charts and numbers update when you change these.")

ages = [a for a in AGE_ORDER if a in data["age_group"].unique()]
sel_age = st.sidebar.multiselect("Age group", ages, default=ages)

sel_gender = st.sidebar.multiselect("Gender", sorted(data["gender"].unique()),
                                    default=sorted(data["gender"].unique()))

admissions = sorted(data["admission_group"].unique())
sel_admission = st.sidebar.multiselect("Admission type", admissions, default=admissions)

discharges = sorted(data["discharge_group"].unique())
sel_discharge = st.sidebar.multiselect("Discharged to", discharges, default=discharges)

diagnoses = sorted(data["primary_diagnosis"].unique())
sel_diag = st.sidebar.multiselect("Primary diagnosis", diagnoses, default=diagnoses)

min_stay, max_stay = int(data["time_in_hospital"].min()), int(data["time_in_hospital"].max())
sel_stay = st.sidebar.slider("Days in hospital", min_stay, max_stay, (min_stay, max_stay))

sel_a1c = st.sidebar.radio("A1C test", ["All", "Tested", "Not tested"], horizontal=True)

df = data[
    data["age_group"].isin(sel_age)
    & data["gender"].isin(sel_gender)
    & data["admission_group"].isin(sel_admission)
    & data["discharge_group"].isin(sel_discharge)
    & data["primary_diagnosis"].isin(sel_diag)
    & data["time_in_hospital"].between(*sel_stay)
]
if sel_a1c != "All":
    df = df[df["a1c_tested"] == sel_a1c]

st.sidebar.divider()
st.sidebar.caption("Data: Diabetes 130-US hospitals, 1999–2008 (UCI / Kaggle). "
                   "Patients who died or went to hospice are excluded.")
st.sidebar.caption(f"Data loaded from: {data_source}")

# ------------------------------------------------------------------
# Header and key metrics
# ------------------------------------------------------------------
st.title("Diabetic patient readmission dashboard")
st.write("Which diabetic patients return to hospital within 30 days of discharge, "
         "based on about 99,000 visits to 130 US hospitals.")

if df.empty:
    st.warning("No visits match these filters. Widen the filters in the sidebar to see results.")
    st.stop()

overall_rate = data["readmitted_30"].mean() * 100
filtered_rate = df["readmitted_30"].mean() * 100

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Hospital visits", f"{len(df):,}")
m2.metric("Unique patients", f"{df['patient_nbr'].nunique():,}")
m3.metric("30-day readmission rate", f"{filtered_rate:.1f}%",
          delta=f"{filtered_rate - overall_rate:+.1f} pts vs all patients",
          delta_color="inverse")
m4.metric("Average stay", f"{df['time_in_hospital'].mean():.1f} days")
m5.metric("Average medications", f"{df['num_medications'].mean():.1f}")

if len(df) < 500:
    st.info(f"Only {len(df):,} visits match these filters, so rates may jump around.")

# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tab_overview, tab_history, tab_treatment, tab_findings, tab_predict, tab_data = st.tabs(
    ["Overview", "History and stay", "Treatment", "Key findings", "Risk predictor", "Data"])

# ---- Overview -----------------------------------------------------
with tab_overview:
    c1, c2 = st.columns([1, 1.4])

    with c1:
        status = df["readmit_status"].value_counts().reset_index()
        status.columns = ["status", "visits"]
        fig = px.pie(status, names="status", values="visits", hole=0.45,
                     color="status", color_discrete_map=OUTCOME_COLORS,
                     title="Outcome of each visit")
        show(fig)

    with c2:
        age = readmit_rate(df, "age_group")
        age["age_group"] = pd.Categorical(age["age_group"], AGE_ORDER, ordered=True)
        age = age.sort_values("age_group")
        fig = px.bar(age, x="age_group", y="readmit_rate", hover_data=["visits"],
                     color_discrete_sequence=[BLUE],
                     title="30-day readmission rate by age group",
                     labels={"age_group": "Age group", "readmit_rate": "Readmission rate (%)"})
        fig.add_hline(y=overall_rate, line_dash="dash", line_color=RED,
                      annotation_text=f"All patients {overall_rate:.1f}%")
        show(fig)

    diag = readmit_rate(df[df["primary_diagnosis"] != "Missing"], "primary_diagnosis")
    diag = diag.sort_values("readmit_rate")
    fig = px.bar(diag, x="readmit_rate", y="primary_diagnosis", orientation="h",
                 hover_data=["visits"], text="readmit_rate", color_discrete_sequence=[BLUE],
                 title="30-day readmission rate by primary diagnosis",
                 labels={"readmit_rate": "Readmission rate (%)", "primary_diagnosis": ""})
    fig.update_traces(texttemplate="%{text:.1f}%")
    show(fig, 400)

# ---- History and stay ---------------------------------------------
with tab_history:
    c1, c2 = st.columns(2)

    with c1:
        hist = df.assign(prior=df["number_inpatient"].clip(upper=5).astype(str).replace({"5": "5+"}))
        inp = readmit_rate(hist, "prior")
        fig = px.bar(inp, x="prior", y="readmit_rate", hover_data=["visits"],
                     text="readmit_rate", color_discrete_sequence=[RED],
                     title="Readmission rate by inpatient stays in the previous year",
                     labels={"prior": "Inpatient stays in previous year",
                             "readmit_rate": "Readmission rate (%)"})
        fig.update_traces(texttemplate="%{text:.1f}%")
        show(fig)

    with c2:
        stay = readmit_rate(df, "time_in_hospital")
        fig = px.line(stay, x="time_in_hospital", y="readmit_rate", markers=True,
                      hover_data=["visits"], color_discrete_sequence=[RED],
                      title="Readmission rate by length of stay",
                      labels={"time_in_hospital": "Days in hospital",
                              "readmit_rate": "Readmission rate (%)"})
        show(fig)

    disc = readmit_rate(df, "discharge_group").sort_values("readmit_rate")
    fig = px.bar(disc, x="readmit_rate", y="discharge_group", orientation="h",
                 hover_data=["visits"], text="readmit_rate",
                 color="readmit_rate", color_continuous_scale="Reds",
                 title="Readmission rate by discharge destination",
                 labels={"readmit_rate": "Readmission rate (%)", "discharge_group": ""})
    fig.update_traces(texttemplate="%{text:.1f}%")
    fig.update_coloraxes(showscale=False)
    show(fig)

    fig = px.histogram(df, x="time_in_hospital", color="readmit_status", barmode="group",
                       color_discrete_map=OUTCOME_COLORS,
                       title="How long patients stayed, by outcome",
                       labels={"time_in_hospital": "Days in hospital", "readmit_status": "Outcome"})
    show(fig)

# ---- Treatment ----------------------------------------------------
with tab_treatment:
    c1, c2 = st.columns(2)

    with c1:
        ins = readmit_rate(df, "insulin")
        ins["insulin"] = pd.Categorical(ins["insulin"], ["No", "Steady", "Up", "Down"], ordered=True)
        ins = ins.sort_values("insulin")
        fig = px.bar(ins, x="insulin", y="readmit_rate", hover_data=["visits"],
                     text="readmit_rate", color_discrete_sequence=[BLUE],
                     title="Readmission rate by insulin status",
                     labels={"insulin": "Insulin during the visit",
                             "readmit_rate": "Readmission rate (%)"})
        fig.update_traces(texttemplate="%{text:.1f}%")
        show(fig)

    with c2:
        a1c = readmit_rate(df, "a1c_result")
        a1c["a1c_result"] = pd.Categorical(a1c["a1c_result"],
                                           ["Not tested", "Norm", ">7", ">8"], ordered=True)
        a1c = a1c.sort_values("a1c_result")
        fig = px.bar(a1c, x="a1c_result", y="readmit_rate", hover_data=["visits"],
                     text="readmit_rate", color_discrete_sequence=[GREY],
                     title="Readmission rate by A1C test result",
                     labels={"a1c_result": "A1C result", "readmit_rate": "Readmission rate (%)"})
        fig.update_traces(texttemplate="%{text:.1f}%")
        show(fig)

    meds = readmit_rate(df, "num_medications")
    meds = meds[meds["visits"] >= 30]
    fig = px.scatter(meds, x="num_medications", y="readmit_rate", size="visits",
                     color_discrete_sequence=[BLUE],
                     title="Readmission rate vs number of medications (bubble size = visits)",
                     labels={"num_medications": "Number of medications",
                             "readmit_rate": "Readmission rate (%)"})
    show(fig)

    sample = df.sample(min(len(df), 10_000), random_state=42)
    fig = px.box(sample, x="readmit_status", y="num_medications", color="readmit_status",
                 color_discrete_map=OUTCOME_COLORS,
                 category_orders={"readmit_status": ["Not readmitted", "After 30 days",
                                                     "Within 30 days"]},
                 title="Number of medications by outcome",
                 labels={"readmit_status": "", "num_medications": "Number of medications"})
    fig.update_layout(showlegend=False)
    show(fig)

# ---- Key findings -------------------------------------------------
with tab_findings:
    st.subheader("What the analysis found")
    st.markdown("""
These findings come from the full dataset (all filters cleared).

1. **About 1 in 9 visits (11.4%) ends in a readmission within 30 days.**
2. **Past hospital stays are the strongest warning sign.** The rate rises from 8.6% for
   patients with no inpatient stays in the previous year to 37.1% for those with 5 or more.
3. **Discharge destination matters.** Patients sent to a care or rehab facility (16.5%)
   or another hospital (16.0%) return far more often than those sent home (9.3%).
4. **Longer stays carry more risk.** The rate climbs from 8.4% for a 1-day stay to
   about 14–15% for 8–10 days.
5. **Insulin dose changes signal risk.** Increased (13.3%) or decreased (14.2%) insulin
   compares with 10.2% for patients not on insulin.
6. **The A1C test is rarely done.** It was skipped in 83% of visits, and tested
   patients were readmitted less often (9.8–10.2% vs 11.7%).
7. **Patients admitted for diabetes itself** have the highest diagnosis-group rate (13.1%).
8. **Gender makes almost no difference** (11.5% women vs 11.3% men).
""")
    st.subheader("Recommendations")
    st.markdown("""
- Give every patient with 2 or more inpatient stays in the past year a follow-up call
  or clinic visit within a week of discharge.
- Send clear discharge notes and medication plans when patients move to rehab or
  nursing facilities.
- Make the A1C test a standard part of every diabetic admission.
- Give extra education and an early check-up to patients whose insulin dose changed.
""")
    st.caption("These are associations in historical data (1999–2008), not proof of cause. "
               "This dashboard is a learning project, not medical advice.")

# ---- Risk predictor -----------------------------------------------
with tab_predict:
    st.subheader("Predict a patient's 30-day readmission risk")
    model = load_model(data)

    if model is None:
        st.info("The prediction model could not be prepared.")
    else:
        st.write("Enter the patient's details and click **Predict risk**. "
                 "The model is XGBoost, the best of the 11 models compared in "
                 "model_comparison.ipynb.")

        def options(col):
            return sorted(data[col].dropna().unique())

        with st.form("predict_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**Patient**")
                age_group = st.selectbox("Age group", ages, index=ages.index("70-80"))
                gender = st.selectbox("Gender", options("gender"))
                primary_diagnosis = st.selectbox("Primary diagnosis", options("primary_diagnosis"))
            with c2:
                st.markdown("**Previous year**")
                number_inpatient = st.number_input("Inpatient stays", 0, 25, 0)
                number_emergency = st.number_input("Emergency visits", 0, 80, 0)
                number_outpatient = st.number_input("Outpatient visits", 0, 45, 0)
            with c3:
                st.markdown("**This hospital stay**")
                time_in_hospital = st.slider("Days in hospital", 1, 14, 4)
                num_medications = st.slider("Number of medications", 1, 81, 15)
                number_diagnoses = st.slider("Number of diagnoses", 1, 16, 8)

            c4, c5, c6 = st.columns(3)
            with c4:
                admission_group = st.selectbox("Admission type", options("admission_group"))
                discharge_group = st.selectbox("Discharged to", options("discharge_group"),
                                               index=options("discharge_group").index("Home"))
            with c5:
                insulin = st.selectbox("Insulin", ["No", "Steady", "Up", "Down"])
                a1c_result = st.selectbox("A1C result", ["Not tested", "Norm", ">7", ">8"])
            with c6:
                diabetes_med = st.selectbox("On diabetes medication?", ["Yes", "No"])
                med_change = st.selectbox("Medication changed?", ["No", "Ch"],
                                          format_func=lambda v: "Yes" if v == "Ch" else "No")

            submitted = st.form_submit_button("Predict risk")

        if submitted:
            # Start from a "typical" patient: most common value for text columns,
            # median for number columns. Then overwrite with what the user entered.
            feature_cols = model.feature_names_in_
            patient = {}
            for col in feature_cols:
                if pd.api.types.is_numeric_dtype(data[col]):
                    patient[col] = data[col].median()
                else:
                    patient[col] = data[col].mode()[0]

            entered = {
                "age_group": age_group, "gender": gender,
                "primary_diagnosis": primary_diagnosis,
                "number_inpatient": number_inpatient,
                "number_emergency": number_emergency,
                "number_outpatient": number_outpatient,
                "total_prior_visits": number_inpatient + number_emergency + number_outpatient,
                "time_in_hospital": time_in_hospital,
                "num_medications": num_medications,
                "number_diagnoses": number_diagnoses,
                "admission_group": admission_group, "discharge_group": discharge_group,
                "insulin": insulin, "a1c_result": a1c_result,
                "diabetes_med": diabetes_med, "med_change": med_change,
            }
            patient.update(entered)
            patient_df = pd.DataFrame([patient])[feature_cols]
            risk = model.predict_proba(patient_df)[0, 1] * 100
            level = "High" if risk >= 15 else "Medium" if risk >= 8 else "Low"

            # Streamlit reruns the script on every click, so we keep the result in
            # session_state. Otherwise it would disappear when the AI button is clicked.
            st.session_state["prediction"] = {"risk": risk, "level": level, "patient": entered}
            st.session_state.pop("ai_summary", None)

        if "prediction" in st.session_state:
            pred = st.session_state["prediction"]
            risk, level = pred["risk"], pred["level"]
            show_msg = {"High": st.error, "Medium": st.warning, "Low": st.success}[level]

            r1, r2 = st.columns(2)
            r1.metric("Predicted 30-day readmission risk", f"{risk:.1f}%",
                      delta=f"{risk - overall_rate:+.1f} pts vs average patient",
                      delta_color="inverse")
            r2.metric("Risk level", level)
            show_msg(f"**{level} risk.** The average patient's risk is {overall_rate:.1f}%.")

            st.caption("Risk levels: Low = under 8%, Medium = 8 to 15%, High = 15% or more. "
                       "When tested on patients the model had never seen, those rated High were "
                       "readmitted about 21% of the time, compared with about 6% for those "
                       "rated Low. This is a learning project, not medical advice.")

            # ---- Generative AI summary ------------------------------------
            st.divider()
            st.subheader("AI summary")
            factors = ai_helper.risk_factors(pred["patient"])
            with st.expander("Warning signs found for this patient", expanded=False):
                if factors:
                    st.markdown("\n".join(f"- {f}" for f in factors))
                else:
                    st.write("None of the main warning signs from our analysis.")

            if ai_helper.get_api_key() is None:
                st.info("To turn on the AI summary, create a free Gemini API key at "
                        "aistudio.google.com, then put it in `.streamlit/secrets.toml` as  \n"
                        '`GEMINI_API_KEY = "your-key"`  \nand restart the app.')
            elif st.button("Write AI summary"):
                prompt = ai_helper.build_prompt(pred["patient"], risk, level,
                                                overall_rate, factors)
                with st.spinner("Asking Gemini..."):
                    try:
                        st.session_state["ai_summary"] = ai_helper.generate_summary(prompt)
                    except Exception as err:
                        st.error(f"The AI request failed: {err}")

            if "ai_summary" in st.session_state:
                st.markdown(st.session_state["ai_summary"])

# ---- Data ---------------------------------------------------------
with tab_data:
    st.subheader("Filtered data")
    st.write(f"Showing the first 500 of {len(df):,} visits that match your filters.")
    st.dataframe(df.head(500), width="stretch", hide_index=True)
    st.download_button("Download filtered data (CSV)",
                       df.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_readmissions.csv", mime="text/csv")
