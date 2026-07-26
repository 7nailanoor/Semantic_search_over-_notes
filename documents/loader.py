"""
Document Loader

Loads supported document types and returns a standardized
document object enriched with metadata.

Supported Formats:
- PDF
- DOCX
- TXT
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from documents.pdf_reader import PDFReader
from documents.docx_reader import DOCXReader
from documents.txt_reader import TXTReader


class DocumentLoader:
    """
    Loads documents using the appropriate reader.

    Returns a standardized dictionary that the rest of the
    project (preprocessing, chunking, embeddings, FAISS)
    can consume.
    """

    SUPPORTED_TYPES = {
        ".pdf": PDFReader,
        ".docx": DOCXReader,
        ".txt": TXTReader,
    }

    def __init__(self, file_path: str | Path):

        self.file_path = Path(file_path)

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def load(self) -> Dict[str, Any]:
        """
        Load a document.

        Returns
        -------
        dict
            Standardized document dictionary.
        """

        self._validate()

        reader_class = self.SUPPORTED_TYPES[self.file_path.suffix.lower()]

        reader = reader_class(self.file_path)

        document = reader.read()

        document.update(
            {
                "document_id": self._generate_document_id(),
                "file_path": str(self.file_path.resolve()),
                "extension": self.file_path.suffix.lower(),
                "file_size": self.file_path.stat().st_size,
                "file_hash": self._calculate_hash(),
                "uploaded_at": datetime.now().isoformat(timespec="seconds"),
            }
        )

        return document

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate(self) -> None:

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if not self.file_path.is_file():
            raise ValueError(f"{self.file_path} is not a file.")

        extension = self.file_path.suffix.lower()

        if extension not in self.SUPPORTED_TYPES:
            supported = ", ".join(self.SUPPORTED_TYPES.keys())

            raise ValueError(
                f"Unsupported file type '{extension}'. Supported: {supported}"
            )

        if self.file_path.stat().st_size == 0:
            raise ValueError("Uploaded file is empty.")

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def _calculate_hash(self) -> str:
        """
        Calculate SHA-256 hash.

        Used for duplicate detection.
        """

        sha256 = hashlib.sha256()

        with open(self.file_path, "rb") as file:
            while True:
                chunk = file.read(8192)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    @staticmethod
    def _generate_document_id() -> str:
        """
        Generate a unique document ID.
        """

        return str(uuid.uuid4())
