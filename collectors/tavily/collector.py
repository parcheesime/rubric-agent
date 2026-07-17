"""Review and optionally download syllabi discovered through Tavily."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests

from collectors.tavily.search import (
    SyllabusCandidate,
    discover_all_syllabi,
)


DOWNLOAD_TIMEOUT = 60
DOWNLOAD_CHUNK_SIZE = 64 * 1024

DEFAULT_OUTPUT_DIRECTORY = Path("corpus/syllabi/raw")
DEFAULT_MANIFEST_PATH = Path("corpus/syllabi/manifest.jsonl")

REQUEST_HEADERS = {
    "User-Agent": (
        "rubric-agent/0.1 "
        "(educational resource research; contact: YOUR_EMAIL)"
    ),
    "Accept": (
        "application/pdf,"
        "application/octet-stream;q=0.9,"
        "*/*;q=0.1"
    ),
}


class DownloadError(Exception):
    """Raised when a candidate cannot be downloaded as a valid PDF."""


def sanitize_filename(value: str) -> str:
    """Convert text into a safe filename component."""

    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "-", value)
    normalized = normalized.strip("-._")

    return normalized[:100] or "syllabus"


def filename_from_candidate(candidate: SyllabusCandidate) -> str:
    """Build a readable filename for a syllabus candidate."""

    url_filename = Path(
        unquote(urlparse(candidate.document_url).path)
    ).name

    if url_filename.lower().endswith(".pdf"):
        return sanitize_filename(url_filename[:-4]) + ".pdf"

    return sanitize_filename(candidate.title) + ".pdf"


def sha256_file(file_path: Path) -> str:
    """Calculate a file's SHA-256 checksum."""

    digest = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(DOWNLOAD_CHUNK_SIZE),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def download_candidate(
    candidate: SyllabusCandidate,
    *,
    session: requests.Session,
    output_directory: Path,
) -> tuple[Path, str]:
    """Download and validate one syllabus PDF."""

    response = session.get(
        candidate.document_url,
        headers=REQUEST_HEADERS,
        timeout=DOWNLOAD_TIMEOUT,
        stream=True,
        allow_redirects=True,
    )
    response.raise_for_status()

    output_directory.mkdir(parents=True, exist_ok=True)

    filename = filename_from_candidate(candidate)
    output_path = output_directory / filename

    temporary_path = output_path.with_suffix(".pdf.part")

    try:
        with temporary_path.open("wb") as file:
            for chunk in response.iter_content(
                chunk_size=DOWNLOAD_CHUNK_SIZE
            ):
                if chunk:
                    file.write(chunk)

        if temporary_path.stat().st_size == 0:
            raise DownloadError(
                f"Downloaded file is empty: {candidate.document_url}"
            )

        with temporary_path.open("rb") as file:
            signature = file.read(5)

        if signature != b"%PDF-":
            content_type = response.headers.get(
                "Content-Type",
                "missing",
            )

            raise DownloadError(
                "Downloaded content is not a PDF. "
                f"Content-Type: {content_type}; "
                f"URL: {candidate.document_url}"
            )

        checksum = sha256_file(temporary_path)

        if output_path.exists():
            existing_checksum = sha256_file(output_path)

            if existing_checksum == checksum:
                temporary_path.unlink()
                return output_path, checksum

            output_path = (
                output_directory
                / f"{output_path.stem}-{checksum[:8]}.pdf"
            )

        temporary_path.replace(output_path)

        return output_path, checksum

    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def write_manifest_entry(
    *,
    manifest_path: Path,
    candidate: SyllabusCandidate,
    status: str,
    local_path: Path | None = None,
    checksum: str | None = None,
    error: str | None = None,
) -> None:
    """Append one discovery or download result to JSON Lines."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        **asdict(candidate),
        "status": status,
        "local_path": str(local_path) if local_path else None,
        "checksum_sha256": checksum,
        "error": error,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    with manifest_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def display_candidates(
    candidates: list[SyllabusCandidate],
) -> None:
    """Print candidates with numbers for review and selection."""

    if not candidates:
        print("No likely syllabus PDFs were found.")
        return

    print(f"\nFound {len(candidates)} unique syllabus candidates.\n")

    for index, candidate in enumerate(candidates, start=1):
        print(f"[{index}] {candidate.title}")
        print(f"    URL:   {candidate.document_url}")
        print(f"    Query: {candidate.query}")
        print(f"    Score: {candidate.score}")
        print()


def select_candidates(
    candidates: list[SyllabusCandidate],
    selected_numbers: list[int] | None,
    limit: int | None,
) -> list[SyllabusCandidate]:
    """Select candidates using one-based result numbers or a limit."""

    if selected_numbers:
        invalid = [
            number
            for number in selected_numbers
            if number < 1 or number > len(candidates)
        ]

        if invalid:
            invalid_text = ", ".join(map(str, invalid))
            raise ValueError(
                f"Selection numbers out of range: {invalid_text}"
            )

        return [
            candidates[number - 1]
            for number in selected_numbers
        ]

    if limit is not None:
        return candidates[:limit]

    return candidates


def collect_syllabi(
    *,
    download: bool,
    selected_numbers: list[int] | None = None,
    limit: int | None = None,
    max_results_per_query: int = 5,
    queries: list[str] | None = None,
    output_directory: Path = DEFAULT_OUTPUT_DIRECTORY,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, int]:
    """Discover and optionally download syllabus candidates."""

    candidates = discover_all_syllabi(
        queries=queries,
        max_results_per_query=max_results_per_query,
    )

    display_candidates(candidates)

    totals = {
        "discovered": len(candidates),
        "selected": 0,
        "downloaded": 0,
        "failed": 0,
    }

    if not download:
        print(
            "Discovery only. Nothing was downloaded or uploaded to R2."
        )
        return totals

    selected_candidates = select_candidates(
        candidates,
        selected_numbers,
        limit,
    )

    totals["selected"] = len(selected_candidates)

    if not selected_candidates:
        print("No candidates selected for download.")
        return totals

    print(
        f"Downloading {len(selected_candidates)} "
        "selected syllabus candidates...\n"
    )

    with requests.Session() as session:
        for index, candidate in enumerate(
            selected_candidates,
            start=1,
        ):
            print(
                f"[{index}/{len(selected_candidates)}] "
                f"{candidate.title}"
            )

            try:
                local_path, checksum = download_candidate(
                    candidate,
                    session=session,
                    output_directory=output_directory,
                )

                totals["downloaded"] += 1

                write_manifest_entry(
                    manifest_path=manifest_path,
                    candidate=candidate,
                    status="downloaded",
                    local_path=local_path,
                    checksum=checksum,
                )

                print(f"Saved:    {local_path}")
                print(f"SHA-256:  {checksum}")

            except (
                requests.RequestException,
                DownloadError,
                OSError,
            ) as error:
                totals["failed"] += 1

                write_manifest_entry(
                    manifest_path=manifest_path,
                    candidate=candidate,
                    status="failed",
                    error=f"{type(error).__name__}: {error}",
                )

                print(
                    f"Failed: {type(error).__name__}: {error}"
                )

            print()

    print("Collection complete")
    print("-------------------")
    print(f"Discovered: {totals['discovered']}")
    print(f"Selected:   {totals['selected']}")
    print(f"Downloaded: {totals['downloaded']}")
    print(f"Failed:     {totals['failed']}")
    print(f"Manifest:   {manifest_path}")

    return totals


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(
        description=(
            "Discover and optionally download syllabus PDFs "
            "using Tavily."
        )
    )

    parser.add_argument(
        "--download",
        action="store_true",
        help="Download selected syllabus PDFs locally.",
    )

    parser.add_argument(
        "--select",
        type=int,
        nargs="+",
        default=None,
        help=(
            "Download specific one-based candidate numbers, "
            "such as --select 1 4 7."
        ),
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Use only the first N discovered candidates.",
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Maximum Tavily results requested per query.",
    )

    parser.add_argument(
        "--query",
        action="append",
        dest="queries",
        help=(
            "Use a custom syllabus query. Repeat this option "
            "to provide multiple queries."
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIRECTORY,
        help="Directory for downloaded syllabus PDFs.",
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
        help="JSONL manifest output path.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the Tavily syllabus collector."""

    args = parse_args()

    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    if not 1 <= args.max_results <= 20:
        raise SystemExit("--max-results must be between 1 and 20")

    if args.select and not args.download:
        raise SystemExit("--select requires --download")

    if args.limit is not None and args.select:
        raise SystemExit(
            "Use either --limit or --select, not both."
        )

    try:
        totals = collect_syllabi(
            download=args.download,
            selected_numbers=args.select,
            limit=args.limit,
            max_results_per_query=args.max_results,
            queries=args.queries,
            output_directory=args.output_dir,
            manifest_path=args.manifest,
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error

    if args.download and totals["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()