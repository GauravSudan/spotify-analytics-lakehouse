from src.ingestion.minio_client import MinIOClient

client = MinIOClient()

client.create_bucket_if_not_exists()

client.upload_file(
    "datasets/dataset.csv",
    "raw/spotify/dataset.csv",
)