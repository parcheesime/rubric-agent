# Educational Resource Record Architecture

## Status

**Status:** Draft  
**Version:** 0.1  
**Scope:** Canonical educational-resource records  
**Applies to:** All supported source providers

---

# 1. Purpose

Rubric Agent represents educational resources using a three-level conceptual
architecture.

The purpose of this architecture is to keep three different kinds of information
separate:

1. what a resource is
2. how that resource relates to other educational objects
3. what is contained inside the resource

These levels are designed to work across different providers and source formats.

A provider may expose lessons, units, files, assessments, standards, and
instructional metadata in very different ways. Source-specific collectors and
adapters map those structures into the Rubric Agent canonical architecture.

The architecture is source-independent.

---

# 2. The Three-Level Model

```text
EDUCATIONAL RESOURCE RECORD
│
├── Level 1: Resource Identity
│   └── What is this resource?
│
├── Level 2: Resource Relationships
│   └── How does this resource relate to other educational objects?
│
└── Level 3: Resource Content and Interpretation
    └── What is inside this resource?