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
    "learning_intention",
    "success_criterion",
    "expectation",
    "framework",
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
    "key_idea",
    "key_concept",
    "key_vocabulary",
    "disciplinary_knowledge",
    "procedural_knowledge",
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
    # Lesson and planning materials
    "lesson",
    "lesson_plan",
    "unit_plan",
    "syllabus",
    "outline",
    "teacher_guide",
    "teacher_manual",
    "teacher_notes",
    "student_guide",

    # Worksheets, practice, and assessment support
    "worksheet",
    "practice_set",
    "problem_set",
    "question_bank",
    "independent_work_packet",
    "answer_key",
    "worked_example",
    "exemplar",

    # Reference and reading materials
    "textbook",
    "student_book",
    "workbook",
    "reading",
    "reading_passage",
    "article",
    "book",
    "ebook",
    "reference_sheet",
    "formula_sheet",
    "handout",

    # Visual and classroom materials
    "slide",
    "anchor_chart",
    "graphic_organizer",
    "task_card",
    "flash_card",
    "poster",
    "bulletin_board",
    "word_wall",
    "clip_art",
    "template",
    "stimulus",

    # Activities and projects
    "activity",
    "game",
    "center",
    "project",
    "laboratory",
    "lab",
    "simulation",
    "interactive",

    # Media and digital resources
    "video",
    "audio",
    "podcast",
    "song",
    "notebook",
    "printable",

    # General
    "resource",
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
    "classroom_management",
    "mini_lesson",
    "discussion",
    "collaboration",
    "pair_work",
    "group_work",
    "whole_group",
    "small_group",
    "independent_work",
    "think_pair_share",
    "inquiry",
    "investigation",
    "exploration",
    "demonstration",
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
    "accessibility",
    "assistive_technology",
    "ell",
    "esl",
    "multilingual_learner",
    "special_education",
    "gifted",
    "advanced_learner",
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

    # Additional platforms / sources
    "google_workspace",
    "google_sites",
    "clever",
    "wikipedia",
    "coolmath_games",
    "zoom",
    "abcya",
    "prodigy",
    "google_meet",
    "khan_academy",
    "epic",
    "jamboard",
    "mit_app_inventor",
    "weebly",
    "gimkit",
    "scholastic",
    "brainpop",
    "code_org",
    "grammarly",
    "classlink",
    "ixl",
    "phet",
    "math_playground",
)

EDTECH_AI_TERMS = (
    "artificial_intelligence",
    "ai",
    "generative_ai",
    "ai_tutor",
    "ai_assistant",
    "chatbot",
    "adaptive_learning",
)

EDTECH_DIGITAL_FORMAT_TERMS = (
    "slide",
    "slides",
    "spreadsheet",
    "google_doc",
    "document",
    "notebook",
    "digital_notebook",
    "presentation",
    "interactive_presentation",
    "digital_worksheet",
    "digital_form",
)

EDTECH_DEVICE_TERMS = (
    "laptop",
    "chromebook",
    "ipad",
    "tablet",
    "smart_board",
    "interactive_whiteboard",
    "calculator",
    "graphing_calculator",
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
    *EDTECH_DEVICE_TERMS,
    *EDTECH_DIGITAL_FORMAT_TERMS,
    *EDTECH_AI_TERMS,
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
