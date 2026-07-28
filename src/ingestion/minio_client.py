import os

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()


class MinIOClient:
    def __init__(self):
        self.bucket = os.getenv("MINIO_BUCKET")

        self.s3 = boto3.client(
            "s3",
            endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT')}",
            aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
            aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
        )

    def create_bucket_if_not_exists(self):
        """
        Create the bucket if it does not already exist.
        """
        try:
            self.s3.head_bucket(Bucket=self.bucket)
            print(f"Bucket '{self.bucket}' already exists.")

        except ClientError as e:
            code = e.response["Error"]["Code"]

            if code in ("404", "NoSuchBucket"):
                self.s3.create_bucket(Bucket=self.bucket)
                print(f"Bucket '{self.bucket}' created.")
            else:
                raise

    def upload_file(self, local_path: str, object_name: str):
        """
        Upload a local file to MinIO.
        """
        self.s3.upload_file(
            Filename=local_path,
            Bucket=self.bucket,
            Key=object_name,
        )

        print(f"Uploaded '{object_name}'")

    def download_file(self, object_name: str, local_path: str):
        """
        Download an object from MinIO.
        """
        self.s3.download_file(
            Bucket=self.bucket,
            Key=object_name,
            Filename=local_path,
        )

        print(f"Downloaded '{object_name}'")

    def object_exists(self, object_name: str) -> bool:
        """
        Check whether an object exists in MinIO.
        """
        try:
            self.s3.head_object(
                Bucket=self.bucket,
                Key=object_name,
            )
            return True

        except ClientError:
            return False

    def get_latest_object(self, prefix: str, filename: str) -> str:
        """
        Returns the latest object matching:

            <prefix>/ingestion_date=YYYY-MM-DD/<filename>

        Example:
            prefix="silver/spotify"
            filename="dataset.parquet"

        Returns:
            silver/spotify/ingestion_date=2026-07-26/dataset.parquet
        """

        paginator = self.s3.get_paginator("list_objects_v2")

        pages = paginator.paginate(
            Bucket=self.bucket,
            Prefix=prefix,
        )

        pattern = re.compile(r"ingestion_date=(\d{4}-\d{2}-\d{2})")

        latest_date = None
        latest_key = None

        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]

                if not key.endswith(filename):
                    continue

                match = pattern.search(key)

                if not match:
                    continue

                current_date = datetime.strptime(
                    match.group(1),
                    "%Y-%m-%d",
                ).date()

                if latest_date is None or current_date > latest_date:
                    latest_date = current_date
                    latest_key = key

        if latest_key is None:
            raise FileNotFoundError(
                f"No '{filename}' found under '{prefix}'"
            )

        print(f"Using latest object: {latest_key}")

        return latest_key