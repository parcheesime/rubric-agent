"""educational_terms.py

A centralized glossary of universal K-12 educational, instructional,
and curriculum engineering terms.
"""

CURRICULUM_TERMS = (
    "objective",
    "outcome",
    "learning_target",
    "success_criteria",
    "curriculum",
    "standard",
    "strand",
    "sub_strand",
    "benchmark",
    "indicator",
    "competency",
    "rationale",
)

CONTENT_TERMS = (
    "topic",
    "concept",
    "skill",
    "big_idea",
    "essential_question",
    "vocabulary",
    "knowledge",
    "misconception",
    "theme",
    "fact",
    "phenomenon",
)

SEQUENCE_TERMS = (
    "unit",
    "sequence",
    "scope",
    "programme",
    "order",
    "position",
    "prerequisite",
    "prior_knowledge",
    "previous_lesson",
    "next_lesson",
    "module",
    "pacing",
    "duration",
    "term",
)

ASSESSMENT_TERMS = (
    "quiz",
    "assessment",
    "exit_ticket",
    "rubric",
    "mark_scheme",
    "question_set",
    "formative",
    "summative",
    "diagnostic",
    "criteria",
)

RESOURCE_TERMS = (
    "worksheet",
    "slide",
    "video",
    "resource",
    "teacher_guide",
    "answer_key",
    "exemplar",
    "worked_example",
    "anchor_chart",
    "task_card",
    "graphic_organizer",
    "reading_passage",
    "handout",
    "template",
    "stimulus",
)

INSTRUCTION_TERMS = (
    "prompt",
    "hook",
    "warm_up",
    "starter",
    "guided_practice",
    "independent_practice",
    "wrap_up",
    "extension",
    "activity",
    "practice",
    "modality",
    "direct_instruction",
    "modeling",
    "grouping",
    "closure",
    "check_for_understanding",
    "turn_and_talk",
)

SUPPORT_TERMS = (
    "differentiation",
    "scaffold",
    "modification",
    "accommodation",
    "intervention",
    "manipulative",
    "support",
    "reteach",
    "enrichment",
    "language_objective",
    "sentence_frame",
    "word_bank",
    "acceleration",
)

EDTECH_PLATFORM_TERMS = (
    "pear_deck",
    "mentimeter",
    "kahoot",
    "canva",
    "canvas_lms",
    "youtube",
    "smart_board",
    "quizlet",
    "quizizz",
    "lumio",
    "nearpod",
    "edpuzzle",
    "google_classroom",
    "schoology",
    "moodle",
    "seesaw",
    "padlet",
    "flip",
    "desmos",
    "geogebra",
    "formative",
    "classkick",
    "blooket",
    "socrative",
)

EDTECH_TYPE_TERMS = (
    "interactive_lesson",
    "digital_activity",
    "learning_management_system",
    "lms",
    "student_response_system",
    "virtual_whiteboard",
    "digital_whiteboard",
    "presentation_tool",
    "quiz_platform",
    "video_lesson",
    "interactive_video",
    "adaptive_learning",
    "gamified_learning",
    "simulation",
    "virtual_lab",
)

EDTECH_TERMS = (
    *EDTECH_PLATFORM_TERMS,
    *EDTECH_TYPE_TERMS,
)

# Global Registry for full verification loops
ALL_CATEGORIES = {
    "curriculum": CURRICULUM_TERMS,
    "content": CONTENT_TERMS,
    "sequence": SEQUENCE_TERMS,
    "assessment": ASSESSMENT_TERMS,
    "resource": RESOURCE_TERMS,
    "instruction": INSTRUCTION_TERMS,
    "support": SUPPORT_TERMS,
    "edtech": EDTECH_TERMS,
}

ALL_TERMS = tuple(
    term
    for terms in ALL_CATEGORIES.values()
    for term in terms
)
