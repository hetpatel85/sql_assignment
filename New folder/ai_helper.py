"""
ai_helper.py
------------
Generative AI part: turns a patient's predicted risk into plain-language text,
using Google's Gemini API (free plan, runs in Google's cloud, nothing to download).

The API key is read from .streamlit/secrets.toml:
    GEMINI_API_KEY = "paste-your-key-here"
"""

import os

import streamlit as st

DEFAULT_MODEL = "gemini-flash-latest"   # always points to Google's newest fast model


def _read_secret(name: str):
    """Read a setting from .streamlit/secrets.toml, or from an environment variable."""
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:                      # no secrets.toml file yet
        pass
    return os.environ.get(name)


def get_api_key():
    key = _read_secret("GEMINI_API_KEY")
    if not key or key == "paste-your-key-here":
        return None
    return key


def risk_factors(p: dict) -> list:
    """
    Warning signs found in our data analysis (analysis.ipynb), checked for this patient.
    Each line includes the readmission rate we measured for that group, so the AI
    only uses facts from our own data.
    """
    factors = []
    if p["number_inpatient"] >= 5:
        factors.append(f"{p['number_inpatient']} inpatient stays in the previous year "
                       "(patients with 5+ were readmitted 37% of the time)")
    elif p["number_inpatient"] >= 2:
        factors.append(f"{p['number_inpatient']} inpatient stays in the previous year "
                       "(18-24% readmission for 2-4 stays, vs 9% for none)")
    elif p["number_inpatient"] == 1:
        factors.append("1 inpatient stay in the previous year (13% readmission, vs 9% for none)")
    if p["number_emergency"] >= 1:
        factors.append(f"{p['number_emergency']} emergency visit(s) in the previous year")
    if p["discharge_group"] in ("Care / rehab facility", "Another hospital"):
        factors.append(f"discharged to {p['discharge_group'].lower()} "
                       "(about 16% readmission, vs 9% for home)")
    elif p["discharge_group"] == "Left against advice":
        factors.append("left against medical advice (14% readmission)")
    if p["time_in_hospital"] >= 8:
        factors.append(f"long stay of {p['time_in_hospital']} days "
                       "(14-15% readmission, vs 8% for 1 day)")
    if p["insulin"] in ("Up", "Down"):
        factors.append(f"insulin dose changed ({p['insulin'].lower()}) during the stay "
                       "(13-14% readmission, vs 10% for no insulin)")
    if p["a1c_result"] == "Not tested":
        factors.append("A1C blood sugar test not done "
                       "(12% readmission, vs about 10% for tested patients)")
    if p["num_medications"] >= 21:
        factors.append(f"{p['num_medications']} medications (about 13% readmission)")
    if p["primary_diagnosis"] == "Diabetes":
        factors.append("admitted mainly for diabetes (13% readmission, the highest diagnosis group)")
    return factors


def build_prompt(p: dict, risk: float, level: str, average: float, factors: list) -> str:
    factor_text = "\n".join(f"- {f}" for f in factors) or "- none of the main warning signs"
    return f"""You are helping a hospital team after a diabetic patient's discharge.
A machine learning model (XGBoost) trained on 99,340 past hospital visits predicted this patient's
risk of being readmitted within 30 days.

Patient: age group {p['age_group']}, {p['gender']}, main diagnosis group: {p['primary_diagnosis']}.
Predicted 30-day readmission risk: {risk:.1f}% ({level} risk). Average patient: {average:.1f}%.
Warning signs found in our data for this patient:
{factor_text}

Write two short sections in plain English:

**For the care team** (3-4 sentences): explain the risk level and the main reasons, using only
the facts above, and suggest practical follow-up steps such as a follow-up call or clinic visit,
medication review or diabetes education.

**For the patient** (3-4 short bullet points, simple words, friendly tone): what to watch for at
home and when to contact their doctor.

Rules: use only the information above, do not invent test results or diagnoses, do not prescribe
medicines or doses, and end with one line saying this is an AI-generated summary, not medical advice."""


def generate_summary(prompt: str) -> str:
    """Send the prompt to Gemini and return its answer as text."""
    from google import genai               # imported here so the app still runs without it

    client = genai.Client(api_key=get_api_key())
    model = _read_secret("GEMINI_MODEL") or DEFAULT_MODEL
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text
