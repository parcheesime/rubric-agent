"""Utilities for generating stable corpus identifiers."""


def create_resource_id(checksum: str) -> str:
    """Create a stable resource ID from a SHA-256 checksum."""

    if len(checksum) != 64:
        raise ValueError("Expected a 64-character SHA-256 checksum")

    return f"rubric_{checksum[:16]}"
