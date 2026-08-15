"""Tests for checksum utilities."""

from hashlib import sha256

import pytest

from collectors.shared.checksum import calculate_sha256


def test_calculate_sha256_returns_expected_checksum(tmp_path):
    """Return the expected SHA-256 checksum for a file."""

    file_path = tmp_path / "sample.txt"
    content = b"rubric agent"
    file_path.write_bytes(content)

    expected = sha256(content).hexdigest()

    assert calculate_sha256(file_path) == expected


def test_calculate_sha256_is_deterministic(tmp_path):
    """Return the same checksum for files with identical contents."""

    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("same content")
    second_file.write_text("same content")

    assert calculate_sha256(first_file) == calculate_sha256(second_file)


def test_calculate_sha256_changes_with_content(tmp_path):
    """Return different checksums for different file contents."""

    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("first")
    second_file.write_text("second")

    assert calculate_sha256(first_file) != calculate_sha256(second_file)


def test_calculate_sha256_raises_for_missing_file(tmp_path):
    """Raise FileNotFoundError when the file does not exist."""

    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        calculate_sha256(missing_file)