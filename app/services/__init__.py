"""
Services Layer - Orchestration layer between API routes and lower-level components.

This layer provides:
- Input validation
- Business logic coordination
- Error handling and propagation
- Dependency injection
- Type safety
- Proper logging

Services:
- ChatService: Chat completion and conversation management
- RAGService: Retrieval orchestration and response generation
- IngestionService: Document processing and vector store insertion
- DocumentService: Document management operations
"""

from app.services.base import BaseService
from app.services.exceptions import (
    ServiceException,
    ValidationException,
    NotFoundException,
    DocumentProcessingException,
    RetrievalException,
    GenerationException,
)

__all__ = [
    "BaseService",
    "ServiceException",
    "ValidationException",
    "NotFoundException",
    "DocumentProcessingException",
    "RetrievalException",
    "GenerationException",
]
