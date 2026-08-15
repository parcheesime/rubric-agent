"""Tests for corpus identifier utilities."""

import pytest

from collectors.shared.ids import create_resource_id


def test_create_resource_id_returns_expected_id():
    """Create the expected resource ID from a SHA-256 checksum."""

    checksum = "a" * 64

    assert create_resource_id(checksum) == f"resource_{'a' * 16}"


def test_create_resource_id_uses_first_16_checksum_characters():
    """Use only the first 16 characters of the checksum."""

    checksum = "1234567890abcdef" + "a" * 48

    assert create_resource_id(checksum) == "resource_1234567890abcdef"


@pytest.mark.parametrize(
    "checksum",
    [
        "",
        "a" * 63,
        "a" * 65,
    ],
)
def test_create_resource_id_rejects_invalid_checksum_length(checksum):
    """Reject checksums that are not exactly 64 characters."""

    with pytest.raises(
        ValueError,
        match="Expected a 64-character SHA-256 checksum",
    ):
        create_resource_id(checksum)