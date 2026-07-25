"""
DOCX Reader.

Extracts:
- Full document text
- Paragraph-wise text
- Document metadata

Author: Naila Noor
Project: Semantic Search over Notes
"""

import logging
from typing import Dict, Any, List

from docx import Document

from documents.base_reader import BaseReader

logger = logging.getLogger(__name__)


class DOCXReader(BaseReader):
    """
    Reads Microsoft Word (.docx) documents.
    """

    def read(self) -> Dict[str, Any]:

        if not self.exists():
            raise FileNotFoundError(f"{self.file_path} not found.")

        try:
            document = Document(self.file_path)

            paragraphs: List[Dict[str, Any]] = []
            full_text = []

            for index, para in enumerate(document.paragraphs, start=1):
                text = para.text.strip()

                if not text:
                    continue

                paragraphs.append(
                    {
                        "page": 1,  # DOCX has no fixed pages
                        "paragraph": index,
                        "text": text,
                        "characters": len(text),
                        "words": len(text.split()),
                    }
                )

                full_text.append(text)

            core = document.core_properties

            metadata = {
                "title": core.title or "",
                "author": core.author or "",
                "subject": core.subject or "",
                "keywords": core.keywords or "",
                "category": core.category or "",
                "comments": core.comments or "",
            }

            result = {
                "filename": self.filename,
                "filetype": "docx",
                "pages": 1,
                "text": "\n".join(full_text),
                "page_texts": paragraphs,
                "metadata": metadata,
            }

            logger.info(
                "Successfully loaded DOCX: %s",
                self.filename,
            )

            return result

        except Exception as e:
            logger.exception("Failed reading DOCX.")

            raise RuntimeError(f"Error reading DOCX '{self.filename}': {e}")
