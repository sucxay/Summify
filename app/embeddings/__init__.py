"""
Embedding package for Summify.
Provides local and cloud-based embedding implementations.
"""
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.embedding_factory import create_embedding_service

__all__ = ["EmbeddingService", "create_embedding_service"]