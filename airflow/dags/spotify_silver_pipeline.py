from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.silver.silver_pipeline import run


default_args = {
    "owner": "airflow",
}


with DAG(
    dag_id="spotify_silver_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["spotify", "silver"],
) as dag:

    silver_task = PythonOperator(
        task_id="silver_pipeline",
        python_callable=run,
    )