"""
Summary Service - Generates summaries using RAG pipeline.
"""
from typing import Optional, Dict, Any
import logging

from app.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)


class SummaryService:
    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline

    def generate_summary(
        self,
        query: str,
        document_id: Optional[str] = None,
        summary_type: str = "general",
        top_k: int = 5,
    ) -> Dict[str, Any]:
        result = self.rag_pipeline.summarize(
            query=query,
            document_id=document_id,
            summary_type=summary_type,
            top_k=top_k,
        )
        return {
            "query": result["query"],
            "summary": result["summary"],
            "document_id": document_id,
            "summary_type": summary_type,
        }

    def generate_executive_summary(
        self,
        document_id: str,
    ) -> Dict[str, Any]:
        return self.generate_summary(
            query="Provide an executive summary of this document",
            document_id=document_id,
            summary_type="executive",
            top_k=10,
        )

    def generate_bullet_points(
        self,
        document_id: str,
        topic: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = f"Extract key points about {topic}" if topic else "Extract all key points"
        return self.generate_summary(
            query=query,
            document_id=document_id,
            summary_type="bullet_points",
            top_k=10,
        )

    def generate_key_findings(self, document_id: str) -> Dict[str, Any]:
        return self.generate_summary(
            query="What are the key findings and conclusions?",
            document_id=document_id,
            summary_type="key_findings",
            top_k=10,
        )

    def generate_action_items(self, document_id: str) -> Dict[str, Any]:
        return self.generate_summary(
            query="Extract all action items and next steps",
            document_id=document_id,
            summary_type="action_items",
            top_k=10,
        )