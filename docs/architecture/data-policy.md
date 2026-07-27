# Data Policy

**Project:** Rubric Agent
**Status:** Draft
**Applies to:** All collected resources, uploaded educational materials, derived representations, and contributors.

---

# Purpose

Rubric Agent is an open-source educational document intelligence project that transforms educational materials into structured, machine-readable representations while preserving their provenance, licensing context, and instructional meaning.

Unlike a traditional document repository or web scraper, Rubric Agent is designed as reusable infrastructure for understanding educational documents. The project combines document collection, ingestion, normalization, interpretation, and structured metadata generation into a shared platform that supports educational applications such as assessment, curriculum planning, search, and future AI-assisted learning tools.

The project serves two complementary purposes:

1. Maintain a continually improving reference corpus of educational materials from public sources.
2. Interpret teacher-provided educational documents into human-readable and machine-readable representations that can power downstream educational applications while remaining under teacher control.

This policy defines how educational materials are collected, processed, stored, attributed, and used throughout that lifecycle.

---

# Guiding Principles

## Educational Infrastructure

Rubric Agent exists to build reusable infrastructure for educational document understanding rather than simply collecting documents.

Educational materials are transformed into structured representations that can support multiple educational applications without requiring each application to independently solve document ingestion and interpretation.

---

## Scale with Traceability

Rubric Agent is designed to grow a diverse educational corpus over time.

Growth must never come at the expense of provenance.

Every processed resource should remain traceable to its original source, retrieval context, licensing information whenever available, processing history, and derived representations.

---

## Preserve Before Transforming

Whenever practical, the original document is preserved before any extraction or normalization occurs.

Every derived artifact should remain reproducible from its original source document.

---

## Metadata is First-Class Data

Metadata is not considered secondary information.

Source identifiers, retrieval timestamps, licensing information, checksums, processing versions, institutions, document classifications, and provenance records are essential components of every educational resource.

---

## Teacher Control

Rubric Agent assists educators by interpreting documents—not by replacing instructional judgment.

Teacher-provided materials establish instructional intent.

Machine-readable representations, generated summaries, and downstream application behavior should remain reviewable and correctable by educators.

---

## Separation of Content and Software

Rubric Agent software is licensed under Apache License 2.0.

Educational materials processed by the project remain subject to their original licensing terms.

Processing a document does not transfer ownership, alter copyright, or replace the original license.

---

# Data Categories

Rubric Agent manages several distinct categories of information.

These categories are governed differently throughout the ingestion pipeline.

## Public Reference Corpus

Educational resources collected from publicly accessible repositories, institutional archives, and openly available educational collections.

Examples include:

* Rubrics
* Syllabi
* Lesson plans
* Assignments
* Worksheets
* Course materials
* Assessments
* Public educational resources

These materials provide examples that improve document understanding, normalization, and educational analysis.

---

## Teacher Workspace Documents

Documents intentionally uploaded by educators for interpretation or use within downstream applications.

Examples include:

* Classroom rubrics
* Course syllabi
* Assignment descriptions
* Custom assessments
* Project requirements

Teacher workspace materials are distinct from the public reference corpus and should not become shared corpus resources without explicit authorization from the contributor and appropriate rights to do so.

---

## Derived Representations

Rubric Agent produces information derived from educational documents, including:

* Extracted text
* Structural document models
* Machine-readable educational records
* Human-readable document summaries
* Educational objectives
* Assessment criteria
* Metadata
* Tags
* Relationships
* Processing logs

Derived representations remain linked to the source document through persistent provenance records.

---

# Educational Document Lifecycle

Educational documents generally move through the following stages:

Discovery or upload

↓

Original document preservation

↓

Metadata extraction

↓

Text and structural extraction

↓

Document classification

↓

Educational interpretation

↓

Human-readable review

↓

Machine-readable representation

↓

Teacher review (where applicable)

↓

Use by downstream educational applications

Each stage should preserve traceability to previous stages.

---

# Collection Philosophy

Rubric Agent periodically discovers educational materials from public educational sources to improve the diversity and coverage of its reference corpus.

Collectors are responsible for discovering and retrieving resources.

The shared ingestion pipeline is responsible for extracting content, generating metadata, identifying educational structure, and producing normalized representations.

Collectors should prioritize:

* Official institutional repositories
* Open educational resources
* Public educational archives
* Stable, attributable sources

Collectors should preserve available provenance information rather than attempting to infer missing information.

---

# Provenance Requirements

Every collected resource should preserve as much provenance as reasonably available.

Typical provenance includes:

* Original source URL
* Retrieval timestamp
* Institution or publisher
* Repository identifier
* Original filename
* Document checksum
* Collector identifier
* Processing version
* License information when available

Provenance records should remain associated with all derived artifacts.

---

# Copyright and Licensing

Rubric Agent respects the intellectual property rights of educational content creators.

Whenever available, licensing information should be preserved exactly as provided by the original source.

If licensing information is unavailable, the project should record that the license is unknown rather than attempting to infer one.

Ingestion into Rubric Agent does not imply permission for redistribution.

Original licensing terms remain attached to source materials.

---

# Storage Architecture

Rubric Agent intentionally separates different forms of educational information.

Typical storage includes:

* Original documents
* Extracted text
* Metadata
* Normalized representations
* Processing artifacts
* Future derived datasets

Separating these layers improves reproducibility, auditing, and future reprocessing.

---

# Downstream Applications

Applications such as Site Sensei and DiscoverQuery consume structured educational representations rather than directly interpreting source documents independently.

Rubric Agent serves as the shared document understanding layer that enables downstream educational applications while maintaining traceability back to source materials.

Whenever practical, downstream decisions should remain explainable through the educational records generated during document interpretation.

---

# Project Maturity

Rubric Agent is currently under active architectural development.

At this stage, the project's primary focus is establishing a robust foundation for educational document collection, ingestion, interpretation, and normalization. As the architecture evolves, project policies, contribution guidelines, schemas, and development workflows will continue to mature.

Until formal contributor guidelines are published, development is primarily focused on:

* Designing a reusable educational document ingestion pipeline.
* Building a provenance-first reference corpus.
* Developing reliable document interpretation and normalization capabilities.
* Establishing stable schemas for machine-readable educational representations.
* Defining policies that prioritize traceability, reproducibility, and educator control.

Future releases will introduce additional documentation covering contributor expectations, collector development standards, code review processes, dataset governance, and quality assurance.

This Data Policy establishes the principles that will guide those future contributions as the project grows.

---

# Living Policy

Rubric Agent is an evolving educational infrastructure project.

As the ingestion pipeline, corpus architecture, and educational applications mature, this policy will evolve to reflect new capabilities while maintaining its core principles of provenance, transparency, reproducibility, and educator control.
