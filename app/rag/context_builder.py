"""
Context Builder - Formats retrieved chunks into LLM-ready prompts.

Takes raw results from vector store search and builds structured,
token-aware context blocks with proper attribution and instructions.
"""
from typing import List, Dict, Any, Optional
import logging

from app.utils.tokenizer import count_tokens, truncate_tokens
from app.config.constants import MAX_CONTEXT_TOKENS

logger = logging.getLogger(__name__)


class ContextBuilder:
    """
    Builds formatted context from retrieved chunks.

    Responsibilities:
    - Extract and format chunk texts
    - Add source attribution (page numbers, document titles)
    - Manage token budget (fit within LLM context window)
    - Structure context for different use cases (summary, chat, QA)

    Usage:
        builder = ContextBuilder(max_tokens=4000)
        context = builder.build_for_summary(search_results, query)
    """

    def __init__(
        self,
        max_tokens: int = MAX_CONTEXT_TOKENS,
        include_metadata: bool = True,
        include_scores: bool = False,
    ):
        """
        Args:
            max_tokens: Maximum tokens for the entire context block.
                        If chunks exceed this, they are truncated.
            include_metadata: Add [Page X, Doc: Y] labels to chunks.
            include_scores: Add relevance scores (useful for debugging).
        """
        self.max_tokens = max_tokens
        self.include_metadata = include_metadata
        self.include_scores = include_scores

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def build_for_summary(
        self,
        search_results: List[Dict[str, Any]],
        query: str = "",
        summary_type: str = "general",
    ) -> str:
        """
        Build context optimized for document summarization.

        Merges all chunks into a flowing text block with
        document structure preserved.

        Args:
            search_results: List of dicts from vectorstore.search().
            query: The user's summary request.
            summary_type: Type of summary (general, executive, etc.)

        Returns:
            Formatted context string ready for the LLM prompt.
        """
        if not search_results:
            logger.warning("No search results provided for context building.")
            return ""

        # Group chunks by document to preserve structure
        grouped = self._group_by_document(search_results)

        context_parts = []

        for doc_id, chunks in grouped.items():
            doc_title = self._get_document_title(chunks)
            context_parts.append(f"### Document: {doc_title}")

            for i, chunk in enumerate(chunks, 1):
                chunk_text = chunk["text"]
                metadata = chunk.get("metadata", {})

                # Add source attribution
                if self.include_metadata:
                    page_info = self._format_page_range(metadata)
                    chunk_header = f"\n[Chunk {i}{page_info}]"
                else:
                    chunk_header = ""

                # Add score if debugging
                if self.include_scores:
                    score = chunk.get("score", 0)
                    chunk_header += f" (relevance: {score:.2f})"

                context_parts.append(f"{chunk_header}\n{chunk_text}")

        # Join all parts
        full_context = "\n".join(context_parts)

        # Add query context if provided
        if query:
            full_context = (
                f"User Request: {query}\n\n"
                f"Document Excerpts:\n{full_context}"
            )

        # Truncate if exceeds token limit
        return self._enforce_token_limit(full_context)

    def build_for_chat(
        self,
        search_results: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Build context for conversational QA.

        Formats chunks as numbered references for citation.
        Includes conversation history if provided.

        Args:
            search_results: List of dicts from vectorstore.search().
            conversation_history: Previous messages as [{"role": "...", "content": "..."}].

        Returns:
            Formatted context string for chat prompt.
        """
        if not search_results:
            return "No relevant information found in the documents."

        parts = []

        # Add conversation history
        if conversation_history:
            parts.append("### Previous Conversation")
            for msg in conversation_history[-3:]:  # Last 3 messages
                role = msg.get("role", "user").capitalize()
                content = msg.get("content", "")
                parts.append(f"{role}: {content}")
            parts.append("")

        # Add document context with numbered references
        parts.append("### Relevant Document Excerpts")
        parts.append("Use the numbers in [brackets] to cite sources.\n")

        for i, chunk in enumerate(search_results, 1):
            text = chunk["text"]
            metadata = chunk.get("metadata", {})

            # Build citation reference
            citation = f"[{i}]"
            if self.include_metadata:
                page_start = metadata.get("page_start", "")
                page_end = metadata.get("page_end", "")
                if page_start and page_end:
                    citation += f" (Page {page_start}-{page_end})"
                elif page_start:
                    citation += f" (Page {page_start})"

            parts.append(f"{citation}\n{text}\n")

        full_context = "\n".join(parts)
        return self._enforce_token_limit(full_context)

    def build_for_qa(
        self,
        search_results: List[Dict[str, Any]],
        question: str,
    ) -> str:
        """
        Build context for direct question answering.

        Simple format: just the texts, separated by newlines.
        Prioritizes the most relevant chunks.

        Args:
            search_results: List of dicts from vectorstore.search().
            question: The user's question.

        Returns:
            Formatted context string.
        """
        if not search_results:
            return ""

        # Sort by score (already sorted, but ensure it)
        sorted_results = sorted(
            search_results,
            key=lambda x: x.get("score", 0),
            reverse=True,
        )

        texts = []
        for chunk in sorted_results:
            text = chunk["text"].strip()
            if text:
                texts.append(text)

        if not texts:
            return ""

        context = (
            f"Question: {question}\n\n"
            f"Relevant Information:\n"
            + "\n\n".join(texts)
        )

        return self._enforce_token_limit(context)

    def build_prompt(
        self,
        search_results: List[Dict[str, Any]],
        system_prompt: str,
        user_query: str,
    ) -> str:
        """
        Build a complete LLM prompt with system instructions,
        context, and user query.

        Args:
            search_results: List of dicts from vectorstore.search().
            system_prompt: System instructions for the LLM.
            user_query: The user's question or request.

        Returns:
            Complete prompt string.
        """
        context = self.build_for_qa(search_results, user_query)

        prompt = f"{system_prompt}\n\n{context}"

        return prompt

    # ------------------------------------------------------------------
    # Private Helper Methods
    # ------------------------------------------------------------------

    def _group_by_document(
        self,
        results: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group search results by document_id.

        Preserves document structure in the context.

        Args:
            results: Search results list.

        Returns:
            Dict mapping document_id → list of chunks.
        """
        grouped = {}

        for item in results:
            doc_id = item.get("document_id") or item.get("metadata", {}).get(
                "document_id", "unknown"
            )
            if doc_id not in grouped:
                grouped[doc_id] = []
            grouped[doc_id].append(item)

        # Sort chunks within each document by chunk_index
        for doc_id in grouped:
            grouped[doc_id].sort(
                key=lambda x: x.get("metadata", {}).get("chunk_index", 0)
            )

        return grouped

    def _get_document_title(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Extract document title from chunk metadata.

        Args:
            chunks: List of chunks from the same document.

        Returns:
            Document title or document_id if title not found.
        """
        for chunk in chunks:
            metadata = chunk.get("metadata", {})
            title = metadata.get("document_title") or metadata.get("title")
            if title:
                return title

        # Fallback to document_id
        return chunks[0].get("document_id", "Unknown Document")

    def _format_page_range(self, metadata: Dict[str, Any]) -> str:
        """
        Format page range for display.

        Args:
            metadata: Chunk metadata dict.

        Returns:
            String like " (Pages 5-7)" or " (Page 3)" or "".
        """
        page_start = metadata.get("page_start")
        page_end = metadata.get("page_end")

        if page_start is not None and page_end is not None:
            if page_start == page_end:
                return f", Page {page_start}"
            return f", Pages {page_start}-{page_end}"

        if page_start is not None:
            return f", Page {page_start}"

        return ""

    def _enforce_token_limit(self, text: str) -> str:
        """
        Truncate text if it exceeds the maximum token limit.

        Truncation strategy:
        - Count tokens
        - If over limit, truncate from the end
        - Add a warning that content was truncated

        Args:
            text: The full context text.

        Returns:
            Text guaranteed to be within token limit.
        """
        token_count = count_tokens(text)

        if token_count <= self.max_tokens:
            return text

        logger.warning(
            f"Context exceeds token limit ({token_count} > {self.max_tokens}). "
            f"Truncating..."
        )

        truncated = truncate_tokens(text, self.max_tokens)

        return truncated + "\n\n[Note: Some context was truncated due to length limits.]"

    def get_stats(
        self,
        search_results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Return statistics about the context that would be built.

        Useful for debugging and monitoring.

        Args:
            search_results: Search results to analyze.

        Returns:
            Dict with statistics.
        """
        if not search_results:
            return {
                "num_chunks": 0,
                "num_documents": 0,
                "total_tokens": 0,
                "avg_score": 0.0,
            }

        context = self.build_for_summary(search_results)
        scores = [r.get("score", 0) for r in search_results]
        doc_ids = set()

        for r in search_results:
            doc_id = r.get("document_id") or r.get("metadata", {}).get("document_id")
            if doc_id:
                doc_ids.add(doc_id)

        return {
            "num_chunks": len(search_results),
            "num_documents": len(doc_ids),
            "total_tokens": count_tokens(context),
            "avg_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "max_score": round(max(scores), 4) if scores else 0.0,
            "min_score": round(min(scores), 4) if scores else 0.0,
        }