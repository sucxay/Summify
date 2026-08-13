"""
Token counting utilities.
Uses tiktoken for OpenAI-compatible token counting.
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


try:
    import tiktoken
    _TIKTOKEN_AVAILABLE = True
except ImportError:
    _TIKTOKEN_AVAILABLE = False


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count the number of tokens in a text string.

    Uses tiktoken if available, otherwise falls back to
    a simple word-count approximation (4 chars ≈ 1 token).

    Args:
        text: The text to count tokens for.
        model: Model name for tiktoken encoding.

    Returns:
        Approximate token count.
    """
    if not text:
        return 0

    if _TIKTOKEN_AVAILABLE:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(
                "Failed to count tokens with tiktoken: %s. Falling back to character approximation.",
                e
            )

    # Fallback: approximate 1 token ≈ 4 characters
    return len(text) // 4


def truncate_tokens(text: str, max_tokens: int, model: str = "gpt-4") -> str:
    """
    Truncate text to fit within a token limit.

    Args:
        text: Text to truncate.
        max_tokens: Maximum token count.
        model: Model name for tiktoken encoding.

    Returns:
        Truncated text.
    """
    if not text:
        return ""

    if _TIKTOKEN_AVAILABLE:
        try:
            encoding = tiktoken.encoding_for_model(model)
            tokens = encoding.encode(text)
            if len(tokens) <= max_tokens:
                return text
            truncated_tokens = tokens[:max_tokens]
            return encoding.decode(truncated_tokens)
        except Exception as e:
            logger.warning(
                "Failed to truncate tokens with tiktoken: %s. Falling back to character truncation.",
                e
            )

    # Fallback: simple character-based truncation
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    return text[:max_chars]