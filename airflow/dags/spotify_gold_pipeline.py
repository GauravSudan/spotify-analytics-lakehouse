"""
Airflow DAG for the Spotify Gold Pipeline.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.gold.gold_pipeline import run


default_args = {
    "owner": "airflow",
}


with DAG(
    dag_id="spotify_gold_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 7, 26),
    schedule="@daily",
    catchup=False,
    tags=["spotify", "gold"],
) as dag:

    gold_pipeline = PythonOperator(
        task_id="run_gold_pipeline",
        python_callable=run,
    )

    gold_pipeline