from pathlib import Path
import fitz

from typing import Any
from dataclasses import dataclass, field

from app.config.constants import HEADING_FONT_THRESHOLD
from app.utils.timers import timeit


@dataclass
class ExtractedPage:
    page_number: int
    text: str
    tables: list[list[list[str]]] = field(default_factory=list)
    headings: list[str] = field(default_factory=list)
    word_count: int = 0


class PDFLoader:
    def __init__(
        self,
        extract_tables: bool = True,
        heading_font_threshold: float = HEADING_FONT_THRESHOLD,
    ):
        self.extract_tables = extract_tables
        self.heading_font_threshold = heading_font_threshold

    @timeit
    def load(
        self, file_path: Path
    ) -> tuple[list[ExtractedPage], dict[str, Any]]:
        pages = []

        with fitz.open(str(file_path)) as doc:
            for page_num in range(doc.page_count):
                page = doc[page_num]
                extracted = self._extract_page(page, page_num + 1)
                pages.append(extracted)

            metadata = self._extract_metadata(doc, file_path)

        return pages, metadata

    def _extract_page(
        self,
        page: fitz.Page,
        page_num: int,
    ) -> ExtractedPage:
        blocks = page.get_text("dict")["blocks"]
        text_blocks = [block for block in blocks if block["type"] == 0]

        text_lines = []
        headings = []

        for block in text_blocks:
            for line in block.get("lines", []):
                line_text = ""
                max_font_size = 0

                for span in line.get("spans", []):
                    line_text += span["text"]
                    max_font_size = max(max_font_size, span["size"])

                line_text = line_text.strip()

                if line_text:
                    text_lines.append(line_text)

                    if max_font_size >= self.heading_font_threshold:
                        headings.append(line_text)

        full_text = "\n".join(text_lines)

        tables = []
        if self.extract_tables:
            tables = self._extract_tables(page)

        return ExtractedPage(
            page_number=page_num,
            text=full_text,
            tables=tables,
            headings=headings,
            word_count=len(full_text.split()),
        )

    def _extract_tables(
        self,
        page: fitz.Page,
    ) -> list[list[list[str]]]:
        tables = []

        try:
            found_tables = page.find_tables()

            for table in found_tables:
                extracted = table.extract()

                if extracted:
                    tables.append(extracted)

        except Exception:
            return []

        return tables

    def _extract_metadata(
        self,
        doc: fitz.Document,
        file_path: Path,
    ) -> dict[str, Any]:
        meta = doc.metadata

        total_words = 0

        for page_num in range(doc.page_count):
            page = doc[page_num]
            total_words += len(page.get_text("text").split())

        return {
            "title": meta.get("title") or file_path.stem,
            "author": meta.get("author") or "Unknown",
            "subject": meta.get("subject") or "",
            "keywords": meta.get("keywords") or "",
            "creator": meta.get("creator") or "",
            "page_count": doc.page_count,
            "total_words": total_words,
            "file_size_mb": round(file_path.stat().st_size / (1024 * 1024), 2),
            "source_path": str(file_path.resolve()),
            "file_name": file_path.name,
        }