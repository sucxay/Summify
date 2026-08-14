"""
Abstract base class for vector store implementations.

Defines the contract that all vector stores must follow.
Concrete implementations (ChromaDB, Qdrant, Pinecone, etc.)
inherit from this class and implement these methods.

This allows the rest of the application to work with ANY
vector store without knowing which one is being used.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from app.schemas.chunk import Chunk


class BaseVectorStore(ABC):
    """
    Abstract interface for vector store operations.

    All vector store implementations MUST implement:
    - add_documents: Store chunks and their embeddings.
    - similarity_search: Find chunks similar to a query.
    - delete_document: Remove all chunks of a document.
    - count: Return total number of stored chunks.

    Why an abstract base class?
    - Enforces a consistent API across implementations.
    - Makes it easy to swap backends (ChromaDB → Qdrant → Pinecone).
    - Enables testing with mock implementations.
    - Documents the expected behavior clearly.
    """

    # ------------------------------------------------------------------
    # Abstract Methods (MUST be implemented by subclasses)
    # ------------------------------------------------------------------

    @abstractmethod
    def add_documents(
        self,
        chunks: List[Chunk],
        embeddings: List[List[float]],
    ) -> None:
        """
        Store document chunks and their embedding vectors.

        This is called after chunking and embedding a document.
        Each chunk is stored with its text, metadata, and vector.

        Args:
            chunks: List of Chunk objects from the SemanticChunker.
                    Each chunk has: chunk_id, document_id, text,
                    page_start, page_end, chunk_index, metadata.
            embeddings: List of embedding vectors (list of floats).
                        Must be the SAME length as chunks.
                        embeddings[i] is the vector for chunks[i].

        Raises:
            ValueError: If len(chunks) != len(embeddings).
            StorageError: If the database operation fails.

        Example:
            store.add_documents(
                chunks=[chunk1, chunk2],
                embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]]
            )
        """
        ...

    @abstractmethod
    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find the top_k chunks most similar to the query embedding.

        This is the core retrieval operation. Given a query vector
        (from embedding the user's question), find the closest chunks
        in the vector space.

        Args:
            query_embedding: The embedding vector of the user's query.
                             Shape: [384] for MiniLM.
            top_k: How many results to return (default: 5).
            filter: Optional metadata filter.
                    Example: {"document_id": "doc_123"}
                    Example: {"page_start": {"$gte": 10}}

        Returns:
            List of dicts, each containing:
            {
                "chunk_id": str,      # Unique chunk identifier
                "text": str,          # The chunk's text content
                "metadata": dict,     # Page numbers, document_id, etc.
                "score": float,       # Similarity score (0 to 1, higher = better)
                "document_id": str,   # Which document this chunk belongs to
            }

            Results are sorted by score descending (best match first).

        Example:
            results = store.similarity_search(
                query_embedding=[0.1, 0.2, ...],
                top_k=3
            )
            for r in results:
                print(f"Score: {r['score']:.3f} | {r['text'][:100]}")
        """
        ...

    @abstractmethod
    def delete_document(self, document_id: str) -> None:
        """
        Remove ALL chunks belonging to a specific document.

        This is called when a user deletes a document from the system.
        After this call, no chunks from this document will appear in searches.

        Args:
            document_id: The unique identifier of the document to delete.

        Example:
            store.delete_document("doc_abc123")
        """
        ...

    @abstractmethod
    def count(self) -> int:
        """
        Return the total number of chunks stored across all documents.

        Useful for:
        - Monitoring: "How much data is indexed?"
        - Testing: "Did the chunks actually get stored?"
        - UI: "Showing X chunks indexed"

        Returns:
            Integer count of total chunks.

        Example:
            total = store.count()
            print(f"Vector store contains {total} chunks")
        """
        ...

   
    def get_chunk_by_id(
        self,
        document_id: str,
        chunk_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific chunk by its ID.

        This is an optional convenience method. The default implementation
        is inefficient (searches all collections). Subclasses can override
        with a direct lookup for better performance.

        Args:
            document_id: The document the chunk belongs to.
            chunk_id: The chunk's unique identifier.

        Returns:
            Dict with chunk data, or None if not found.

        Example:
            chunk = store.get_chunk_by_id("doc_123", "doc_123_chunk_0005")
        """
        # Default implementation: not all backends support direct ID lookup
        raise NotImplementedError(
            "Direct chunk lookup not implemented for this vector store"
        )

    def list_documents(self) -> List[str]:
        """
        Return a list of all document IDs in the store.

        Useful for admin dashboards or document management.

        Returns:
            List of document ID strings.

        Example:
            docs = store.list_documents()
            print(f"Indexed documents: {docs}")
        """
        # Default implementation: not all backends track documents separately
        raise NotImplementedError(
            "Document listing not implemented for this vector store"
        )