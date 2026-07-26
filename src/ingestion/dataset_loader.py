from pathlib import Path

import pandas as pd

# Required columns for validation
REQUIRED_COLUMNS = [
    "track_id",
    "track_name",
    "artists",
    "album_name",
    "popularity",
    "duration_ms",
    "danceability",
    "energy",
    "track_genre",
]


def load_dataset(dataset_path: str | Path) -> pd.DataFrame:
    """
    Load the Spotify dataset from CSV.

    Args:
        dataset_path: Path to the dataset CSV.

    Returns:
        pandas.DataFrame

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        ValueError: If the dataset is empty or missing required columns.
    """

    dataset_path = Path(dataset_path)

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {dataset_path}"
        )

    df = pd.read_csv(dataset_path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df