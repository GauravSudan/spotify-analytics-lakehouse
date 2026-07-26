from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion.ingest_dataset import run_ingestion


default_args = {
    "owner": "gaurav",
}


with DAG(
    dag_id="spotify_dataset_ingestion",
    default_args=default_args,
    start_date=datetime(2026, 7, 26),
    schedule="@daily",
    catchup=False,
    tags=["spotify", "minio", "ingestion"],
) as dag:

    ingest_dataset = PythonOperator(
        task_id="ingest_dataset",
        python_callable=run_ingestion,
    )