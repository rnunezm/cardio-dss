from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LogisticRegression
import os

# -------------------
# CONFIGURATION
# -------------------

CSV_FILE = '/Users/rubennunez/Documents/Msc_Data_Sciences/DSS/Project/cardio-dss/data/raw/cardio_train.csv'  # <- Change to your CSV path
DB_URI = 'postgresql+psycopg2://rubennunez:VeraRomina201@localhost:5432/cardio'
TABLE_NAME = "patients"
DECISION_TABLE = "risk_results"

# -------------------
# DAG FUNCTIONS
# -------------------

def extract(**kwargs):
    df = pd.read_csv(CSV_FILE, sep=';')

    #  THIS FORMAT IS THE CORRECT ONE
    kwargs['ti'].xcom_push(
        key='raw_data',
        value=df.to_dict(orient='records')
    )

    print(f"Extract completed: {len(df)} rows")
    return len(df)


def transform(**kwargs):
    """Transform data and convert age from days to years"""

    records = kwargs['ti'].xcom_pull(key='raw_data')

    if not records:
        raise ValueError("raw_data is empty")

    # raw_data IS ALREADY a list of dicts
    df = pd.DataFrame(records)

    # Convert to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # Remove null values
    df = df.dropna()

    # Age: days → years
    df['age'] = (df['age'] / 365.25).round(0).astype(int)

    kwargs['ti'].xcom_push(
        key='transformed_data',
        value=df.to_dict(orient='records')
    )

    print(f"Transform completed: {len(df)} rows")
    return len(df)


def load(**kwargs):
    df = pd.DataFrame(kwargs['ti'].xcom_pull(key='transformed_data'))
    engine = create_engine(DB_URI)
    df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
    print(f"Load completed: {len(df)} rows loaded")


def decision_engine(**kwargs):
    """Simple decision engine: predictive model"""
    df = pd.DataFrame(kwargs['ti'].xcom_pull(key='transformed_data'))
    
    # Example: predict cardiovascular risk
    X = df[['age', 'height', 'weight']]  # Adjust according to your columns
    y = df['cardio']  # target column

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    df['risk_pred'] = model.predict(X)

    # Save results to DB
    engine = create_engine(DB_URI)
    df.to_sql(DECISION_TABLE, engine, if_exists='replace', index=False, method='multi')
    
    kwargs['ti'].xcom_push(key='decision_results', value=df.to_dict())
    print("Decision Engine completed")
    return df.shape[0]

# -------------------
# DAG
# -------------------

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1
}

with DAG(
    dag_id='full_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    t1_extract = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    t2_transform = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    t3_load = PythonOperator(
        task_id='load',
        python_callable=load
    )

    t4_decision = PythonOperator(
        task_id='decision_engine',
        python_callable=decision_engine
    )

    # Execution order
    t1_extract >> t2_transform >> t3_load >> t4_decision
