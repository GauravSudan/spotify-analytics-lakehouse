import duckdb


def get_connection(database=":memory:"):
    """
    Returns a DuckDB connection.
    Uses an in-memory database by default.
    """
    return duckdb.connect(database=database)