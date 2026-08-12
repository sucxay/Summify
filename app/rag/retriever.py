from typing import List , Any ,Dict ,Optional 

import logging 

from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.base import BaseVectorStore

from app.rag.context_builder import ContextBuilder

from app.config.constants import TOP_K_DEFAULT

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self, embedding_service: EmbeddingService, vector_store: BaseVectorStore, context_builder: ContextBuilder, top_k: int = TOP_K_DEFAULT):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.context_builder = context_builder
        self.top_k = top_k


    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        document_id: Optional[str] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:

        if not query or not query.strip():
            logger.warning("Empty query provided to retriever.")
            return []
        
        k = top_k if top_k is not None else self.top_k

        logger.debug(f"Embedding query: {query}")
        query_embedding = self.embedding_service.embed_single(query)

        logger.debug(f"Searching for top_{k} chunks....")

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=k,
            document_id=document_id,
            metadata_filter=metadata_filter
        )

        if document_id and results:
            results = [r for r in results if r.get("document_id") == document_id]

        logger.info(f"Retrieved {len(results)} chunks for query: '{query[:80]}...'")
        return results
    

    def retrieve_context(
        self,
        query: str,
        top_k: Optional[int] = None,
        document_id: Optional[str] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
        context_type: str = "qa",
    ) -> str:
        results = self.retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
            metadata_filter=metadata_filter,
        )

        if not results:
            logger.warning(f"No results found for query: '{query[:80]}...'")
            return "No relevant information found in the documents."

        if context_type == "summary":
            context = self.context_builder.build_for_summary(results, query)
        elif context_type == "chat":
            context = self.context_builder.build_for_chat(results)
        else:
            context = self.context_builder.build_for_qa(results, query)

        return context

    def retrieve_with_scores(
        self,
        query: str,
        top_k: Optional[int] = None,
        min_score: float = 0.0,
        document_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = self.retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
        )

        if min_score > 0:
            filtered = [r for r in results if r.get("score", 0) >= min_score]
            logger.debug(
                f"Score filter ({min_score}): {len(results)} → {len(filtered)} chunks"
            )
            return filtered

        return results

    def retrieve_from_document(
        self,
        query: str,
        document_id: str,
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        return self.retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
        )

    def retrieve_by_page_range(
        self,
        query: str,
        document_id: str,
        page_start: int,
        page_end: int,
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        metadata_filter = {
            "$and": [
                {"page_start": {"$gte": page_start}},
                {"page_end": {"$lte": page_end}},
            ]
        }

        return self.retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
            metadata_filter=metadata_filter,
        )

    def get_relevant_texts(
        self,
        query: str,
        top_k: Optional[int] = None,
        document_id: Optional[str] = None,
    ) -> List[str]:
        results = self.retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
        )
        return [r["text"] for r in results]

    def get_retrieval_stats(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        results = self.retrieve(query=query, top_k=top_k)

        if not results:
            return {
                "query": query,
                "num_results": 0,
                "avg_score": 0.0,
                "max_score": 0.0,
                "documents_found": 0,
            }

        scores = [r.get("score", 0) for r in results]
        doc_ids = set(r.get("document_id", "") for r in results)

        return {
            "query": query,
            "num_results": len(results),
            "avg_score": round(sum(scores) / len(scores), 4),
            "max_score": round(max(scores), 4),
            "min_score": round(min(scores), 4),
            "documents_found": len(doc_ids),
            "document_ids": list(doc_ids),
            "top_chunk_preview": results[0]["text"][:100] + "..." if results else "",
        }




    

