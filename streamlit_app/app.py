import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(page_title="Cardiovascular Risk DSS", layout="wide")

DB_URI = 'postgresql+psycopg2://rubennunez:VeraRomina201@localhost:5432/cardio'
TABLE_NAME = "risk_results"

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    engine = create_engine(DB_URI)
    return pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)

df = load_data()

# -----------------------------
# Sidebar – patient selection
# -----------------------------
st.sidebar.title("🧑‍⚕️ Patient Selection")

patient_id = st.sidebar.selectbox(
    "Select Patient ID",
    df["id"].sort_values().unique()
)

patient = df[df["id"] == patient_id].iloc[0]

# -----------------------------
# DSS functions
# -----------------------------
def calculate_risk(p):
    score = 0

    if p.age >= 55:
        score += 1
    if p.ap_hi >= 140 or p.ap_lo >= 90:
        score += 2
    if p.cholesterol >= 2:
        score += 1
    if p.gluc >= 2:
        score += 1
    if p.smoke == 1:
        score += 1
    if p.alco == 1:
        score += 1
    if p.active == 0:
        score += 1

    if score <= 2:
        return "🟢 Low", score
    elif score <= 5:
        return "🟠 Moderate", score
    else:
        return "🔴 High", score


def recommendations(p, risk_level):
    recs = []

    if risk_level == "🔴 High":
        recs.append("Urgent medical consultation and cardiovascular follow-up.")
    if p.ap_hi >= 140 or p.ap_lo >= 90:
        recs.append("Strict blood pressure control.")
    if p.cholesterol >= 2:
        recs.append("Low saturated fat diet and cholesterol management.")
    if p.gluc >= 2:
        recs.append("Glycemic control and diabetes assessment.")
    if p.smoke == 1:
        recs.append("Smoking cessation is strongly recommended.")
    if p.alco == 1:
        recs.append("Reduce or eliminate alcohol consumption.")
    if p.active == 0:
        recs.append("Increase regular physical activity.")

    if not recs:
        recs.append("Maintain current healthy lifestyle habits.")

    return recs

# -----------------------------
# DSS evaluation
# -----------------------------
risk_level, score = calculate_risk(patient)
recs = recommendations(patient, risk_level)

# -----------------------------
# Main UI
# -----------------------------
st.title("🫀 Decision Support System – Cardiovascular Risk")

col1, col2, col3 = st.columns(3)

col1.metric("Age (years)", patient.age)
col2.metric("Systolic Blood Pressure", f"{patient.ap_hi} mmHg")
col3.metric("Diastolic Blood Pressure", f"{patient.ap_lo} mmHg")

col1.metric("Cholesterol", "Normal" if patient.cholesterol == 1 else "High")
col2.metric("Glucose", "Normal" if patient.gluc == 1 else "High")
col3.metric("Physical Activity", "Active" if patient.active == 1 else "Sedentary")

st.divider()

# -----------------------------
# Risk assessment
# -----------------------------
st.subheader("📊 Risk Assessment")

st.markdown(f"""
### Risk Level: **{risk_level}**
DSS Score: **{score}**
""")

# -----------------------------
# Recommendations
# -----------------------------
st.subheader("💡 Personalized Recommendations")

for r in recs:
    st.write("•", r)

# -----------------------------
# Clinical status
# -----------------------------
st.divider()
st.subheader("📌 Recorded Clinical Status")

if patient.cardio == 1:
    st.error("Patient diagnosed with cardiovascular disease")
else:
    st.success("No recorded cardiovascular diagnosis")
