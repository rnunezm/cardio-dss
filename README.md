# Cardiovascular Decision Support System (Cardio-DSS)

## 1. Project Overview

This project implements an end-to-end Decision Support System (DSS) for cardiovascular risk assessment, developed as part of a Master’s Degree in Data Science.

The system integrates data ingestion, transformation, storage, predictive modeling, and decision support visualization using modern data engineering and data science tools.

The goal is to assist healthcare decision-making by identifying patients at risk of cardiovascular disease and providing personalized recommendations based on clinical data.

---

## 2. System Architecture

CSV (Local File)  
↓  
Apache Airflow (ETL + Decision Engine)  
↓  
PostgreSQL Database
↓  
Streamlit Dashboard (DSS Interface)

---

## 3. Technologies Used

| Layer              | Tool           |
| ------------------ | -------------- |
| Orchestration      | Apache Airflow |
| Data Processing    | Pandas         |
| Database           | PostgreSQL     |
| ORM / DB Access    | SQLAlchemy     |
| Machine Learning   | Scikit-learn   |
| Visualization / UI | Streamlit      |
| Language           | Python 3.9     |

---

## 4. Project Structure

cardio-dss/
│  
├── Airflow/  
│ └── dags/  
│ └── cardio_etl_dag.py/  
├── Streamlit_app/  
│ └── app.py/
├── data/
│ └── raw/
│ └── cardio_train.csv
│
├── requirements.txt
│  
├── README.md

---

## 5. Data Pipeline (Airflow DAG)

The Airflow DAG executes the following stages:

### 5.1 Extract

- Reads cardiovascular data from a local CSV file
- Stores records using Airflow XCom

### 5.2 Transform

- Converts data to numeric format
- Removes missing values
- Converts age from days to years
- Cleans and standardizes features

### 5.3 Load

- Stores processed patient data in PostgreSQL

### 5.4 Decision Engine

- Trains a Logistic Regression model
- Predicts cardiovascular risk
- Saves predictions into a dedicated decision table

---

## 6. Decision Support System (Streamlit)

The Streamlit application provides:

- Patient selection by ID
- Clinical indicators overview
- DSS-based risk scoring
- Personalized health recommendations
- Clinical history visualization
- Explainable decision logic

---

## 7. Installation and Setup

### 7.1 Create virtual environment

python3.9 -m venv venv
source venv/bin/activate

### 7.2 Install dependencies

pip install -r requirements.txt

### 7.3 PostgreSQL Setup

CREATE DATABASE cardio;

---

## 8. Running the Project

### 8.1 Start Airflow

export AIRFLOW_HOME=$(pwd)/Airflow
airflow db init
airflow webserver
airflow scheduler

### Access Airflow UI

http://localhost:8080

### Trigger the DAG

full_pipeline

### 8.2 Run Streamlit Application

streamlit run app.py

### Access dashboard

http://localhost:8501

---

## 9. Machine Learning Model

Algorithm: Logistic Regression
Target variable: cardio
Features:
Age
Height
Weight
Purpose: Cardiovascular risk prediction for decision support

---

## 10. Disclaimer

This system is for academic and educational purposes only.
It does not replace medical diagnosis or professional healthcare advice.

---

## 11. Academic Context

Program: Master in Data Science
Course: Decision Support Systems
Focus:
ETL pipelines
Predictive analytics
Explainable decision-making
End-to-end DSS development

---

## 12. Future Improvements

Feature engineering (BMI, risk indices)
Advanced machine learning models
Real-time data ingestion
Role-based access control
