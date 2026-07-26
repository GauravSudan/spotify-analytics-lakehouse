"""
Gold Pipeline

Workflow:
1. Download Silver Parquet from MinIO
2. Load into DuckDB
3. Apply Gold transformations
4. Export Gold Parquet files
5. Upload Gold Parquet files to MinIO
"""

from datetime import date
from pathlib import Path

from src.ingestion.minio_client import MinIOClient
from src.gold.duckdb_utils import get_connection
from src.gold.gold_transform import transform


TODAY = date.today().isoformat()

SILVER_OBJECT = (
    f"silver/spotify/ingestion_date={TODAY}/dataset.parquet"
)

LOCAL_SILVER_FILE = Path("/tmp/silver_dataset.parquet")

GOLD_TABLES = {
    "artist_summary": Path("/tmp/artist_summary.parquet"),
    "genre_summary": Path("/tmp/genre_summary.parquet"),
    "explicit_summary": Path("/tmp/explicit_summary.parquet"),
    "popularity_distribution": Path("/tmp/popularity_distribution.parquet"),
    "audio_feature_summary": Path("/tmp/audio_feature_summary.parquet"),
}


def download_silver_data(minio):
    """
    Download Silver Parquet from MinIO.
    """
    minio.download_file(
        object_name=SILVER_OBJECT,
        local_path=str(LOCAL_SILVER_FILE),
    )


def load_silver_table(con):
    """
    Load Silver Parquet into DuckDB.
    """
    con.execute(f"""
        CREATE OR REPLACE TABLE silver AS
        SELECT *
        FROM read_parquet('{LOCAL_SILVER_FILE}');
    """)

    rows = con.execute("""
        SELECT COUNT(*)
        FROM silver
    """).fetchone()[0]

    print(f"Loaded {rows} rows into DuckDB")


def export_gold_tables(con):
    """
    Export all Gold tables to Parquet.
    """
    for table_name, local_path in GOLD_TABLES.items():
        con.execute(f"""
            COPY {table_name}
            TO '{local_path}'
            (FORMAT PARQUET);
        """)

        print(f"Exported '{local_path}'")


def upload_gold_data(minio):
    """
    Upload all Gold Parquet files to MinIO.
    """
    for table_name, local_path in GOLD_TABLES.items():

        object_name = (
            f"gold/spotify/ingestion_date={TODAY}/{table_name}.parquet"
        )

        minio.upload_file(
            local_path=str(local_path),
            object_name=object_name,
        )


def run():
    print("=" * 50)
    print("Starting Gold Pipeline")
    print("=" * 50)

    minio = MinIOClient()
    con = get_connection()

    try:
        download_silver_data(minio)
        load_silver_table(con)

        transform(con)

        export_gold_tables(con)
        upload_gold_data(minio)

        print("=" * 50)
        print("Gold Pipeline completed successfully.")
        print("=" * 50)

    finally:
        con.close()


if __name__ == "__main__":
    run()