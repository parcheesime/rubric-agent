"""Discover rubric PDF links from approved Exemplars index pages."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": (
        "rubric-agent/0.1 "
        "(educational resource research; contact: YOUR_EMAIL)"
    )
}

RUBRIC_INDEX_PAGES = {
    "assessment": "https://exemplars.com/resources/assessment/rubrics",
    "math": "https://exemplars.com/resources/math/rubrics",
    "science": "https://exemplars.com/resources/science/rubrics",
    "writing": "https://exemplars.com/resources/writing/rubrics",
}

EXCLUDED_TITLE_TERMS = {
    "terms of use",
    "privacy policy",
    "state standards",
    "standards for mathematical practice",
    "spanish",
}

SUPPORTED_LANGUAGES = {"english"}

SPANISH_MARKERS = {
    "spanish",
    "español",
}

@dataclass(frozen=True)
class RubricCandidate:
    """A direct rubric document discovered on an Exemplars page."""

    title: str
    document_url: str
    source_url: str
    subject: str
    file_type: str


def is_pdf_url(url: str) -> bool:
    """Return True when the URL path ends with .pdf."""

    return urlparse(url).path.lower().endswith(".pdf")


def is_likely_rubric(title: str) -> bool:
    """Reject clearly non-rubric documents found on an index page."""

    normalized_title = title.strip().lower()

    if not normalized_title:
        return False

    return not any(
        excluded_term in normalized_title
        for excluded_term in EXCLUDED_TITLE_TERMS
    )

def is_supported_language(title: str) -> bool:
    normalized = title.lower()
    return not any(marker in normalized for marker in SPANISH_MARKERS)

def discover_rubrics(
    source_url: str,
    *,
    subject: str,
    timeout: int = 30,
    session: requests.Session | None = None,
) -> list[RubricCandidate]:
    """Extract unique rubric PDF candidates from one index page."""

    client = session or requests.Session()

    response = client.get(
        source_url,
        headers=DEFAULT_HEADERS,
        timeout=timeout,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    candidates: list[RubricCandidate] = []
    seen_urls: set[str] = set()

    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        title = link.get_text(" ", strip=True)
        document_url = urljoin(source_url, href)

        if not is_pdf_url(document_url):
            continue

        if not is_likely_rubric(title):
            continue

        if document_url in seen_urls:
            continue

        if not is_supported_language(title):
            continue

        seen_urls.add(document_url)

        candidates.append(
            RubricCandidate(
                title=title,
                document_url=document_url,
                source_url=source_url,
                subject=subject,
                file_type=".pdf",
            )
        )

    return candidates


def discover_all_rubrics() -> list[RubricCandidate]:
    """Discover rubric candidates from every configured index page."""

    all_candidates: list[RubricCandidate] = []

    with requests.Session() as session:
        for subject, source_url in RUBRIC_INDEX_PAGES.items():
            candidates = discover_rubrics(
                source_url,
                subject=subject,
                session=session,
            )
            all_candidates.extend(candidates)

    return all_candidates