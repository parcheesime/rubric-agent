# Rubric Agent

## Mission

Develop a machine-readable understanding of assessment rubrics while preserving their original intent and meaning.

## Objectives

The Rubric Agent should be able to:

- Collect diverse rubric examples.
- Determine assessment intent.
- Determine assessment context.
- Recognize rubric structure.
- Extract grading criteria.
- Identify performance levels.
- Normalize rubrics into a consistent JSON representation.
- Compare related rubrics.
- Preserve provenance and source information.

## Guiding Principles

- Preserve the author's intent.
- Preserve the original document.
- Build from evidence, not assumptions.
- Remain domain independent.
- Separate collection, analysis, and normalization.
- Produce consistent machine-readable representations.

## Analysis Pipeline

1. Collect
2. Determine assessment intent
3. Determine assessment context
4. Analyze rubric structure
5. Extract grading criteria
6. Extract performance levels
7. Normalize
8. Validate
9. Compare

## Current Focus

Build a diverse research corpus of rubrics before developing parsing and normalization algorithms.

The corpus should drive the design of the normalization schema rather than the schema dictating how rubrics are interpreted.
