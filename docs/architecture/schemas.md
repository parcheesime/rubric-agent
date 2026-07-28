# Schema Architecture

**Project:** Rubric Agent  
**Status:** Early Design

---

# Purpose

Rubric Agent transforms educational documents into structured, machine-readable representations that can support educational search, analysis, assessment, curriculum planning, and future AI-assisted applications.

No single schema can effectively represent every aspect of an educational resource. Instead, Rubric Agent separates information into multiple schemas, each with a clearly defined responsibility.

This document describes the role of each schema within the system and the relationships between them.

---

# Design Philosophy

Schemas represent different perspectives of the same educational resource rather than duplicating information.

Each schema answers a different set of questions.

For example:

- What is this document?
- Where did it come from?
- What educational meaning does it contain?
- How is it related to other resources?
- How can downstream applications use it?

Keeping these responsibilities separate allows each schema to evolve independently while remaining connected through shared identifiers and provenance.

---

# The Educational Document Lifecycle

Educational resources move through several stages as they are processed by Rubric Agent.

```text
Educational Document
        │
        ▼
Metadata
        │
        ▼
Text & Structure Extraction
        │
        ▼
Agent Interpretation
        │
        ▼
Normalized Representation
        │
        ▼
Future Knowledge Layers
```

Each stage builds upon the previous one while preserving traceability back to the original document.

---

# Schema Responsibilities

## Metadata Schema

The metadata schema describes the educational resource itself.

Its purpose is to record:

- Identity
- Provenance
- Source information
- Licensing
- Storage
- Processing history
- Versioning
- Integrity

It answers questions such as:

- What is this document?
- Where did it originate?
- When was it collected?
- How was it processed?
- Where is it stored?

The metadata schema does **not** interpret educational meaning.

---

## Normalized Schema

The normalized schema represents Rubric Agent's structured understanding of an educational document.

Rather than describing the document itself, it describes what the agent believes the document communicates.

Examples include:

- learning objectives
- assessment criteria
- instructional expectations
- deliverables
- educational relationships
- machine-readable educational structures

This distinction is intentional.

The normalized representation is an interpretation of the educational content rather than a direct copy of the original document.

Whenever possible, normalized records should preserve references back to the portions of the source document that support the interpretation.

---

# Agent Interpretation

Educational documents often contain ambiguity.

Rubric Agent therefore distinguishes between:

- information explicitly stated by the source document
- information inferred through interpretation
- information confirmed or modified by educators

Future versions of the normalized schema may preserve this distinction directly within interpretation records.

This allows downstream applications to understand both what the source document says and how Rubric Agent interpreted it.

---

# Shared Resource Identity

Although each schema serves a different purpose, they all describe the same educational resource.

Schemas should therefore remain connected through a stable internal resource identifier.

This allows applications to associate:

- metadata
- normalized representations
- future relationships
- processing history
- derived artifacts

without duplicating information across schemas.

---

# Future Schema Expansion

Rubric Agent is expected to grow beyond the initial metadata and normalized schemas.

Future schemas may include:

## Relationship Schema

Represents relationships between educational resources.

Examples:

- prerequisite relationships
- curriculum alignment
- document versions
- related assignments
- related rubrics

---

## Objective Schema

Represents reusable learning objectives independently from individual documents.

This would allow multiple educational resources to reference the same educational concept.

---

## Provenance Schema

Represents detailed provenance and processing history beyond the core metadata record.

---

## Retrieval Schema

Represents future search, indexing, chunking, embeddings, or retrieval artifacts used by downstream AI systems.

---

# Schema Evolution

Rubric Agent is an evolving educational document intelligence system.

New schemas may be introduced as the project expands.

Existing schemas may gain additional fields or capabilities.

The architectural responsibilities described in this document should remain stable even as the implementation evolves.

Whenever possible:

- schemas should have clearly defined responsibilities
- schemas should avoid duplicating information
- schemas should preserve traceability
- schemas should support reproducibility
- schemas should remain extensible for future educational applications

---

# Relationship to the System Architecture

The schema architecture reflects the overall design of Rubric Agent.

The ingestion pipeline transforms educational documents into structured representations.

Those representations become the shared foundation for downstream applications such as Site Sensei, DiscoverQuery, and future educational tools.

By separating identity, interpretation, and future knowledge layers into independent schemas, Rubric Agent can support both reproducible document processing and long-term educational knowledge representation.