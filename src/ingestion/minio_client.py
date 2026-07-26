import os

from dotenv import load_dotenv
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

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
        self.s3.upload_file(
            Filename=local_path,
            Bucket=self.bucket,
            Key=object_name,
        )
        print(f"Uploaded '{object_name}'")