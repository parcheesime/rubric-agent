"""Shared document-ingestion workflow."""

from datetime import datetime, timezone
import mimetypes
from pathlib import Path
from typing import Any

from collectors.shared.checksum import calculate_sha256
from collectors.shared.ids import create_rubric_id
from collectors.shared.storage import (
    object_exists,
    upload_file,
    upload_json,
)


def ingest_rubric(
    file_path: str | Path,
    *,
    source_type: str,
    source_url: str | None = None,
    additional_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Add one rubric document to the R2 corpus.

    Returns metadata describing whether the document was uploaded
    or already existed.
    """

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Rubric file does not exist: {path}")

    checksum = calculate_sha256(path)
    rubric_id = create_rubric_id(checksum)

    extension = path.suffix.lower() or ".bin"
    raw_object_key = f"raw/{source_type}/{rubric_id}{extension}"
    metadata_object_key = f"metadata/{rubric_id}.json"

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
        "rubric_id": rubric_id,
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