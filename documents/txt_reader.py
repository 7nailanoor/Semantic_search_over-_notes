"""
TXT Reader.

Supports multiple encodings.

Author: Naila Noor
Project: Semantic Search over Notes
"""

import logging
from typing import Dict, Any, List

from documents.base_reader import BaseReader

logger = logging.getLogger(__name__)


class TXTReader(BaseReader):
    """
    Reads plain text files.
    """

    ENCODINGS = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin-1",
    ]

    def read(self) -> Dict[str, Any]:

        if not self.exists():
            raise FileNotFoundError(f"{self.file_path} not found.")

        text = None
        used_encoding = None

        for encoding in self.ENCODINGS:
            try:
                with open(
                    self.file_path,
                    "r",
                    encoding=encoding,
                ) as file:
                    text = file.read()

                used_encoding = encoding
                break

            except UnicodeDecodeError:
                continue

        if text is None:
            raise RuntimeError(f"Unable to decode '{self.filename}'.")

        lines = text.splitlines()

        page_texts: List[Dict[str, Any]] = []

        for index, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            page_texts.append(
                {
                    "page": 1,
                    "line": index,
                    "text": line.strip(),
                    "characters": len(line),
                    "words": len(line.split()),
                }
            )

        result = {
            "filename": self.filename,
            "filetype": "txt",
            "pages": 1,
            "text": text,
            "page_texts": page_texts,
            "metadata": {
                "encoding": used_encoding,
                "lines": len(lines),
            },
        }

        logger.info(
            "Successfully loaded TXT: %s",
            self.filename,
        )

        return result
