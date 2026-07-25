"""
PDF Reader using PyMuPDF.

Extracts:
- Full document text
- Page-wise text
- PDF metadata

Author: Naila Noor
Project: Semantic Search over Notes
"""

import logging
from typing import Dict, Any, List

import fitz

from documents.base_reader import BaseReader


logger = logging.getLogger(__name__)


class PDFReader(BaseReader):
    """
    Reads PDF documents using PyMuPDF.
    """

    def read(self) -> Dict[str, Any]:

        if not self.exists():
            raise FileNotFoundError(f"{self.file_path} not found.")

        try:
            pdf = fitz.open(self.file_path)

            page_texts: List[Dict[str, Any]] = []

            full_text = []

            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                if not text:
                    text = ""

                page_texts.append(
                    {
                        "page": page_number,
                        "text": text,
                        "characters": len(text),
                        "words": len(text.split()),
                    }
                )

                full_text.append(text)

            metadata = pdf.metadata or {}

            result = {
                "filename": self.filename,
                "filetype": "pdf",
                "pages": len(pdf),
                "text": "\n".join(full_text),
                "page_texts": page_texts,
                "metadata": {
                    "title": metadata.get("title", ""),
                    "author": metadata.get("author", ""),
                    "creator": metadata.get("creator", ""),
                    "producer": metadata.get("producer", ""),
                    "subject": metadata.get("subject", ""),
                    "keywords": metadata.get("keywords", ""),
                },
            }

            pdf.close()

            logger.info(
                "Successfully loaded PDF: %s (%d pages)",
                self.filename,
                result["pages"],
            )

            return result

        except Exception as e:
            logger.exception("Failed reading PDF.")

            raise RuntimeError(f"Error reading PDF '{self.filename}': {e}")
