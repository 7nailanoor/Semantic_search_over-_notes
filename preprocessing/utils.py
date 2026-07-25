"""
Preprocessing Utilities

Helper functions used during text preprocessing.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import re
from typing import List


def count_words(text: str) -> int:
    """
    Count the number of words in a text.

    Parameters
    ----------
    text : str

    Returns
    -------
    int
    """

    if not text:
        return 0

    return len(text.split())


def count_characters(text: str) -> int:
    """
    Count the number of characters.

    Parameters
    ----------
    text : str

    Returns
    -------
    int
    """

    return len(text)


def split_into_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs.

    Empty paragraphs are removed.
    """

    if not text:
        return []

    paragraphs = re.split(r"\n\s*\n", text)

    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.
    """

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def remove_empty_lines(text: str) -> str:
    """
    Remove blank lines from text.
    """

    if not text:
        return ""

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return "\n".join(lines)


def estimate_reading_time(
    text: str,
    words_per_minute: int = 200,
) -> float:
    """
    Estimate reading time in minutes.

    Parameters
    ----------
    text : str

    words_per_minute : int

    Returns
    -------
    float
    """

    words = count_words(text)

    if words == 0:
        return 0.0

    return round(words / words_per_minute, 2)


def truncate_text(
    text: str,
    max_length: int = 200,
) -> str:
    """
    Truncate long text for previews.

    Parameters
    ----------
    text : str

    max_length : int

    Returns
    -------
    str
    """

    if len(text) <= max_length:
        return text

    return text[:max_length].rstrip() + "..."


def unique_words(text: str) -> List[str]:
    """
    Return sorted unique words.

    Parameters
    ----------
    text : str

    Returns
    -------
    List[str]
    """

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )

    return sorted(set(words))
