"""Tests for the shared resource ingestion workflow."""

from unittest.mock import patch

import pytest

from collectors.shared.ingest import ingest_resource


def test_ingest_resource_raises_for_missing_file(tmp_path):
    """Raise FileNotFoundError when the resource file does not exist."""

    missing_file = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        ingest_resource(
            missing_file,
            source_type="manual",
        )


@patch("collectors.shared.ingest.upload_json")
@patch("collectors.shared.ingest.upload_file")
@patch("collectors.shared.ingest.object_exists")
def test_ingest_resource_uploads_new_resource(
    mock_object_exists,
    mock_upload_file,
    mock_upload_json,
    tmp_path,
):
    """Upload the raw file and metadata for a new resource."""

    file_path = tmp_path / "rubric.pdf"
    file_path.write_bytes(b"sample rubric")

    # raw object does not exist
    # metadata object does not exist
    mock_object_exists.side_effect = [False, False]

    metadata = ingest_resource(
        file_path,
        source_type="manual",
        source_url="https://example.com/rubric",
        resource_type="rubric",
    )

    mock_upload_file.assert_called_once()
    mock_upload_json.assert_called_once()

    assert metadata["resource_type"] == "rubric"
    assert metadata["source_type"] == "manual"
    assert metadata["source_url"] == "https://example.com/rubric"
    assert metadata["duplicate"] is False
    assert metadata["original_filename"] == "rubric.pdf"
    assert metadata["file_extension"] == ".pdf"
    assert metadata["content_type"] == "application/pdf"

    assert metadata["resource_id"].startswith("resource_")
    assert metadata["raw_object_key"].startswith("raw/manual/resource_")
    assert metadata["metadata_object_key"].startswith("metadata/resource_")


@patch("collectors.shared.ingest.upload_json")
@patch("collectors.shared.ingest.upload_file")
@patch("collectors.shared.ingest.object_exists")
def test_ingest_resource_skips_raw_upload_for_duplicate(
    mock_object_exists,
    mock_upload_file,
    mock_upload_json,
    tmp_path,
):
    """Do not upload the raw object again when it already exists."""

    file_path = tmp_path / "rubric.pdf"
    file_path.write_bytes(b"sample rubric")

    # raw object exists
    # metadata object exists
    mock_object_exists.side_effect = [True, True]

    metadata = ingest_resource(
        file_path,
        source_type="manual",
    )

    mock_upload_file.assert_not_called()
    mock_upload_json.assert_not_called()

    assert metadata["duplicate"] is True


@patch("collectors.shared.ingest.upload_json")
@patch("collectors.shared.ingest.upload_file")
@patch("collectors.shared.ingest.object_exists")
def test_ingest_resource_includes_additional_metadata(
    mock_object_exists,
    mock_upload_file,
    mock_upload_json,
    tmp_path,
):
    """Preserve source-specific metadata."""

    file_path = tmp_path / "lesson.txt"
    file_path.write_text("sample lesson")

    mock_object_exists.side_effect = [False, False]

    additional_metadata = {
        "grade_level": "6",
        "subject": "mathematics",
    }

    metadata = ingest_resource(
        file_path,
        source_type="example_source",
        resource_type="lesson",
        additional_metadata=additional_metadata,
    )

    assert metadata["additional_metadata"] == additional_metadata


@patch("collectors.shared.ingest.upload_json")
@patch("collectors.shared.ingest.upload_file")
@patch("collectors.shared.ingest.object_exists")
def test_ingest_resource_restores_missing_metadata(
    mock_object_exists,
    mock_upload_file,
    mock_upload_json,
    tmp_path,
):
    """Upload metadata when the raw resource exists but metadata is missing."""

    file_path = tmp_path / "rubric.pdf"
    file_path.write_bytes(b"sample rubric")

    # Raw object exists, metadata object does not.
    mock_object_exists.side_effect = [True, False]

    metadata = ingest_resource(
        file_path,
        source_type="manual",
        resource_type="rubric",
    )

    mock_upload_file.assert_not_called()
    mock_upload_json.assert_called_once()

    assert metadata["duplicate"] is True