"""Cloudflare R2 storage operations."""

from pathlib import Path

import boto3
from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError, ClientError

from collectors.shared.config import get_r2_config


def get_r2_client() -> BaseClient:
    """Create and return an authenticated Cloudflare R2 client."""

    config = get_r2_config()

    return boto3.client(
        service_name="s3",
        endpoint_url=config.endpoint_url,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        region_name="auto",
    )


def upload_file(
    local_path: str | Path,
    object_key: str,
    *,
    content_type: str | None = None,
) -> str:
    """
    Upload a local file to the configured Cloudflare R2 bucket.

    Args:
        local_path:
            Path to the local file.
        object_key:
            Destination path inside the bucket, such as
            ``raw/manual/example.pdf``.
        content_type:
            Optional MIME type, such as ``application/pdf``.

    Returns:
        The uploaded object's key.

    Raises:
        FileNotFoundError:
            If the local file does not exist.
        RuntimeError:
            If the R2 upload fails.
    """

    file_path = Path(local_path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Upload source file does not exist: {file_path}"
        )

    config = get_r2_config()
    client = get_r2_client()

    extra_args = {}

    if content_type:
        extra_args["ContentType"] = content_type

    try:
        client.upload_file(
            Filename=str(file_path),
            Bucket=config.bucket_name,
            Key=object_key,
            ExtraArgs=extra_args or None,
        )
    except (BotoCoreError, ClientError) as error:
        raise RuntimeError(
            f"Could not upload {file_path} to "
            f"r2://{config.bucket_name}/{object_key}"
        ) from error

    return object_key