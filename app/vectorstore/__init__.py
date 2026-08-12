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
        PersistenceManager instance with search capabilities.

    Example:
        store = get_vector_store()
        store.add_documents(chunks, embeddings)
        results = store.search(query_embedding, top_k=5)
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
    "get_vector_store",
    "reset_vector_store",
]
