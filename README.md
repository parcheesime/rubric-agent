# Rubric Agent

> Understanding assessment rubrics through structured research, normalization, and machine-readable representation.

## Overview

Rubric Agent is a research project focused on understanding, classifying, and normalizing assessment rubrics into a structured, machine-readable format.

Rather than treating rubrics as static documents, this project investigates how rubrics are designed, what they measure, and how their intent, structure, and evaluation criteria can be represented consistently across educational and professional domains.

The long-term goal is to develop a reusable knowledge base and normalization pipeline capable of analyzing diverse rubric formats while preserving their original meaning.

---

## Research Goals

This project begins with research before implementation.

The initial objectives are to:

- Build a diverse corpus of publicly available rubrics.
- Study the different purposes and structures of rubrics.
- Identify common patterns across disciplines and industries.
- Develop a consistent JSON representation for machine processing.
- Explore methods for comparing similar rubrics.
- Build a reusable foundation for future assessment and analysis tools.

---

## Guiding Principles

- Preserve the original rubric.
- Normalize rather than rewrite.
- Build the schema from evidence rather than assumptions.
- Separate research from implementation.
- Support multiple domains, not only education.
- Maintain provenance and source information for every collected rubric.

---

## Project Phases

### Phase 1 — Corpus Collection

Collect a diverse set of publicly available rubrics from multiple domains.

Potential sources include:

- Open Educational Resources (OER)
- Universities
- K–12 school districts
- Government agencies
- Professional organizations
- Competition and judging organizations
- Industry evaluation frameworks

Each rubric is stored with its original file, metadata, and source information.

### Phase 2 — Corpus Analysis

Analyze the collected rubrics to better understand:

- Assessment purpose (intent)
- Assessment context
- Rubric structure
- Performance level organization
- Scoring methods
- Evaluation criteria
- Common design patterns

### Phase 3 — Normalization

Develop a machine-readable schema capable of representing a broad variety of rubric structures while preserving their semantic meaning.

### Phase 4 — Comparison

Compare normalized rubrics to identify:

- Similar assessment goals
- Shared evaluation criteria
- Structural similarities
- Missing or uncommon assessment dimensions
- Emerging patterns across disciplines

---

## Repository Structure

```text
docs/           Research notes and documentation
corpus/         Original rubrics, metadata, and normalized data
collectors/     Resource collection utilities
schemas/        JSON schema definitions
scripts/        Collection and analysis scripts
tests/          Test fixtures and validation