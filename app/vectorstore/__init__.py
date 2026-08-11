"""
Vector Store package for Summify.

Provides:
- ChromaClient: Singleton client for ChromaDB connection.
- CollectionManager: Manager for ChromaDB collections.
- PersistenceManager: Manager for document persistence.
- similarity_search: Function for searching similar documents.
- get_vector_store(): Factory function returning a singleton vector store instance.

Usage:
    from app.vectorstore import get_vector_store, CollectionManager

    store = get_vector_store()
    store.add_documents(chunks, embeddings)
    results = store.similarity_search(query_embedding, top_k=5)
"""
from typing import Optional

from app.vectorstore.chroma import ChromaClient
from app.vectorstore.collections import CollectionManager
from app.vectorstore.persistence import PersistenceManager
from app.vectorstore.search import similarity_search

# ---------------------------------------------------------------------------
# Singleton instance
# ---------------------------------------------------------------------------
# Module-level variable holding the one and only vector store instance.
# Underscore prefix (_) signals: "this is internal, use get_vector_store() instead."
_vector_store_instance: Optional[PersistenceManager] = None


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------

def get_vector_store():
    """
    Get the singleton vector store instance.

    On first call, creates a PersistenceManager instance.
    On subsequent calls, returns the same instance.

    This ensures:
    - Only one vector store instance exists.
    - All parts of the app share the same vector store.
    - You can swap the backend by changing ONE line here.

    Returns:
        PersistenceManager instance.

    Example:
        store = get_vector_store()
        store.add_documents(chunks, embeddings)
        count = store.count()
    """
    global _vector_store_instance

    if _vector_store_instance is None:
        _vector_store_instance = PersistenceManager()

    return _vector_store_instance


# ---------------------------------------------------------------------------
# Reset function (for testing)
# ---------------------------------------------------------------------------

def reset_vector_store() -> None:
    """
    Reset the singleton. USEFUL ONLY FOR TESTING.

    In production, you should never need to reset.
    This allows tests to start with a fresh vector store.
    """
    global _vector_store_instance
    _vector_store_instance = None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "ChromaClient",
    "CollectionManager", 
    "PersistenceManager",
    "similarity_search",
    "get_vector_store",
    "reset_vector_store",
]
