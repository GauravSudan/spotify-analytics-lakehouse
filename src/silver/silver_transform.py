"""
Silver layer transformations.

Responsibilities:
- Remove duplicate records
- Handle missing values
- Standardize text
- Perform data quality validation
"""


def remove_duplicates(con):
    """
    Remove duplicate track_ids.
    Keep the record with the highest popularity.
    """
    before_count = con.execute("""
        SELECT COUNT(*)
        FROM bronze
    """).fetchone()[0]

    print(f"Rows before cleaning: {before_count}")

    con.execute("""
        CREATE OR REPLACE TABLE silver AS

        SELECT *
        EXCLUDE (rn)

        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY track_id
                       ORDER BY popularity DESC
                   ) AS rn
            FROM bronze
        )

        WHERE rn = 1;
    """)

    after_count = con.execute("""
        SELECT COUNT(*)
        FROM silver
    """).fetchone()[0]

    removed = before_count - after_count

    print(f"Rows after deduplication : {after_count}")
    print(f"Duplicate rows removed   : {removed}")


def handle_missing_values(con):
    """
    Replace missing values with defaults.
    """
    con.execute("""
        UPDATE silver
        SET track_name = 'Unknown Track'
        WHERE track_name IS NULL;
    """)

    con.execute("""
        UPDATE silver
        SET artists = 'Unknown Artist'
        WHERE artists IS NULL;
    """)


def standardize_text(con):
    """
    Standardize text columns.
    """
    con.execute("""
        UPDATE silver
        SET
            track_name = TRIM(track_name),
            artists = TRIM(artists),
            album_name = TRIM(album_name),
            track_genre = LOWER(TRIM(track_genre));
    """)


def validate_ranges(con):
    """
    Validate important numeric columns.
    """

    popularity_invalid = con.execute("""
        SELECT COUNT(*)
        FROM silver
        WHERE popularity < 0
           OR popularity > 100;
    """).fetchone()[0]

    audio_columns = [
        "danceability",
        "energy",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
    ]

    print("\nRange Validation")
    print("----------------")

    print(f"popularity : {popularity_invalid}")

    for column in audio_columns:
        invalid = con.execute(f"""
            SELECT COUNT(*)
            FROM silver
            WHERE {column} < 0
               OR {column} > 1;
        """).fetchone()[0]

        print(f"{column:<17}: {invalid}")


def print_null_summary(con):
    """
    Print NULL summary for important columns.
    """

    track_name_nulls = con.execute("""
        SELECT COUNT(*)
        FROM silver
        WHERE track_name IS NULL;
    """).fetchone()[0]

    artists_nulls = con.execute("""
        SELECT COUNT(*)
        FROM silver
        WHERE artists IS NULL;
    """).fetchone()[0]

    print("\nNULL Summary")
    print("------------")
    print(f"track_name : {track_name_nulls}")
    print(f"artists    : {artists_nulls}")


def transform(con):
    """
    Execute all Silver transformations.
    """

    print("\nStarting Silver transformations...\n")

    remove_duplicates(con)
    handle_missing_values(con)
    standardize_text(con)
    validate_ranges(con)
    print_null_summary(con)

    print("\nSilver transformations completed.")