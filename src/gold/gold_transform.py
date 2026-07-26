"""
Gold transformations.

Creates business-ready analytical tables from the Silver dataset.
"""


def create_artist_summary(con):
    """
    Create artist-level summary.
    """
    con.execute("""
        CREATE OR REPLACE TABLE artist_summary AS
        SELECT
            artists,
            COUNT(*) AS total_tracks,
            ROUND(AVG(popularity), 2) AS avg_popularity,
            MAX(popularity) AS max_popularity,
            ROUND(AVG(danceability), 3) AS avg_danceability,
            ROUND(AVG(energy), 3) AS avg_energy,
            ROUND(AVG(valence), 3) AS avg_valence
        FROM silver
        GROUP BY artists
        ORDER BY avg_popularity DESC;
    """)

    rows = con.execute("""
        SELECT COUNT(*)
        FROM artist_summary
    """).fetchone()[0]

    print(f"Created artist_summary ({rows} rows)")


def create_genre_summary(con):
    """
    Create genre-level summary.
    """
    con.execute("""
        CREATE OR REPLACE TABLE genre_summary AS
        SELECT
            track_genre,
            COUNT(*) AS total_tracks,
            ROUND(AVG(popularity), 2) AS avg_popularity,
            ROUND(AVG(danceability), 3) AS avg_danceability,
            ROUND(AVG(energy), 3) AS avg_energy,
            ROUND(AVG(acousticness), 3) AS avg_acousticness
        FROM silver
        GROUP BY track_genre
        ORDER BY avg_popularity DESC;
    """)

    rows = con.execute("""
        SELECT COUNT(*)
        FROM genre_summary
    """).fetchone()[0]

    print(f"Created genre_summary ({rows} rows)")


def create_explicit_summary(con):
    """
    Create explicit vs non-explicit summary.
    """
    con.execute("""
        CREATE OR REPLACE TABLE explicit_summary AS
        SELECT
            explicit,
            COUNT(*) AS total_tracks,
            ROUND(AVG(popularity), 2) AS avg_popularity,
            ROUND(AVG(energy), 3) AS avg_energy,
            ROUND(AVG(valence), 3) AS avg_valence
        FROM silver
        GROUP BY explicit;
    """)

    rows = con.execute("""
        SELECT COUNT(*)
        FROM explicit_summary
    """).fetchone()[0]

    print(f"Created explicit_summary ({rows} rows)")


def create_popularity_distribution(con):
    """
    Create popularity distribution table.
    """
    con.execute("""
        CREATE OR REPLACE TABLE popularity_distribution AS
        SELECT
            CASE
                WHEN popularity BETWEEN 0 AND 20 THEN '0-20'
                WHEN popularity BETWEEN 21 AND 40 THEN '21-40'
                WHEN popularity BETWEEN 41 AND 60 THEN '41-60'
                WHEN popularity BETWEEN 61 AND 80 THEN '61-80'
                ELSE '81-100'
            END AS popularity_bucket,
            COUNT(*) AS total_tracks
        FROM silver
        GROUP BY popularity_bucket
        ORDER BY popularity_bucket;
    """)

    rows = con.execute("""
        SELECT COUNT(*)
        FROM popularity_distribution
    """).fetchone()[0]

    print(f"Created popularity_distribution ({rows} rows)")


def create_audio_feature_summary(con):
    """
    Create overall audio feature summary.
    """
    con.execute("""
        CREATE OR REPLACE TABLE audio_feature_summary AS
        SELECT
            ROUND(AVG(danceability), 3) AS avg_danceability,
            ROUND(AVG(energy), 3) AS avg_energy,
            ROUND(AVG(acousticness), 3) AS avg_acousticness,
            ROUND(AVG(valence), 3) AS avg_valence,
            ROUND(AVG(liveness), 3) AS avg_liveness,
            ROUND(AVG(speechiness), 3) AS avg_speechiness
        FROM silver;
    """)

    print("Created audio_feature_summary (1 row)")


def transform(con):
    """
    Run all Gold transformations.
    """
    create_artist_summary(con)
    create_genre_summary(con)
    create_explicit_summary(con)
    create_popularity_distribution(con)
    create_audio_feature_summary(con)