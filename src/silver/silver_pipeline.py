"""
Silver Pipeline

Workflow:
1. Download Bronze Parquet from MinIO
2. Load into DuckDB
3. Apply Silver transformations
4. Export Silver Parquet
5. Upload Silver Parquet to MinIO
"""

from datetime import date
from pathlib import Path

from src.ingestion.minio_client import MinIOClient
from src.silver.duckdb_utils import get_connection
from src.silver.silver_transform import transform


TODAY = date.today().isoformat()

BRONZE_OBJECT = (
    f"bronze/spotify/ingestion_date={TODAY}/dataset.parquet"
)

SILVER_OBJECT = (
    f"silver/spotify/ingestion_date={TODAY}/dataset.parquet"
)

LOCAL_BRONZE_FILE = Path("/tmp/bronze_dataset.parquet")
LOCAL_SILVER_FILE = Path("/tmp/silver_dataset.parquet")


def download_bronze_data(minio):
    """
    Download Bronze Parquet from MinIO.
    """
    minio.download_file(
        object_name=BRONZE_OBJECT,
        local_path=str(LOCAL_BRONZE_FILE),
    )


def load_bronze_table(con):
    """
    Load Bronze Parquet into DuckDB.
    """
    con.execute(f"""
        CREATE OR REPLACE TABLE bronze AS
        SELECT *
        FROM read_parquet('{LOCAL_BRONZE_FILE}');
    """)

    rows = con.execute("""
        SELECT COUNT(*)
        FROM bronze
    """).fetchone()[0]

    print(f"Loaded {rows} rows into DuckDB")


def export_silver_table(con):
    """
    Export Silver table to Parquet.
    """
    con.execute(f"""
        COPY silver
        TO '{LOCAL_SILVER_FILE}'
        (FORMAT PARQUET);
    """)

    print(f"Exported '{LOCAL_SILVER_FILE}'")


def upload_silver_data(minio):
    """
    Upload Silver Parquet to MinIO.
    """
    minio.upload_file(
        local_path=str(LOCAL_SILVER_FILE),
        object_name=SILVER_OBJECT,
    )


def run():
    print("=" * 50)
    print("Starting Silver Pipeline")
    print("=" * 50)

    minio = MinIOClient()
    con = get_connection()

    download_bronze_data(minio)
    load_bronze_table(con)

    transform(con)

    export_silver_table(con)
    upload_silver_data(minio)

    con.close()

    print("=" * 50)
    print("Silver Pipeline completed successfully.")
    print("=" * 50)


if __name__ == "__main__":
    run()