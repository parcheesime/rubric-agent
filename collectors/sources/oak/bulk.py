"""Collect Oak bulk metadata into the Rubric Agent corpus."""

from pathlib import Path
import sys

from collectors.shared.checksum import calculate_sha256
from collectors.shared.collection_log import (
    create_collection_log,
    upload_collection_log,
)
from collectors.shared.ids import create_resource_id
from collectors.shared.storage import object_exists, upload_file


SOURCE = "oak"
COLLECTION = "primary-maths"
COLLECTION_PATH = "math/primary"
METADATA_PREFIX = "metadata/oak/math/primary"


def collect_file(file_path: Path) -> dict:
    """Collect one Oak metadata file into R2."""

    checksum = calculate_sha256(file_path)
    resource_id = create_resource_id(checksum)

    object_key = (
        f"{METADATA_PREFIX}/"
        f"{resource_id}{file_path.suffix.lower()}"
    )

    already_exists = object_exists(object_key)

    if not already_exists:
        upload_file(
            local_path=file_path,
            object_key=object_key,
            content_type="application/json",
        )

    return {
        "filename": file_path.name,
        "resource_id": resource_id,
        "sha256": checksum,
        "object_key": object_key,
        "status": "duplicate" if already_exists else "collected",
    }


def collect_directory(directory: Path) -> dict:
    """Collect all JSON files from an Oak bulk download."""

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Oak bulk directory does not exist: {directory}"
        )

    json_files = sorted(directory.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(
            f"No JSON files found in: {directory}"
        )

    results = []

    for file_path in json_files:
        try:
            result = collect_file(file_path)
        except Exception as error:
            result = {
                "filename": file_path.name,
                "status": "failed",
                "error": str(error),
            }

        results.append(result)

        print(
            f"{result['status'].upper()}: "
            f"{file_path.name}"
        )

    log = create_collection_log(
        source=SOURCE,
        collection=COLLECTION,
        results=results,
    )

    log_key = upload_collection_log(
        log,
        source=SOURCE,
        collection_path=COLLECTION_PATH,
    )

    print(f"Collection log: {log_key}")

    return log


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python -m collectors.sources.oak.collect "
            "<oak-bulk-directory>"
        )

    collect_directory(Path(sys.argv[1]))