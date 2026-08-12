"""
RAG Pipeline - Orchestrates the complete retrieval-to-generation flow.
"""
from typing import Optional, Dict, Any, List
import logging

from app.rag.retriever import Retriever
from app.rag.generator import Generator
from app.utils.timers import timeit

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(
        self,
        retriever: Retriever,
        generator: Generator,
        default_top_k: int = 5,
    ):
        self.retriever = retriever
        self.generator = generator
        self.default_top_k = default_top_k

    @timeit
    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        summary_type: str = "general",
        document_id: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        k = top_k or self.default_top_k

        logger.info(f"RAG Pipeline query: '{question[:100]}...'")

        context = self.retriever.retrieve_context(
            query=question,
            top_k=k,
            context_type="qa",
            document_id=document_id,
        )

        answer = self.generator.generate(
            context=context,
            query=question,
            summary_type=summary_type,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "query": question,
            "answer": answer,
            "context": context,
        }

    def summarize(
        self,
        query: str,
        document_id: Optional[str] = None,
        summary_type: str = "general",
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        k = top_k or self.default_top_k

        logger.info(f"RAG Pipeline summarize: '{query[:100]}...'")

        context = self.retriever.retrieve_context(
            query=query,
            top_k=k,
            context_type="summary",
            document_id=document_id,
        )

        summary = self.generator.generate_summary(
            context=context,
            summary_type=summary_type,
        )

        return {
            "query": query,
            "summary": summary,
            "context": context,
        }

    def chat(
        self,
        message: str,
        document_id: Optional[str] = None,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        return self.query(
            question=message,
            top_k=top_k,
            document_id=document_id,
            summary_type="general",
        )