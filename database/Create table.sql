CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY,
    age INTEGER,
    sex INTEGER,
    cholesterol INTEGER,
    blood_pressure INTEGER,
    smoker INTEGER,
    diabetes INTEGER,
    bmi FLOAT,
    target INTEGER
);

CREATE TABLE risk_results (
    patient_id INTEGER,
    risk_score FLOAT,
    risk_level TEXT
);
