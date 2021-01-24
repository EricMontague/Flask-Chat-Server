""""This module contains a repository class to act as an abstraction
on file storage in S3.
"""


import os
import boto3
from botocore.exceptions import ClientError
from app.repositories.abstract_repository import FileStorageRepository
from app.repositories.utils import encode_file_contents


class _S3Repository(FileStorageRepository):
    """Class to interact with the S3 client from the boto3 library."""

    def __init__(self, region):
        self._s3_client = boto3.client("s3", region)
        self._bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")

    def get(self, file_id):
        """Return the contents of a file from S3 as bytes."""
        try:
            response = self._s3_client.get_object(Key=file_id, Bucket=self._bucket_name)
            return response["Body"].read()
        except ClientError:
            return None

    def add(self, file_id, file_contents):
        """Add a new file to S3. If a file with the given file_id already exists,
        it is replaced. File contents should be in bytes.
        """
        response = self._s3_client.put_object(
            Body=file_contents,
            Bucket="chat-app-images",
            Key=file_id,
            StorageClass="STANDARD",
            ContentMD5=encode_file_contents(file_contents),
        )
        return True

    def remove(self, file_id):
        """Delete a file from S3."""
        response = self._s3_client.delete_object(Bucket=self._bucket_name, Key=file_id)
        return True


file_repository = _S3Repository(os.environ.get("AWS_DEFAULT_REGION"))
