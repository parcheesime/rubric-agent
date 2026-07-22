"""Reclassify document metadata stored in Cloudflare R2.

This script identifies known metadata upload batches by local timestamp and
updates their classification fields.

It runs in dry-run mode by default.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

import boto3
from botocore.client import BaseClient
from dotenv import load_dotenv


DEFAULT_TIMEZONE = "America/Los_Angeles"
DEFAULT_METADATA_PREFIX = "metadata/"


def create_r2_client() -> BaseClient:
    """Create an S3-compatible client for Cloudflare R2."""
    load_dotenv()

    required_variables = (
        "R2_ENDPOINT_URL",
        "R2_ACCESS_KEY_ID",
        "R2_SECRET_ACCESS_KEY",
        "R2_BUCKET_NAME",
    )

    missing = [name for name in required_variables if not os.getenv(name)]

    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT_URL"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )


def list_objects(client: BaseClient, bucket: str, prefix: str) -> list[dict[str, Any]]:
    """List every R2 object beneath a prefix."""
    paginator = client.get_paginator("list_objects_v2")
    objects: list[dict[str, Any]] = []

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        objects.extend(page.get("Contents", []))

    return objects


def read_json_object(
    client: BaseClient,
    bucket: str,
    key: str,
) -> dict[str, Any]:
    """Download and parse one JSON object."""
    response = client.get_object(Bucket=bucket, Key=key)
    contents = response["Body"].read().decode("utf-8")
    return json.loads(contents)


def get_classification(
    last_modified: datetime,
    target_date: str,
    timezone_name: str,
) -> dict[str, str] | None:
    """Return the classification for a known upload batch."""
    local_modified = last_modified.astimezone(ZoneInfo(timezone_name))
    selected_date = datetime.strptime(target_date, "%Y-%m-%d").date()

    if local_modified.date() != selected_date:
        return None

    if local_modified.hour == 9:
        return {
            "document_type": "rubric",
            "corpus_status": "included",
            "reason": "Verified actual rubric.",
        }

    if local_modified.hour == 14:
        return {
            "document_type": "rubric_guidance",
            "corpus_status": "excluded",
            "reason": "How-to material rather than an actual rubric.",
        }

    return None


def update_classification(
    metadata: dict[str, Any],
    classification: dict[str, str],
) -> dict[str, Any]:
    """Apply a manual classification decision."""
    updated = dict(metadata)

    updated["metadata_version"] = 2
    updated["document_type"] = classification["document_type"]
    updated["corpus_status"] = classification["corpus_status"]

    review = dict(updated.get("review", {}))
    review.update(
        {
            "status": classification["corpus_status"],
            "review_method": "manual",
            "reason": classification["reason"],
            "reviewed_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    updated["review"] = review

    if classification["corpus_status"] == "excluded":
        updated["exclusion_reason"] = classification["reason"]
    else:
        updated.pop("exclusion_reason", None)

    return updated


def write_json_object(
    client: BaseClient,
    bucket: str,
    key: str,
    metadata: dict[str, Any],
) -> None:
    """Write updated JSON back to the same R2 key."""
    body = json.dumps(metadata, indent=2, ensure_ascii=False) + "\n"

    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="application/json",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reclassify known R2 metadata upload batches."
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Local upload date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--timezone",
        default=DEFAULT_TIMEZONE,
        help=f"IANA timezone name. Default: {DEFAULT_TIMEZONE}",
    )
    parser.add_argument(
        "--prefix",
        default=DEFAULT_METADATA_PREFIX,
        help=f"R2 metadata prefix. Default: {DEFAULT_METADATA_PREFIX}",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to R2. Without this flag, only preview changes.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_r2_client()
    bucket = os.environ["R2_BUCKET_NAME"]

    objects = list_objects(client, bucket, args.prefix)

    classified_objects: list[
        tuple[dict[str, Any], dict[str, str]]
    ] = []

    for item in objects:
        key = item["Key"]

        if not key.lower().endswith(".json"):
            continue

        classification = get_classification(
            last_modified=item["LastModified"],
            target_date=args.date,
            timezone_name=args.timezone,
        )

        if classification is not None:
            classified_objects.append((item, classification))

    if not classified_objects:
        print("No matching metadata records found.")
        return

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"\nMode: {mode}")
    print(f"Matching records: {len(classified_objects)}\n")

    for item, classification in classified_objects:
        key = item["Key"]
        local_modified = item["LastModified"].astimezone(
            ZoneInfo(args.timezone)
        )

        print(f"- {key}")
        print(f"  Last modified: {local_modified.isoformat()}")
        print(f"  Document type: {classification['document_type']}")
        print(f"  Corpus status: {classification['corpus_status']}")
        print(f"  Reason: {classification['reason']}")

        if args.apply:
            metadata = read_json_object(client, bucket, key)

            updated = update_classification(
                metadata,
                classification,
            )

            write_json_object(
                client,
                bucket,
                key,
                updated,
            )

            print("  Updated")
        else:
            print("  Would update")

        print()

    if not args.apply:
        print(
            "No changes were written. "
            "Add --apply after reviewing the list."
        )


if __name__ == "__main__":
    main()