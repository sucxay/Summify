"""
Common data models and types used across the application.
"""
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class Metadata(BaseModel):
    """
    Base metadata model for documents and chunks.
    """
    title: str
    author: str = "Unknown"
    source_path: str
    file_name: str
    file_extension: str
    page_count: int = 0
    total_words: int = 0
    file_size_mb: float = 0.0
    ingestion_timestamp: str
    chunk_count: int = 0
    avg_words_per_page: float = 0.0
    is_empty: bool = False
    keywords: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None

    class Config:
        extra = "allow"


class DocumentReference(BaseModel):
    """
    Reference to a document in the system.
    """
    document_id: UUID
    file_name: str
    page_count: int


class ProcessingResult(BaseModel):
    """
    Base class for processing results.
    """
    success: bool
    message: Optional[str] = None
    processing_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """
    Standard error response format.
    """
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)