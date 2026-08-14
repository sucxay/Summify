"""
Reranker - Re-ranks retrieved chunks using cross-encoder for better relevance.
"""
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name)
        return self._model

    def rerank(
        self,
        query: str,
        results: List[Dict[str, Any]],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        if not results:
            return []

        pairs = [[query, r["text"]] for r in results]
        scores = self.model.predict(pairs)

        for i, result in enumerate(results):
            result["rerank_score"] = float(scores[i])

        results.sort(key=lambda x: x.get("rerank_score", 0), reverse=True)

        k = top_k or len(results)
        return results[:k]

    def rerank_and_filter(
        self,
        query: str,
        results: List[Dict[str, Any]],
        min_score: float = 0.5,
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        reranked = self.rerank(query, results)
        filtered = [r for r in reranked if r.get("rerank_score", 0) >= min_score]
        return filtered[:top_k] if top_k else filtered