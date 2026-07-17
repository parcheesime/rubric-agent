"""Download and ingest rubric PDFs discovered on Exemplars."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path
from typing import Any

import requests

from collectors.exemplars.search import (
    DEFAULT_HEADERS,
    RubricCandidate,
    discover_all_rubrics,
)
from collectors.shared.ingest import ingest_rubric


DOWNLOAD_TIMEOUT = 60
DOWNLOAD_CHUNK_SIZE = 1024 * 64


class DownloadError(Exception):
    """Raised when a rubric document cannot be safely downloaded."""


def download_candidate(
    candidate: RubricCandidate,
    *,
    session: requests.Session,
) -> Path:
    """Download a rubric PDF into a temporary file.

    The caller is responsible for deleting the returned file.
    """

    response = session.get(
        candidate.document_url,
        headers=DEFAULT_HEADERS,
        timeout=DOWNLOAD_TIMEOUT,
        stream=True,
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()

    if content_type and (
        "application/pdf" not in content_type
        and "application/octet-stream" not in content_type
    ):
        raise DownloadError(
            f"Unexpected Content-Type for {candidate.document_url}: "
            f"{content_type}"
        )

    temp_file = tempfile.NamedTemporaryFile(
        mode="wb",
        suffix=".pdf",
        prefix="exemplars_",
        delete=False,
    )

    temp_path = Path(temp_file.name)

    try:
        with temp_file:
            for chunk in response.iter_content(
                chunk_size=DOWNLOAD_CHUNK_SIZE
            ):
                if chunk:
                    temp_file.write(chunk)

        if temp_path.stat().st_size == 0:
            raise DownloadError(
                f"Downloaded file is empty: {candidate.document_url}"
            )

        with temp_path.open("rb") as file:
            signature = file.read(5)

        if signature != b"%PDF-":
            raise DownloadError(
                f"Downloaded file does not have a PDF signature: "
                f"{candidate.document_url}"
            )

        return temp_path

    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def ingest_candidate(
    candidate: RubricCandidate,
    *,
    session: requests.Session,
) -> Any:
    """Download one candidate and pass it to the shared ingestion pipeline."""

    temp_path = download_candidate(
        candidate,
        session=session,
    )

    try:
        print(f"Temporary download: {temp_path}")
        print(f"Temporary size: {temp_path.stat().st_size} bytes")
        print("Calling ingest_rubric...")

        result = ingest_rubric(
            temp_path,
            source_type="exemplars",
            source_url=candidate.source_url,
            additional_metadata={
                "title": candidate.title,
                "collection": candidate.subject,
                "document_url": candidate.document_url,
                "language": "en",
                "provider": "Exemplars",
                "original_filename": Path(candidate.document_url).name,
            },
        )

        print("ingest_rubric returned:", result)
        return result
    finally:
        temp_path.unlink(missing_ok=True)


def collect_rubrics(
    *,
    limit: int | None = None,
) -> dict[str, int]:
    """Discover, download, and ingest Exemplars rubric PDFs."""

    candidates = discover_all_rubrics()

    if limit is not None:
        candidates = candidates[:limit]

    totals = {
        "discovered": len(candidates),
        "succeeded": 0,
        "failed": 0,
    }

    if not candidates:
        print("No rubric candidates were discovered.")
        return totals

    print(f"Discovered {len(candidates)} rubric candidates.")

    with requests.Session() as session:
        for index, candidate in enumerate(candidates, start=1):
            print()
            print(
                f"[{index}/{len(candidates)}] "
                f"{candidate.title}"
            )
            print(f"Collection: {candidate.subject}")
            print(f"Document: {candidate.document_url}")

            try:
                result = ingest_candidate(
                    candidate,
                    session=session,
                )

                totals["succeeded"] += 1
                print("Result:", result)

            except requests.RequestException as error:
                totals["failed"] += 1
                print(f"Download request failed: {error}")

            except DownloadError as error:
                totals["failed"] += 1
                print(f"Download validation failed: {error}")

            except Exception as error:
                totals["failed"] += 1
                print(
                    f"Ingestion failed: "
                    f"{type(error).__name__}: {error}"
                )

    print()
    print("Collection complete")
    print("-------------------")
    print(f"Discovered: {totals['discovered']}")
    print(f"Succeeded:  {totals['succeeded']}")
    print(f"Failed:     {totals['failed']}")

    return totals


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Discover and ingest rubric PDFs from Exemplars."
        )
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only process the first N discovered rubrics.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the Exemplars collector."""

    args = parse_args()

    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    totals = collect_rubrics(limit=args.limit)

    if totals["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()