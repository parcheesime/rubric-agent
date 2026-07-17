"""Smoke test for uploading a local file to Cloudflare R2."""

from pathlib import Path

from collectors.shared.storage import upload_file


def main() -> None:
    """Create and upload a small test file."""

    test_file = Path("tmp/r2-upload-test.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)

    test_file.write_text(
        "Rubric Agent R2 upload test.\n",
        encoding="utf-8",
    )

    object_key = upload_file(
        local_path=test_file,
        object_key="tests/r2-upload-test.txt",
        content_type="text/plain",
    )

    print(f"Upload successful: {object_key}")


if __name__ == "__main__":
    main()