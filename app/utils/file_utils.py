"""
File utility functions.
"""
from pathlib import Path
from typing import Optional


def ensure_directory(path: Path) -> Path:
    """Create directory if it doesn't exist and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size_mb(file_path: Path) -> float:
    """Return file size in megabytes."""
    return file_path.stat().st_size / (1024 * 1024)


def safe_filename(filename: str) -> str:
    """
    Remove potentially dangerous characters from a filename.
    Keeps alphanumeric, underscores, hyphens, and dots.
    """
    return "".join(c for c in filename if c.isalnum() or c in "._- ")