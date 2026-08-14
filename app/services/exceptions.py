"""
Domain-specific exception hierarchy for the Services layer.
All service-level errors inherit from ``ServiceException`` so that API layers can
catch a single base class if desired.
"""

from __future__ import annotations

from typing import Any


class ServiceException(RuntimeError):
    """Base class for all service-level exceptions."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(message)
        self.details = details


class ValidationException(ServiceException):
    """Raised when input validation fails."""


class NotFoundException(ServiceException):
    """Raised when a requested resource cannot be found."""


class DocumentProcessingException(ServiceException):
    """Raised during document ingestion or chunking errors."""


class RetrievalException(ServiceException):
    """Raised when the retriever cannot obtain relevant chunks."""


class GenerationException(ServiceException):
    """Raised when the LLM generator fails."""
