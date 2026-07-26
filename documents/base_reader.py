"""
Base class for all document readers.

Every reader (PDF, DOCX, TXT) inherits from this class so they all
return data in the exact same format.

"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseReader(ABC):
    """
    Abstract base class for document readers.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    @property
    def filename(self) -> str:
        """Return filename only."""
        return self.file_path.name

    @property
    def extension(self) -> str:
        """Return lowercase file extension."""
        return self.file_path.suffix.lower()

    def exists(self) -> bool:
        """Check whether file exists."""
        return self.file_path.exists()

    @abstractmethod
    def read(self) -> Dict[str, Any]:
        """
        Reads the document and returns a standardized dictionary.

        Returns
        -------
        dict

        {
            filename,
            filetype,
            pages,
            text,
            page_texts,
            metadata
        }
        """
        pass
