"""S3 Client"""

from datetime import datetime, timedelta
import os
import uuid
from worker.models.s3_model import S3DB
import boto3
from worker.core.constants import (
    LOG_REPOSITORY,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_BUCKET_NAME,
)
from worker.core.logger_custom import log


class S3Client:
    """S3 Client Class"""

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        self.url_prefix = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/"

    async def upload_file(
        self,
        file_bytes: bytes,
        key_prefix: str,
        extension: str,
        bucket_name: str = AWS_BUCKET_NAME,
    ) -> dict:
        """Upload a file (image/video/other) to S3 with UUID and custom extension"""
        try:
            filename = f"{uuid.uuid4()}{extension}"
            key = f"{key_prefix}{filename}"

            self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=file_bytes)

            url = f"{self.url_prefix}{key}"
            log.info(f"{LOG_REPOSITORY} File uploaded to S3", extra=f"URL: {url}")
            return {"url": url, "filename": filename}

        except Exception as e:
            log.error(
                f"{LOG_REPOSITORY} Error uploading file to S3", extra=f"Error: {e}"
            )
            raise e


    async def preasigned_url(
        self, folder: str, key: str, content_type: str, expires_in: int = 3600
    ) -> S3DB:
        """Generate a preasigned URL for a given key in folder"""
        try:
            full_key = f"{folder}{key}"
            url = self.s3_client.generate_presigned_post(
                Bucket=AWS_BUCKET_NAME,
                Key=full_key,
                Fields={"Content-Type": content_type},
                Conditions=[
                    {"Content-Type": content_type},
                    ["starts-with", "$key", folder],
                ],
                ExpiresIn=expires_in,
            )
            log.info(f"{LOG_REPOSITORY} Preasigned URL generated", extra=f"URL: {url}")
            return S3DB(
                url=url["url"],
                key=full_key,
                filename=key,
                expires_at=datetime.now() + timedelta(seconds=expires_in),
                extra_info=url,
            )

        except Exception as e:
            log.error(
                f"{LOG_REPOSITORY} Error generating preasigned URL", extra=f"Error: {e}"
            )
            raise e
    async def download_file_small(self, key: str) -> bytes:
        """Download a file from S3"""
        try:
            response = self.s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=key)
            return response["Body"].read()
        except Exception as e:
            log.error(f"{LOG_REPOSITORY} Error downloading file from S3", extra=f"Error: {e}")
            return None


    def download_file_large(self, key: str, local_dir: str = "/tmp") -> str:
        """Descarga un archivo grande desde S3 y lo guarda en disco"""
        try:
            local_path = os.path.join(local_dir, os.path.basename(key))
            self.s3_client.download_file(AWS_BUCKET_NAME, key, local_path)
            return local_path
        except Exception as e:
            log.error(f"{LOG_REPOSITORY} Error downloading file from S3", extra=f"Error: {e}")
            return None

    