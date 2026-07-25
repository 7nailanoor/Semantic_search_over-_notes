"""
Helper Functions

Common utility functions used throughout the project.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from datetime import datetime


def save_json(
    data: Any,
    file_path: str | Path,
) -> None:
    """
    Save data to a JSON file.
    """

    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def load_json(
    file_path: str | Path,
):
    """
    Load JSON file.

    Returns an empty dictionary if the
    file does not exist.
    """

    path = Path(file_path)

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_file_size(
    size: int,
) -> str:
    """
    Convert bytes to a human-readable format.
    """

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    size = float(size)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def current_timestamp() -> str:
    """
    Return current timestamp.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_directory(
    directory: str | Path,
) -> Path:
    """
    Create a directory if it doesn't exist.
    """

    path = Path(directory)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def truncate_text(
    text: str,
    max_length: int = 150,
) -> str:
    """
    Truncate text for previews.
    """

    if len(text) <= max_length:
        return text

    return text[:max_length].rstrip() + "..."


def safe_filename(
    filename: str,
) -> str:
    """
    Remove invalid filename characters.
    """

    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        filename = filename.replace(char, "_")

    return filename.strip()


def percentage(
    part: int,
    total: int,
) -> float:
    """
    Calculate percentage.
    """

    if total == 0:
        return 0.0

    return round(
        (part / total) * 100,
        2,
    )
