# Storage

## Purpose

The Rubric Agent separates application code from the educational corpus it processes.

This repository contains the software, schemas, documentation, and tests that define the ingestion pipeline. The production corpus and all derived artifacts are stored in cloud object storage rather than the Git repository.

This approach keeps the repository lightweight, allows the corpus to scale independently, and supports reproducible processing.

---

## Design Principles

The storage system follows several principles:

- The Git repository contains code, documentation, schemas, and test fixtures.
- Cloud object storage is the authoritative location for collected data.
- Original source documents are preserved without modification.
- Each processing stage produces a new artifact rather than overwriting previous outputs.
- Every artifact maintains provenance linking it back to its original source.
- Temporary local files may be deleted after successful processing.

---

## Storage Layers

### Source Systems

Educational materials originate from open, external sources, including:

- Institutional repositories
- University course websites
- Open Educational Resource (OER) collections
- Public educational websites
- Manual imports

Rubric Agent records where a document originated but does not replace the source system.

---

### Local Workspace

Small local directories are used only during collection and processing.

```text
incoming/
tmp/
tests/fixtures/
```

These directories may contain:

- manually imported files
- temporary downloads
- OCR intermediate files
- processing logs
- test documents

They are not considered part of the permanent corpus.

---

### Cloud Object Storage

Cloudflare R2 is the authoritative storage location for the production corpus.

Each processing stage produces an independent object.

Example object layout:

```text
originals/
metadata/
extracted/
normalized/
interpretations/
index/
```

Objects are referenced using stable identifiers assigned during ingestion.

---

## Artifact Types

Each document may produce several related artifacts.

| Artifact | Purpose |
|----------|---------|
| Original | Unmodified source document |
| Metadata | Provenance, licensing, checksums, processing status |
| Extracted | Machine-readable representation of the original document |
| Normalized | Format-independent schema used throughout the project |
| Interpretation | Higher-level educational understanding generated from normalized content |
| Index | Search structures used by downstream applications |

---

## Processing Lifecycle

```text
External Source
      │
      ▼
Temporary Download
      │
      ▼
Metadata + Checksum
      │
      ▼
Original Upload
      │
      ▼
Extraction
      │
      ▼
Normalization
      │
      ▼
Interpretation
      │
      ▼
Indexing
```

Each stage creates a new artifact while preserving previous outputs.

---

## Object Naming

Artifacts are stored using stable identifiers rather than original filenames.

Example:

```text
originals/doc_3f84d2.pdf
metadata/doc_3f84d2.json
extracted/doc_3f84d2.json
normalized/doc_3f84d2.json
interpretations/doc_3f84d2.json
```

Original filenames and source information are preserved in metadata.

---

## Versioning

Processing pipelines evolve over time. Artifacts should record the versions used to produce them, including:

- ingestion pipeline
- extraction pipeline
- schema
- OCR engine
- normalization
- interpretation

This enables reproducibility and future reprocessing without losing historical outputs.

---

## Repository Responsibilities

The Git repository contains:

- source code
- documentation
- schemas
- tests
- sample data

The repository intentionally does **not** contain the production educational corpus.

---

## Future Work

Potential enhancements include:

- object lifecycle policies
- automatic deduplication
- content-addressable storage
- incremental reprocessing
- storage provider abstraction
- dataset releases
- distributed search indexes