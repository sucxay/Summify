"""
Custom exceptions for the Summify application.
"""

class SummifyException(Exception):
    """Base exception for all Summify errors."""
    def __init__(self, message: str, detail: dict = None):
        self.message = message
        self.detail = detail or {}
        super().__init__(self.message)


class FileNotFoundError(SummifyException):
    """File does not exist or is not accessible."""
    pass


class InvalidFileTypeError(SummifyException):
    """File type is not supported."""
    pass


class FileTooLargeError(SummifyException):
    """File exceeds size limit."""
    pass


class EmptyFileError(SummifyException):
    """File is empty (0 bytes)."""
    pass


class CorruptedFileError(SummifyException):
    """File is corrupted or unreadable."""
    pass


class DocumentProcessingError(SummifyException):
    """Error during document processing."""
    pass


class EmbeddingError(SummifyException):
    """Error generating embeddings."""
    pass


class RetrievalError(SummifyException):
    """Error during document retrieval."""
    pass


class SummaryGenerationError(SummifyException):
    """Error generating summary."""
    pass


class ConfigurationError(SummifyException):
    """Application configuration error."""
    pass