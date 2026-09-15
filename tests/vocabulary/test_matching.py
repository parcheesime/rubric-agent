"""Focused tests for metadata key normalization and exact matching."""

import pytest

from rubric_agent.vocabulary.matching import match_metadata_key, normalize_metadata_key


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("priorKnowledge", "prior_knowledge"),
        ("pupilLessonOutcome", "pupil_lesson_outcome"),
        ("lessonPlan", "lesson_plan"),
        ("lesson plan", "lesson_plan"),
        ("lesson-plan", "lesson_plan"),
        ("  lesson__ \t--plan  ", "lesson_plan"),
        ("prior_knowledge", "prior_knowledge"),
        ("LESSON_PLAN", "lesson_plan"),
        ("XMLDocument", "xml_document"),
        ("misconception", "misconception"),
        ("", ""),
    ],
)
def test_normalize_metadata_key(name, expected):
    assert normalize_metadata_key(name) == expected
    assert normalize_metadata_key(expected) == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("priorKnowledge", [("sequence", "prior_knowledge")]),
        ("lessonPlan", [("resource", "lesson_plan")]),
        ("lesson plan", [("resource", "lesson_plan")]),
        ("lesson-plan", [("resource", "lesson_plan")]),
        ("misconception", [("content", "misconception")]),
        ("concept", [("content", "concept")]),
    ],
)
def test_match_metadata_key(name, expected):
    assert match_metadata_key(name) == expected


@pytest.mark.parametrize(
    "name",
    ["misconceptions", "misconceptionsAndCommonMistakes", "pupilLessonOutcome", ""],
)
def test_substrings_and_noncanonical_terms_do_not_match(name):
    assert match_metadata_key(name) == []
