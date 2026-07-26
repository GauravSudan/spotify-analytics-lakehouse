from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.bronze.bronze_pipeline import run_bronze_pipeline

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="spotify_bronze_pipeline",
    default_args=default_args,
    description="Bronze layer transformation pipeline",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["spotify", "bronze"],
) as dag:

    bronze_task = PythonOperator(
        task_id="bronze_transformation",
        python_callable=run_bronze_pipeline,
    )