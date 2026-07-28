# Ingestion Pipeline

**Project:** Rubric Agent  
**Status:** Early design  
**Purpose:** Define the shared process for converting educational documents into traceable, machine-readable representations.

## Overview

The Rubric Agent ingestion pipeline receives educational documents from public collectors, manual imports, and future teacher uploads.

Its purpose is to preserve the source material, extract usable content, identify document structure and instructional meaning, and produce human-readable and machine-readable outputs for downstream applications.

The ingestion pipeline is shared infrastructure. Collectors are responsible primarily for discovering and retrieving resources, while ingestion components handle document processing consistently across sources.

## Goals

The pipeline should:

- Support multiple educational document types and file formats.
- Preserve provenance throughout processing.
- Keep original and derived artifacts separate.
- Produce reproducible, versioned outputs.
- Detect duplicates and revised documents.
- Record extraction failures and uncertainty.
- Support future reprocessing as parsers and schemas improve.
- Produce structured data usable by Site Sensei, DiscoverQuery, and future applications.

## Inputs

The pipeline may receive documents from:

- Scheduled public-source collectors
- Manual corpus imports
- Institutional repositories
- Open educational resource collections
- Future teacher uploads

Each input should arrive with available source metadata, including its origin, retrieval context, and licensing information.

## Pipeline Stages

### 1. Intake

The pipeline accepts a source document and its available metadata.

At intake, the system assigns or resolves a stable internal resource identifier and records the acquisition method.

### 2. Original Preservation

The original file is stored without altering its contents.

A checksum is generated to identify the exact file and support duplicate detection, integrity checks, and version tracking.

### 3. Format Inspection

The pipeline identifies the document format and determines which extraction strategy is appropriate.

Examples may include:

- Digitally generated PDF
- Scanned or image-only PDF
- HTML
- Markdown
- Plain text
- Office document formats

### 4. Content Extraction

Text, page boundaries, headings, tables, lists, and other available structural information are extracted.

Scanned documents may require OCR. Extraction methods and confidence information should be recorded.

### 5. Document Classification

The resource is classified by document type and relevant educational characteristics.

Examples include:

- Rubric
- Syllabus
- Assignment
- Lesson plan
- Worksheet
- Assessment
- Exam
- Course material

Classification may be revised as the interpretation system improves.

### 6. Educational Interpretation

The pipeline identifies instructional meaning within the document, including:

- Learning objectives
- Expected student knowledge and skills
- Deliverables
- Assessment criteria
- Performance levels
- Prerequisites
- Constraints
- Sequence or pacing
- Ambiguities requiring review

Interpretation outputs should distinguish source statements from system-generated conclusions.

### 7. Human-Readable Output

The system produces a review describing what it understood from the document.

This output should communicate:

- What students are expected to know or produce
- How student work may be evaluated
- Important requirements and constraints
- Assumptions made by the system
- Missing or ambiguous information
- Questions that may require teacher confirmation

### 8. Machine-Readable Normalization

The interpreted document is converted into a structured representation using project schemas.

Normalized records may include:

- Document identity
- Provenance
- Educational objectives
- Assessment criteria
- Tags
- Relationships
- Structural sections
- Processing metadata
- Confidence or review status

### 9. Validation

Outputs are checked for schema validity, required provenance, internal consistency, and processing completeness.

Validation failures should be recorded rather than silently ignored.

### 10. Storage and Indexing

The pipeline stores original documents and derived artifacts separately.

Typical artifact categories include:

- Original source file
- Extracted text
- Structural extraction
- Metadata
- Human-readable interpretation
- Normalized JSON
- Processing logs
- Search or retrieval artifacts

### 11. Downstream Handoff

Validated representations may be made available to downstream applications.

Site Sensei may use them to configure assessment or self-review behavior.

DiscoverQuery may use them to support resource discovery, lesson development, or curriculum planning.

Downstream use should preserve traceability to the source document and any teacher-approved changes.

## Processing States

A document may move through states such as:

- Discovered
- Retrieved
- Stored
- Extraction pending
- Extracted
- Interpretation pending
- Interpreted
- Normalized
- Validated
- Failed
- Requires review
- Superseded

The exact state model will be refined during implementation.

## Versioning and Reprocessing

Source versions and processing versions should be tracked separately.

A source document may change while the processing pipeline remains the same.

A document may also be reprocessed without changing the source because:

- Extraction logic improved
- OCR quality improved
- Schemas changed
- Classification rules changed
- Interpretation models changed
- Metadata requirements expanded

Reprocessing should not erase the history of earlier outputs.

## Failure Handling

The pipeline should preserve partial results and record failures clearly.

Failures may include:

- Unsupported format
- Corrupted file
- Empty extraction
- Low-confidence OCR
- Missing provenance
- Invalid normalized output
- Ambiguous document classification
- Storage or network failure

A failed stage should not make the document appear successfully processed.

## Open Design (WIP)

The following decisions remain under development:

- Initial supported file formats
- PDF extraction libraries
- OCR provider and confidence thresholds
- Normalized schema structure
- Chunking strategy
- Teacher review workflow
- Retention rules for uploaded documents
- Search indexing and embeddings
- Processing state implementation
- Versioning format