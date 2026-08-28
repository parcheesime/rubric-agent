"""Shared collection logging utilities."""

from datetime import datetime, timezone
from typing import Any

from collectors.shared.storage import upload_json


def create_collection_log(
    *,
    source: str,
    collection: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a collection log for one collector run."""

    run_at = datetime.now(timezone.utc).isoformat()

    collected_count = sum(
        result.get("status") == "collected"
        for result in results
    )
    duplicate_count = sum(
        result.get("status") == "duplicate"
        for result in results
    )
    failed_count = sum(
        result.get("status") == "failed"
        for result in results
    )

    return {
        "source": source,
        "collection": collection,
        "run_at": run_at,
        "files_checked": len(results),
        "collected": collected_count,
        "duplicates": duplicate_count,
        "failed": failed_count,
        "results": results,
    }


def upload_collection_log(
    log: dict[str, Any],
    *,
    source: str,
    collection_path: str,
) -> str:
    """Upload a collection log to R2."""

    timestamp = (
        datetime.fromisoformat(log["run_at"])
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
        .replace(":", "-")
    )

    object_key = (
        f"metadata/collection_logs/"
        f"{source}/"
        f"{collection_path}/"
        f"{timestamp}.json"
    )

    return upload_json(log, object_key)