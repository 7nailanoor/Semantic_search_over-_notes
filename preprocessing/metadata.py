"""
Metadata Generator

Creates metadata for document chunks to improve
search results and UI display.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

from typing import Dict, Any, List


class MetadataGenerator:
    """
    Generates metadata for document chunks.
    """

    @staticmethod
    def enrich_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add useful metadata to every chunk.

        Parameters
        ----------
        chunks : List[dict]

        Returns
        -------
        List[dict]
        """

        total_chunks = len(chunks)

        for chunk in chunks:
            text = chunk.get("text", "")

            chunk["metadata"] = {
                "document_id": chunk.get("document_id"),
                "filename": chunk.get("filename"),
                "filetype": chunk.get("filetype"),
                "page": chunk.get("page"),
                "chunk_id": chunk.get("chunk_id"),
                "word_count": len(text.split()),
                "character_count": len(text),
                "chunk_position": (f"{chunk.get('chunk_id')}/{total_chunks}"),
            }

        return chunks

    @staticmethod
    def document_summary(
        document: Dict[str, Any], chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate summary statistics for a document.

        Parameters
        ----------
        document : dict

        chunks : List[dict]

        Returns
        -------
        dict
        """

        total_words = sum(chunk["metadata"]["word_count"] for chunk in chunks)

        total_characters = sum(chunk["metadata"]["character_count"] for chunk in chunks)

        return {
            "document_id": document.get("document_id"),
            "filename": document.get("filename"),
            "filetype": document.get("filetype"),
            "pages": document.get("pages"),
            "total_chunks": len(chunks),
            "total_words": total_words,
            "total_characters": total_characters,
        }
