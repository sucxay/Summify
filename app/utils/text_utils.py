"""
Text utility functions.
"""
import re


def word_count(text: str) -> int:
    """Count words in a string."""
    return len(text.split()) if text else 0


def truncate(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to a maximum length, adding suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


def clean_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into a single space."""
    return re.sub(r'\s+', ' ', text).strip()