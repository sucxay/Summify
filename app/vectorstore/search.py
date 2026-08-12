"""
Similarity search across ChromaDB collections.
"""

from typing import Any, Dict, List, Optional
import logging

from app.vectorstore.collections import CollectionManager

logger = logging.getLogger(__name__)

SearchResult = Dict[str, Any]


def similarity_search(
    query_embedding: List[float],
    top_k: int = 5,
    document_id: Optional[str] = None,
    metadata_filter: Optional[Dict[str, Any]] = None,
) -> List[SearchResult]:
    """
    Search for chunks similar to the query embedding.

    Args:
        query_embedding: Query embedding vector.
        top_k: Number of results to return.
        document_id: Search only this document's collection.
        metadata_filter: Optional ChromaDB where clause.

    Returns:
        Ranked list of matching chunks.
    """

    collections = _get_target_collections(document_id)

    if not collections:
        return []

    all_results: List[SearchResult] = []

    for collection in collections:
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=metadata_filter,
                include=["documents", "metadatas", "distances"],
            )

            all_results.extend(
                _format_query_results(results)
            )

        except Exception as e:
            logger.error(
                "Error searching collection %s: %s",
                collection.name,
                e,
            )
            continue  # Skip problematic collections

    all_results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return all_results[:top_k]


def search_across_all_collections(
    query_embedding: List[float],
    top_k: int = 5,
) -> List[SearchResult]:
    """
    Search across every collection.
    """
    return similarity_search(
        query_embedding=query_embedding,
        top_k=top_k,
    )


def search_single_document(
    query_embedding: List[float],
    document_id: str,
    top_k: int = 5,
) -> List[SearchResult]:
    """
    Search within a single document.
    """
    return similarity_search(
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=top_k,
    )


def search_with_page_filter(
    query_embedding: List[float],
    document_id: str,
    page_start: Optional[int] = None,
    page_end: Optional[int] = None,
    top_k: int = 5,
) -> List[SearchResult]:
    """
    Search within a document using page filters.
    """

    metadata_filter = _build_page_filter(
        page_start=page_start,
        page_end=page_end,
    )

    return similarity_search(
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=top_k,
        metadata_filter=metadata_filter,
    )


def get_chunk_by_id(
    document_id: str,
    chunk_id: str,
) -> Optional[SearchResult]:
    """
    Retrieve a chunk by ID.
    """

    try:
        collection = get_collection(document_id)

        result = collection.get(ids=[chunk_id])

        if not result or not result.get("ids"):
            return None

        return {
            "chunk_id": result["ids"][0],
            "text": (
                result["documents"][0]
                if result.get("documents")
                else ""
            ),
            "metadata": (
                result["metadatas"][0]
                if result.get("metadatas")
                else {}
            ),
        }

    except Exception as e:
        logger.error(
            "Error retrieving chunk %s: %s",
            chunk_id,
            e,
        )
        return None


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _get_target_collections(
    document_id: Optional[str],
):
    """
    Determine which collections should be searched.
    """

    if document_id is None:
        return CollectionManager.list_collections()

    try:
        return [CollectionManager.get_collection(document_id)]

    except ValueError:
        logger.warning(
            "Collection not found for document: %s",
            document_id,
        )
        return []


def _format_query_results(
    result: Dict[str, Any],
) -> List[SearchResult]:
    """
    Convert raw Chroma query output into structured results.
    """

    chunk_ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    formatted_results: List[SearchResult] = []

    for chunk_id, document, metadata, distance in zip(
        chunk_ids,
        documents,
        metadatas,
        distances,
    ):
        metadata = metadata or {}

        formatted_results.append(
            {
                "chunk_id": chunk_id,
                "text": document,
                "metadata": metadata,
                "score": round(1.0 - distance, 4),
                "document_id": metadata.get(
                    "document_id",
                    "",
                ),
            }
        )

    return formatted_results


def _build_page_filter(
    page_start: Optional[int],
    page_end: Optional[int],
) -> Optional[Dict[str, Any]]:
    """
    Build a ChromaDB page filter.
    """

    if page_start is not None and page_end is not None:
        return {
            "$and": [
                {"page_start": {"$gte": page_start}},
                {"page_end": {"$lte": page_end}},
            ]
        }

    if page_start is not None:
        return {"page_start": {"$gte": page_start}}

    if page_end is not None:
        return {"page_end": {"$lte": page_end}}

    return None