"""
Metadata enrichment for documents.
"""
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


class MetadataExtractor:
    """Enriches raw PDF metadata with computed fields."""

    @staticmethod
    def enrich(
        raw_metadata: dict[str, Any],
        file_path: Path,
        chunk_count: int = 0,
            total_chunks: int = 0,
    ) -> dict[str, Any]:
        """
        Add computed metadata fields.

        Args:
            raw_metadata: From PDFLoader._extract_metadata()
            file_path: Original file path
            chunk_count: Number of chunks created (added after chunking)

        Returns:
            Enriched metadata dict
        """
        page_count = raw_metadata.get("page_count", 0)
        total_words = raw_metadata.get("total_words", 0)

        return {
            **raw_metadata,
            "file_extension": file_path.suffix.lower(),
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
            "chunk_count": chunk_count,
            "avg_words_per_page": (
                round(total_words / page_count, 1)
                if page_count > 0
                else 0
            ),
            "is_empty": total_words == 0,
        }