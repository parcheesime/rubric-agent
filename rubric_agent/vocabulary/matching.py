"""Normalize metadata field names and match complete vocabulary terms."""

import re

from rubric_agent.vocabulary.educational_terms import ALL_CATEGORIES


def normalize_metadata_key(name: str) -> str:
    """Convert camelCase and whitespace/hyphen separators to snake_case."""
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return re.sub(r"[\s_-]+", "_", name).strip("_").lower()


def match_metadata_key(name: str) -> list[tuple[str, str]]:
    """Return (category, canonical term) pairs for exact normalized matches."""
    normalized_key = normalize_metadata_key(name)
    return [
        (category, term)
        for category, terms in ALL_CATEGORIES.items()
        for term in terms
        if normalized_key == normalize_metadata_key(term)
    ]
