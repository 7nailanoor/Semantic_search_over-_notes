"""
File Handler

Handles saving, deleting and listing uploaded files.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from pathlib import Path
import shutil
from typing import List

from utils.constants import SUPPORTED_FILE_TYPES, UPLOAD_DIR


class FileHandler:
    """
    Utility class for file operations.
    """

    def __init__(self):

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------

    def save_uploaded_file(
        self,
        uploaded_file,
    ) -> Path:
        """
        Save a Streamlit uploaded file.

        Parameters
        ----------
        uploaded_file

        Returns
        -------
        Path
        """

        extension = Path(uploaded_file.name).suffix.lower()

        if extension not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {extension}")

        destination = UPLOAD_DIR / uploaded_file.name

        with open(destination, "wb") as file:
            file.write(uploaded_file.getbuffer())

        return destination

    # -----------------------------------------------------

    def delete_file(self, filename: str) -> bool:
        """
        Delete a file.

        Returns
        -------
        bool
        """

        path = UPLOAD_DIR / filename

        if path.exists():
            path.unlink()

            return True

        return False

    # -----------------------------------------------------

    def clear_upload_folder(self):
        """
        Delete all uploaded files.
        """

        for file in UPLOAD_DIR.iterdir():
            if file.is_file():
                file.unlink()

    # -----------------------------------------------------

    def list_uploaded_files(
        self,
    ) -> List[str]:
        """
        Return all uploaded filenames.
        """

        return sorted(file.name for file in UPLOAD_DIR.iterdir() if file.is_file())

    # -----------------------------------------------------

    def file_exists(self, filename: str) -> bool:
        """
        Check whether a file exists.
        """

        return (UPLOAD_DIR / filename).exists()

    # -----------------------------------------------------

    def get_file_path(self, filename: str) -> Path:
        """
        Return the absolute file path.
        """

        return UPLOAD_DIR / filename

    # -----------------------------------------------------

    def copy_file(self, source: str, destination: str):
        """
        Copy a file.
        """

        shutil.copy2(source, destination)
