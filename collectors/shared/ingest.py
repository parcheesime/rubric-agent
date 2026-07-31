"""Shared educational-resource ingestion workflow."""

from datetime import datetime, timezone
import mimetypes
from pathlib import Path
from typing import Any

from collectors.shared.checksum import calculate_sha256
from collectors.shared.ids import create_resource_id
from collectors.shared.storage import (
    object_exists,
    upload_file,
    upload_json,
)


def ingest_resource(
    file_path: str | Path,
    *,
    source_type: str,
    source_url: str | None = None,
    resource_type: str | None = None,
    additional_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Add one educational resource to the corpus.

    Return metadata describing whether the resource was uploaded
    or already existed.
    """

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Resource file does not exist: {path}")

    checksum = calculate_sha256(path)

    resource_id = create_resource_id(checksum)

    extension = path.suffix.lower() or ".bin"
    raw_object_key = f"raw/{source_type}/{resource_id}{extension}"
    metadata_object_key = f"metadata/{resource_id}.json"

    already_exists = object_exists(raw_object_key)

    content_type, _ = mimetypes.guess_type(path.name)
    content_type = content_type or "application/octet-stream"

    if not already_exists:
        upload_file(
            local_path=path,
            object_key=raw_object_key,
            content_type=content_type,
        )

    metadata: dict[str, Any] = {
        "resource_id": resource_id,
        "resource_type": resource_type,
        "sha256": checksum,
        "original_filename": path.name,
        "file_extension": extension,
        "content_type": content_type,
        "file_size_bytes": path.stat().st_size,
        "source_type": source_type,
        "source_url": source_url,
        "raw_object_key": raw_object_key,
        "metadata_object_key": metadata_object_key,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "duplicate": already_exists,
    }

    if additional_metadata:
        metadata["additional_metadata"] = additional_metadata

    if not object_exists(metadata_object_key):
        upload_json(metadata, metadata_object_key)

    return metadata
