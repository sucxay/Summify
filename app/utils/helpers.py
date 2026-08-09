"""
General helper functions.
"""
from typing import Any, Optional


def safe_get(data: dict, *keys, default=None) -> Optional[Any]:
    """
    Safely get a nested value from a dictionary.

    Example:
        data = {"a": {"b": {"c": 1}}}
        safe_get(data, "a", "b", "c")  # returns 1
        safe_get(data, "a", "x")       # returns None
    """
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data