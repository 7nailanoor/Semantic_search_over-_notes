"""
Metadata Store

Stores and manages metadata for document chunks indexed in FAISS.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class MetadataStore:
    """
    Stores metadata corresponding to FAISS vectors.
    """

    def __init__(
        self,
        metadata_path: str = "data/metadata.json",
    ):

        self.metadata_path = Path(metadata_path)

        self.metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.metadata: List[Dict[str, Any]] = []

    # ---------------------------------------------------------

    def add(
        self,
        items: List[Dict[str, Any]],
    ) -> None:
        """
        Add metadata entries.

        Parameters
        ----------
        items : List[dict]
        """

        self.metadata.extend(items)

    # ---------------------------------------------------------

    def get(
        self,
        index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Get metadata by FAISS index.

        Parameters
        ----------
        index : int

        Returns
        -------
        dict | None
        """

        if 0 <= index < len(self.metadata):
            return self.metadata[index]

        return None

    # ---------------------------------------------------------

    def save(self) -> None:
        """
        Save metadata to disk.
        """

        with open(
            self.metadata_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.metadata,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # ---------------------------------------------------------

    def load(self) -> None:
        """
        Load metadata from disk.
        """

        if not self.metadata_path.exists():
            self.metadata = []

            return

        with open(
            self.metadata_path,
            "r",
            encoding="utf-8",
        ) as file:
            self.metadata = json.load(file)

    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all metadata.
        """

        self.metadata = []

        if self.metadata_path.exists():
            self.metadata_path.unlink()

    # ---------------------------------------------------------

    def total_chunks(self) -> int:
        """
        Return total stored metadata entries.
        """

        return len(self.metadata)

    # ---------------------------------------------------------

    def get_document_chunks(
        self,
        document_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Return all chunks belonging to a document.
        """

        return [item for item in self.metadata if item["document_id"] == document_id]

    # ---------------------------------------------------------

    def list_documents(self) -> List[str]:
        """
        Return unique document filenames.
        """

        return sorted({item["filename"] for item in self.metadata})
