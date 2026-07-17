"""Discover syllabus PDF candidates using Tavily Search."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


DEFAULT_SEARCH_QUERIES = [
    '"course syllabus" filetype:pdf site:.edu',
    '"class syllabus" filetype:pdf site:.edu',
    '"course syllabus" "learning objectives" filetype:pdf',
    '"course syllabus" "grading policy" filetype:pdf',
    '"course syllabus" "course schedule" filetype:pdf',
]


EXCLUDED_TERMS = {
    "syllabus template",
    "syllabus guide",
    "how to write a syllabus",
    "how to create a syllabus",
    "creating a syllabus",
    "designing a syllabus",
    "syllabus development",
    "sample syllabus language",
    "syllabus policy",
    "syllabus requirements",
    "faculty handbook",
    "curriculum handbook",
    "accessibility statement",
    "terms of use",
    "privacy policy",
    "how to"
}


STRONG_SYLLABUS_TERMS = {
    "course syllabus",
    "class syllabus",
}


SYLLABUS_STRUCTURE_TERMS = {
    "course description",
    "learning objectives",
    "learning outcomes",
    "course objectives",
    "required textbook",
    "required materials",
    "grading policy",
    "grading scale",
    "course schedule",
    "weekly schedule",
    "attendance policy",
    "office hours",
    "instructor",
    "assignments",
    "prerequisites",
    "fall",
    "spring",
    "summer",
    "winter",
    "semester",
    "quarter",
    "trimester",
    "session",
    "academic year",
}


@dataclass(frozen=True)
class SyllabusCandidate:
    """A likely syllabus PDF discovered through Tavily."""

    title: str
    document_url: str
    query: str
    snippet: str
    score: float | None


def normalize_text(text: str) -> str:
    """Normalize case and whitespace for consistent matching."""

    return " ".join(text.lower().split())


def get_tavily_client() -> TavilyClient:
    """Create an authenticated Tavily client."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY is missing. Add it to your .env file."
        )

    return TavilyClient(api_key=api_key)


def is_pdf_url(url: str) -> bool:
    """Return True when the URL path ends with .pdf."""

    return urlparse(url).path.lower().endswith(".pdf")


def is_likely_syllabus(title: str, snippet: str) -> bool:
    """Conservatively identify likely course syllabus documents."""

    normalized_title = normalize_text(title)
    normalized_combined = normalize_text(f"{title} {snippet}")

    if any(
        excluded_term in normalized_combined
        for excluded_term in EXCLUDED_TERMS
    ):
        return False

    if any(
        strong_term in normalized_title
        for strong_term in STRONG_SYLLABUS_TERMS
    ):
        return True

    has_syllabus = "syllabus" in normalized_title

    has_structure = any(
        structure_term in normalized_combined
        for structure_term in SYLLABUS_STRUCTURE_TERMS
    )

    return has_syllabus and has_structure


def search_syllabi(
    query: str,
    *,
    max_results: int = 10,
    client: TavilyClient | None = None,
) -> list[SyllabusCandidate]:
    """Search Tavily for likely direct syllabus PDFs."""

    tavily_client = client or get_tavily_client()

    response = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=max_results,
        include_answer=False,
        include_raw_content=False,
    )

    candidates: list[SyllabusCandidate] = []

    for result in response.get("results", []):
        title = str(result.get("title") or "").strip()
        document_url = str(result.get("url") or "").strip()
        snippet = str(result.get("content") or "").strip()

        raw_score = result.get("score")
        score = float(raw_score) if raw_score is not None else None

        if not document_url:
            continue

        if not is_pdf_url(document_url):
            continue

        if not is_likely_syllabus(title, snippet):
            continue

        candidates.append(
            SyllabusCandidate(
                title=title or "Untitled syllabus",
                document_url=document_url,
                query=query,
                snippet=snippet,
                score=score,
            )
        )

    return candidates


def discover_all_syllabi(
    *,
    queries: list[str] | None = None,
    max_results_per_query: int = 5,
) -> list[SyllabusCandidate]:
    """Run configured searches and deduplicate candidates by URL."""

    search_queries = queries or DEFAULT_SEARCH_QUERIES
    client = get_tavily_client()

    all_candidates: list[SyllabusCandidate] = []
    seen_urls: set[str] = set()

    for query in search_queries:
        candidates = search_syllabi(
            query,
            max_results=max_results_per_query,
            client=client,
        )

        for candidate in candidates:
            normalized_url = candidate.document_url.rstrip("/")

            if normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)
            all_candidates.append(candidate)

    return all_candidates