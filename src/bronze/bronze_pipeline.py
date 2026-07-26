from src.bronze.duckdb_utils import get_connection
from src.bronze.bronze_transform import (
    export_parquet,
    get_row_count,
    get_schema,
    load_csv,
    validate_duplicate_track_ids,
    validate_nulls,
    validate_required_columns,
    validate_row_count,
)
from src.ingestion.minio_client import MinIOClient

from datetime import datetime

RAW_OBJECT = (
    f"raw/spotify/"
    f"ingestion_date={datetime.now().date()}/"
    f"dataset.csv"
)
BRONZE_OBJECT = (
    f"bronze/spotify/"
    f"ingestion_date={datetime.now().date()}/"
    f"dataset.parquet"
)

LOCAL_CSV = "/tmp/dataset.csv"
LOCAL_PARQUET = "/tmp/dataset.parquet"


def run_bronze_pipeline():
    print("=" * 50)
    print("Starting Bronze Pipeline")
    print("=" * 50)

    client = MinIOClient()

    if not client.object_exists(RAW_OBJECT):
        raise FileNotFoundError(
            f"Raw object '{RAW_OBJECT}' not found in MinIO."
        )

    client.download_file(
        RAW_OBJECT,
        LOCAL_CSV,
    )

    conn = get_connection()

    load_csv(conn, LOCAL_CSV)
    validate_row_count(conn)
    validate_required_columns(conn)
    validate_duplicate_track_ids(conn)
    validate_nulls(conn)

    print(f"Rows: {get_row_count(conn)}")

    print("\nSchema:")

    for column in get_schema(conn):
        print(column)

    export_parquet(
        conn,
        LOCAL_PARQUET,
    )

    client.upload_file(
        LOCAL_PARQUET,
        BRONZE_OBJECT,
    )

    print("\nBronze pipeline completed successfully.")