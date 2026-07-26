from pathlib import Path
from datetime import datetime

from src.ingestion.dataset_loader import load_dataset
from src.ingestion.minio_client import MinIOClient


#DATASET_PATH = Path("datasets/dataset.csv")
BASE_DIR = Path("/opt/airflow/project")
DATASET_PATH = BASE_DIR / "datasets" / "dataset.csv"


def run_ingestion():
    print("Starting Spotify dataset ingestion...")

    # Validate dataset
    df = load_dataset(DATASET_PATH)

    print(f"Dataset loaded successfully.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    # Upload to MinIO
    client = MinIOClient()

    client.create_bucket_if_not_exists()

    object_name = (
        f"raw/spotify/"
        f"ingestion_date={datetime.now().date()}/"
        f"dataset.csv"
    )

    client.upload_file(
        str(DATASET_PATH),
        object_name,
    )

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    run_ingestion()