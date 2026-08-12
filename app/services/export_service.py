"""
Export Service - Export summaries and results to different formats.
"""
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ExportService:
    def __init__(self, export_dir: Path):
        self.export_dir = export_dir
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_as_text(
        self,
        content: str,
        filename: Optional[str] = None,
    ) -> Path:
        if not filename:
            import uuid
            filename = f"summary_{uuid.uuid4().hex[:8]}.txt"

        filepath = self.export_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Exported text to: {filepath}")
        return filepath

    def export_as_markdown(
        self,
        title: str,
        content: str,
        filename: Optional[str] = None,
    ) -> Path:
        if not filename:
            import uuid
            filename = f"summary_{uuid.uuid4().hex[:8]}.md"

        md_content = f"# {title}\n\n{content}"
        filepath = self.export_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"Exported markdown to: {filepath}")
        return filepath

    def export_summary_result(
        self,
        result: Dict[str, Any],
        format: str = "text",
    ) -> Path:
        query = result.get("query", "Summary")
        summary = result.get("summary", result.get("message", ""))

        if format == "markdown":
            return self.export_as_markdown(query, summary)
        return self.export_as_text(f"{query}\n\n{summary}")