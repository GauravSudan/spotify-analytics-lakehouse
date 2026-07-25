from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def hello_spotify():
    """Simple verification task."""
    print("=" * 60)
    print("🎵 Spotify Analytics Lakehouse")
    print("✅ Airflow DAG is running successfully!")
    print("🚀 Ready to build the ingestion pipeline.")
    print("=" * 60)


with DAG(
    dag_id="hello_spotify",
    description="Verify that the Airflow environment is working correctly.",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["setup", "phase1"],
) as dag:

    hello_task = PythonOperator(
        task_id="hello_spotify",
        python_callable=hello_spotify,
    )