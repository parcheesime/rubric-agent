"""Utilities for calculating file checksums."""

from hashlib import sha256
from pathlib import Path


def calculate_sha256(file_path: str | Path) -> str:
    """Return the SHA-256 checksum of a file."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {path}")

    digest = sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()