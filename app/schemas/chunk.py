"""
Chunk data models for document processing.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4

from app.schemas.common import Metadata


class ChunkMetadata(BaseModel):
    """
    Metadata specific to a document chunk.
    """
    chunk_id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    chunk_index: int
    source_page: Optional[int] = None
    word_count: int
    character_count: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_first_chunk: bool = False
    is_last_chunk: bool = False


class Chunk(BaseModel):
    """
    A chunk of document content with associated metadata.
    """
    content: str
    metadata: ChunkMetadata
    document_metadata: Metadata

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class ChunkingResult(BaseModel):
    """
    Result of the chunking process for a document.
    """
    chunks: list[Chunk]
    total_chunks: int
    total_words: int
    total_characters: int