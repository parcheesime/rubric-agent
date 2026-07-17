"""Cloudflare R2 storage operations."""

import json
from pathlib import Path
from typing import Any

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

def object_exists(object_key: str) -> bool:
    """Return True when an object already exists in R2."""

    config = get_r2_config()
    client = get_r2_client()

    try:
        client.head_object(
            Bucket=config.bucket_name,
            Key=object_key,
        )
        return True
    except ClientError as error:
        status_code = error.response.get("ResponseMetadata", {}).get(
            "HTTPStatusCode"
        )

        if status_code == 404:
            return False

        raise RuntimeError(
            f"Could not check R2 object: {object_key}"
        ) from error


def upload_json(
    data: dict[str, Any],
    object_key: str,
) -> str:
    """Serialize a dictionary and upload it to R2 as JSON."""

    config = get_r2_config()
    client = get_r2_client()

    body = json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")

    try:
        client.put_object(
            Bucket=config.bucket_name,
            Key=object_key,
            Body=body,
            ContentType="application/json",
        )
    except ClientError as error:
        raise RuntimeError(
            f"Could not upload JSON to R2: {object_key}"
        ) from error

    return object_key