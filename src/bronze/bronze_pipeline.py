from datetime import date

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

TODAY = date.today().isoformat()

BRONZE_OBJECT = (
    f"bronze/spotify/"
    f"ingestion_date={TODAY}/"
    f"dataset.parquet"
)

LOCAL_CSV = "/tmp/dataset.csv"
LOCAL_PARQUET = "/tmp/dataset.parquet"


def run_bronze_pipeline():
    print("=" * 50)
    print("Starting Bronze Pipeline")
    print("=" * 50)

    client = MinIOClient()

    # Automatically find the latest Raw dataset
    raw_object = client.get_latest_object(
        prefix="raw/spotify",
        filename="dataset.csv",
    )

    client.download_file(
        raw_object,
        LOCAL_CSV,
    )

    conn = get_connection()

    try:
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

    finally:
        conn.close()


if __name__ == "__main__":
    run_bronze_pipeline()