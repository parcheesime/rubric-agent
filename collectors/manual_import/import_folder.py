"""Import rubric files from the manual-import incoming directory."""

from pathlib import Path

from collectors.shared.ingest import ingest_rubric


INCOMING_DIRECTORY = Path("collectors/manual_import/incoming")

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".html",
    ".htm",
    ".rtf",
    ".odt",
    ".xlsx",
    ".xls",
    ".csv",
}


def find_rubric_files(directory: Path) -> list[Path]:
    """Return supported rubric files in a directory."""

    if not directory.exists():
        raise FileNotFoundError(
            f"Incoming directory does not exist: {directory}"
        )

    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def main() -> None:
    """Upload all supported files from the incoming directory."""

    files = find_rubric_files(INCOMING_DIRECTORY)

    if not files:
        print(f"No rubric files found in {INCOMING_DIRECTORY}")
        return

    uploaded = 0
    duplicates = 0
    failed = 0

    for file_path in files:
        try:
            result = ingest_rubric(
                file_path,
                source_type="manual_import",
            )

            if result["duplicate"]:
                duplicates += 1
                print(f"SKIPPED duplicate: {file_path.name}")
            else:
                uploaded += 1
                print(
                    f"UPLOADED: {file_path.name} "
                    f"-> {result['raw_object_key']}"
                )

        except Exception as error:
            failed += 1
            print(f"FAILED: {file_path.name}: {error}")

    print()
    print("Import complete")
    print(f"Uploaded:   {uploaded}")
    print(f"Duplicates: {duplicates}")
    print(f"Failed:     {failed}")


if __name__ == "__main__":
    main()