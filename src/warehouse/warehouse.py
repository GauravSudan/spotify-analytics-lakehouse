from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[2]

WAREHOUSE_DB = PROJECT_ROOT / "warehouse" / "spotify.duckdb"


def get_connection():
    """Return a connection to the persistent warehouse."""
    return duckdb.connect(str(WAREHOUSE_DB))


def refresh_gold_tables(source_con):
    """
    Copy all Gold tables from the processing database
    into the persistent warehouse.
    """
    warehouse_con = get_connection()

    try:
        tables = [
            "artist_summary",
            "genre_summary",
            "explicit_summary",
            "popularity_distribution",
            "audio_feature_summary",
        ]

        for table in tables:
            df = source_con.execute(
                f"SELECT * FROM {table}"
            ).fetchdf()

            warehouse_con.register("temp_df", df)

            warehouse_con.execute(f"""
                CREATE OR REPLACE TABLE {table} AS
                SELECT *
                FROM temp_df
            """)

            warehouse_con.unregister("temp_df")

            print(f"Warehouse refreshed: {table}")

    finally:
        warehouse_con.close()