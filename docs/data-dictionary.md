# Rubric Agent Data Dictionary

## Purpose

The Rubric Agent data dictionary defines the canonical vocabulary used to
represent educational resources across different source providers.

Source systems may use different names, structures, identifiers, and taxonomies.
Collectors and adapters map those source-specific values into the Rubric Agent
canonical model.

This document defines the meaning of canonical fields. It should remain aligned
with the project's schemas, models, tests, and golden records.

---

## Core Principles

1. Source data does not define the canonical model.
2. Preserve provenance and source-native identifiers.
3. Prefer controlled vocabularies for categorical values.
4. Keep source-provided data separate from derived or AI-generated data.
5. Do not introduce new canonical fields without updating this dictionary.
6. Grow the model from observed source data rather than assumptions.

---

## Record Categories

The canonical model is organized into these broad categories:

- Identity
- Provenance
- Educational classification
- Instructional metadata
- Assets
- Relationships
- Access and licensing
- Derived and extracted data
- Data quality and validation

These categories may later become separate supporting dictionaries.

---

# Identity

| Field | Type | Requirement | Description |
|---|---|---|---|
| `resource_id` | string | required | Stable Rubric Agent identifier. |
| `resource_type` | string | required | Canonical resource classification. |
| `title` | string | required | Human-readable resource title. |
| `description` | string/null | recommended | Description supplied by the source. |
| `language` | string/null | recommended | Primary language of the resource. |
| `record_version` | string | required | Version of the canonical record format. |

Initial `resource_type` values may include:

```text
lesson
unit
course
worksheet
slide-deck
quiz
assessment
answer-key
teacher-guide
student-guide
video
activity
assignment
rubric
syllabus
other