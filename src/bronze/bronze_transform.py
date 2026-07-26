import duckdb


def load_csv(connection, csv_path):
    """
    Load a CSV file into DuckDB as a table and perform
    basic Bronze-layer transformations.
    """
    connection.execute("""
        CREATE OR REPLACE TABLE spotify_raw AS
        SELECT *
        FROM read_csv_auto(?, HEADER=TRUE);
    """, [csv_path])

    # Remove the unwanted index column if present
    columns = [
        row[0]
        for row in connection.execute(
            "DESCRIBE spotify_raw"
        ).fetchall()
    ]

    if "column00" in columns:
        connection.execute("""
            ALTER TABLE spotify_raw
            DROP COLUMN column00;
        """)


def get_row_count(connection):
    """
    Return the number of rows.
    """
    return connection.execute(
        "SELECT COUNT(*) FROM spotify_raw"
    ).fetchone()[0]


def get_schema(connection):
    """
    Return the inferred schema.
    """
    return connection.execute(
        "DESCRIBE spotify_raw"
    ).fetchall()


def export_parquet(connection, output_path):
    """
    Export the table as a Parquet file.
    """
    connection.execute("""
        COPY spotify_raw
        TO ?
        (FORMAT PARQUET);
    """, [output_path])

def validate_row_count(connection):
    """
    Ensure the dataset is not empty.
    """
    count = get_row_count(connection)

    if count == 0:
        raise ValueError("Dataset is empty.")

    print(f"✓ Row count check passed ({count} rows)")

def validate_required_columns(connection):
    """
    Ensure all required columns exist.
    """
    required_columns = {
        "track_id",
        "artists",
        "album_name",
        "track_name",
        "popularity",
        "duration_ms",
        "track_genre",
    }

    existing_columns = {
        row[0]
        for row in get_schema(connection)
    }

    missing = required_columns - existing_columns

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    print("✓ Required columns check passed")

def validate_duplicate_track_ids(connection):
    """
    Report duplicate track IDs.
    """
    duplicates = connection.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT track_id
            FROM spotify_raw
            GROUP BY track_id
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]

    print(f"Duplicate track_ids: {duplicates}")

def validate_nulls(connection):
    """
    Report NULL values in important columns.
    """
    important_columns = [
        "track_id",
        "track_name",
        "artists",
        "track_genre",
    ]

    print("\nNULL Summary")

    for column in important_columns:
        nulls = connection.execute(f"""
            SELECT COUNT(*)
            FROM spotify_raw
            WHERE {column} IS NULL
        """).fetchone()[0]

        print(f"{column}: {nulls}")