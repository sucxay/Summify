"""
Semantic chunker respecting document structure.
"""
from dataclasses import dataclass, field

from app.ingestion.text_cleaner import TextCleaner
from app.config.constants import CHUNK_SIZE, CHUNK_OVERLAP, MIN_CHUNK_SIZE


@dataclass
class Chunk:
    """A semantic chunk of document text."""
    chunk_id: str
    document_id: str
    text: str
    page_start: int
    page_end: int
    chunk_index: int
    word_count: int
    metadata: dict = field(default_factory=dict)


class SemanticChunker:
    """
    Creates chunks respecting page and paragraph boundaries.

    Usage:
        chunker = SemanticChunker(chunk_size=1000, chunk_overlap=200)
        chunks = chunker.chunk_document(pages, metadata, "doc_001")
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        min_chunk_size: int = MIN_CHUNK_SIZE,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.cleaner = TextCleaner()

    def chunk_document(
        self, pages, metadata: dict, document_id: str
    ) -> list[Chunk]:
        """Chunk entire document into semantic chunks."""
        # Step 1: Clean all page texts
        page_texts = []
        for page in pages:
            cleaned = self.cleaner.clean_for_chunking(page.text)
            if cleaned:
                page_texts.append({
                    "page_num": page.page_number,
                    "text": cleaned,
                    "word_count": len(cleaned.split()),
                })

        if not page_texts:
            return []

        # Step 2: Create chunks respecting page boundaries
        raw_chunks = self._create_chunks(page_texts)

        # Step 3: Merge small chunks with neighbors
        merged_chunks = self._merge_small_chunks(raw_chunks)

        # Step 4: Build final Chunk objects
        final_chunks = []
        for i, chunk_data in enumerate(merged_chunks):
            chunk = Chunk(
                chunk_id=f"{document_id}_chunk_{i:04d}",
                document_id=document_id,
                text=chunk_data["text"],
                page_start=chunk_data["page_start"],
                page_end=chunk_data["page_end"],
                chunk_index=i,
                word_count=len(chunk_data["text"].split()),
                metadata={
                    "document_title": metadata.get("title", ""),
                    "page_range": f"{chunk_data['page_start']}-{chunk_data['page_end']}",
                },
            )
            final_chunks.append(chunk)

        return final_chunks

    def _create_chunks(self, page_texts: list[dict]) -> list[dict]:
        """Create initial chunks, splitting oversized pages."""
        chunks = []
        current_text = ""
        current_start = None
        current_end = None

        for page_data in page_texts:
            page_text = page_data["text"]
            page_num = page_data["page_num"]

            # If single page exceeds chunk limit, split it into sub-chunks
            if page_data["word_count"] > self.chunk_size:
                # Flush current chunk first
                if current_text:
                    chunks.append({
                        "text": current_text.strip(),
                        "page_start": current_start,
                        "page_end": current_end,
                    })
                    current_text = ""
                    current_start = None

                # Split the long page
                sub_chunks = self._split_long_text(page_text, page_num)
                chunks.extend(sub_chunks)
                continue

            # Try adding this page to current chunk
            separator = "\n\n" if current_text else ""
            test_text = current_text + separator + page_text

            if len(test_text.split()) <= self.chunk_size:
                current_text = test_text
                if current_start is None:
                    current_start = page_num
                current_end = page_num
            else:
                # Save current chunk, start new one
                if current_text:
                    chunks.append({
                        "text": current_text.strip(),
                        "page_start": current_start,
                        "page_end": current_end,
                    })
                current_text = page_text
                current_start = page_num
                current_end = page_num

        # Don't forget the last chunk
        if current_text:
            chunks.append({
                "text": current_text.strip(),
                "page_start": current_start,
                "page_end": current_end,
            })

        return chunks

    def _split_long_text(self, text: str, page_num: int) -> list[dict]:
        """Split a long text into smaller chunks by paragraph boundaries."""
        paragraphs = text.split("\n\n")
        chunks = []
        current = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            test = current + "\n\n" + para if current else para

            if len(test.split()) <= self.chunk_size:
                current = test
            else:
                if current:
                    chunks.append({
                        "text": current.strip(),
                        "page_start": page_num,
                        "page_end": page_num,
                    })
                current = para

        if current:
            chunks.append({
                "text": current.strip(),
                "page_start": page_num,
                "page_end": page_num,
            })

        return chunks

    def _merge_small_chunks(self, chunks: list[dict]) -> list[dict]:
        """Merge chunks smaller than min_chunk_size with their neighbor."""
        if len(chunks) <= 1:
            return chunks

        merged = []
        i = 0

        while i < len(chunks):
            current = chunks[i]
            words = len(current["text"].split())

            if words < self.min_chunk_size and i + 1 < len(chunks):
                next_chunk = chunks[i + 1]
                merged_text = current["text"] + "\n\n" + next_chunk["text"]
                merged.append({
                    "text": merged_text,
                    "page_start": current["page_start"],
                    "page_end": next_chunk["page_end"],
                })
                i += 2
            else:
                merged.append(current)
                i += 1

        return merged