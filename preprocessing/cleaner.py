"""
Text Cleaner

Cleans extracted document text before chunking
and embedding generation.

Features
--------
- Remove extra spaces
- Remove blank lines
- Normalize Unicode characters
- Remove control characters
- Normalize line endings

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import re
import unicodedata


class TextCleaner:
    """
    Utility class for cleaning extracted text.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean extracted text.

        Parameters
        ----------
        text : str

        Returns
        -------
        str
            Cleaned text.
        """

        if not text:
            return ""

        # Normalize unicode characters
        text = unicodedata.normalize("NFKC", text)

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove invisible/control characters
        text = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]",
            "",
            text,
        )

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove spaces around new lines
        text = re.sub(r" *\n *", "\n", text)

        # Collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @staticmethod
    def clean_document(document: dict) -> dict:
        """
        Clean an entire loaded document.

        Parameters
        ----------
        document : dict

        Returns
        -------
        dict
        """

        document["text"] = TextCleaner.clean(document["text"])

        for section in document.get("page_texts", []):
            section["text"] = TextCleaner.clean(section["text"])

        return document
