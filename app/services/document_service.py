"""
Document Service - Handles document upload, processing, and indexing.
"""
from pathlib import Path
from typing import Optional, List, Dict, Any
import uuid
import logging

from app.ingestion.validators import DocumentValidator
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.text_cleaner import TextCleaner
from app.ingestion.metadata import MetadataExtractor
from app.ingestion.chunker import SemanticChunker
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.base import BaseVectorStore

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(
        self,
        embed_service: EmbeddingService,
        vector_store: BaseVectorStore,
        upload_dir: Path,
    ):
        self.embed_service = embed_service
        self.vector_store = vector_store
        self.upload_dir = upload_dir
        self.validator = DocumentValidator()
        self.loader = PDFLoader()
        self.cleaner = TextCleaner()
        self.metadata_extractor = MetadataExtractor()
        self.chunker = SemanticChunker()
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def process_document(self, file_path: Path) -> Dict[str, Any]:
        validation_result = self.validator.validate(file_path)
        document_id = str(uuid.uuid4())

        pages, raw_metadata = self.loader.load(file_path)

        for page in pages:
            page.text = self.cleaner.clean_for_chunking(page.text)

        metadata = self.metadata_extractor.enrich(raw_metadata, file_path)
        metadata["document_id"] = document_id

        chunks = self.chunker.chunk_document(pages, metadata, document_id)
        metadata["chunk_count"] = len(chunks)

        if chunks:
            embeddings = self.embed_service.embed_chunks(chunks)
            self.vector_store.add_documents(chunks, embeddings)

        logger.info(f"Document processed: {document_id} with {len(chunks)} chunks")

        return {
            "document_id": document_id,
            "metadata": metadata,
            "chunk_count": len(chunks),
            "status": "indexed",
        }

    def delete_document(self, document_id: str) -> bool:
        try:
            self.vector_store.delete_document(document_id)
            logger.info(f"Document deleted: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False

    def get_document_info(self, document_id: str) -> Optional[Dict[str, Any]]:
        try:
            collections = self.vector_store.list_documents()
            if document_id in collections:
                return {
                    "document_id": document_id,
                    "status": "indexed",
                }
        except Exception:
            pass
        return None

    def list_documents(self) -> List[str]:
        try:
            return self.vector_store.list_documents()
        except Exception:
            return []