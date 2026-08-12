"""
Search Service - Semantic search across documents.
"""
from typing import Optional, List, Dict, Any
import logging

from app.rag.retriever import Retriever

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_id: Optional[str] = None,
        min_score: float = 0.0,
    ) -> Dict[str, Any]:
        if min_score > 0:
            results = self.retriever.retrieve_with_scores(
                query=query,
                top_k=top_k,
                document_id=document_id,
                min_score=min_score,
            )
        else:
            results = self.retriever.retrieve(
                query=query,
                top_k=top_k,
                document_id=document_id,
            )

        return {
            "query": query,
            "results": results,
            "total_results": len(results),
        }

    def search_by_page_range(
        self,
        query: str,
        document_id: str,
        page_start: int,
        page_end: int,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        results = self.retriever.retrieve_by_page_range(
            query=query,
            document_id=document_id,
            page_start=page_start,
            page_end=page_end,
            top_k=top_k,
        )

        return {
            "query": query,
            "document_id": document_id,
            "page_range": f"{page_start}-{page_end}",
            "results": results,
            "total_results": len(results),
        }