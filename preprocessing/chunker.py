"""
Advanced Text Chunker

Creates meaningful chunks for semantic search.

Features
--------
- Section-aware chunking
- Heading preservation
- Word-based chunk size
- Overlapping chunks
- Metadata preservation

"""

from __future__ import annotations

from typing import Any, Dict, List
import re


class TextChunker:
    """
    Splits documents into optimized chunks
    for embedding and vector search.
    """

    def __init__(
        self,
        chunk_size: int = 150,
        overlap: int = 30,
    ):

        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk size.")

        self.chunk_size = chunk_size
        self.overlap = overlap

    # --------------------------------------------------
    # Section splitting
    # --------------------------------------------------

    def split_sections(self, text: str) -> List[str]:
        """
        Split document into logical sections.

        Detects headings like:

        1. Introduction
        2. Tools Used
        3. Conclusion
        """

        sections = re.split(r"\n(?=\d+\.\s)", text)

        return [section.strip() for section in sections if section.strip()]

    # --------------------------------------------------
    # Create chunks
    # --------------------------------------------------

    def create_chunks(self, text: str) -> List[str]:
        """
        Create overlapping text chunks.
        """

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):
            end = start + self.chunk_size

            chunk_words = words[start:end]

            if chunk_words:
                chunks.append(" ".join(chunk_words))

            start += self.chunk_size - self.overlap

        return chunks

    # --------------------------------------------------
    # Main function
    # --------------------------------------------------

    def chunk_document(
        self,
        document: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Convert loaded document into chunks.

        Parameters
        ----------
        document:
            Output from DocumentLoader


        Returns
        -------
        List of chunk dictionaries
        """

        chunks = []

        chunk_id = 1

        text = document.get("text", "")

        if not text.strip():
            return []

        sections = self.split_sections(text)

        for section in sections:
            section_chunks = self.create_chunks(section)

            for chunk_text in section_chunks:
                chunks.append(
                    {
                        "document_id": document["document_id"],
                        "filename": document["filename"],
                        "filetype": document["filetype"],
                        "page": self.get_page(section),
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                        "word_count": len(chunk_text.split()),
                        "section": self.extract_heading(section),
                    }
                )

                chunk_id += 1

        return chunks

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def extract_heading(section: str) -> str:
        """
        Extract section title.

        Example:

        "7. Conclusion:
        This project..."

        returns:

        "7. Conclusion"
        """

        first_line = section.split("\n")[0]

        if len(first_line) < 100:
            return first_line.strip()

        return "General"

    @staticmethod
    def get_page(section: str) -> int:
        """
        Placeholder page handling.

        PDF readers can later provide
        real page numbers.
        """

        return 1
