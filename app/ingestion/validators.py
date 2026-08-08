"""
Document validators - file existence, extension, size, MIME type, and PDF integrity.
"""

import mimetypes
from pathlib import Path
from typing import Tuple, Optional

import fitz

from app.config.constants import (
    ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    MAX_FILE_SIZE_MB,  # 50MB
)

from app.exceptions.custom_exceptions import (
    FileNotFoundError,
    InvalidFileTypeError,
    FileTooLargeError,
    CorruptedFileError,
    EmptyFileError,
)


class DocumentValidator:
    """
    Comprehensive document validation before processing.

    Usage:
        validator = DocumentValidator()
        validator.validate(Path('document.pdf'))
    """

    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS
    ALLOWED_MIME_TYPES = ALLOWED_MIME_TYPES
    MAX_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

    @staticmethod
    def validate_file_exists(file_path: Path) -> Path:
        """Check if file exists and is a file (not directory)."""
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Path is not a file: {file_path}"
            )

        return file_path.resolve()

    @staticmethod
    def validate_file_extension(file_path: Path) -> str:
        """Check if file extension is supported."""
        suffix = file_path.suffix.lower()

        if not suffix:
            raise InvalidFileTypeError(
                f"File has no extension: {file_path.name}"
            )

        if suffix not in ALLOWED_EXTENSIONS:
            raise InvalidFileTypeError(
                f"Unsupported file type '{suffix}'. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        return suffix

    @staticmethod
    def validate_file_size(
        file_path: Path,
        max_size_bytes: Optional[int] = None,
    ) -> int:
        """Check file size is within limits."""
        max_size = (
            max_size_bytes
            if max_size_bytes is not None
            else DocumentValidator.MAX_SIZE_BYTES
        )

        try:
            file_size = file_path.stat().st_size
        except OSError as e:
            raise FileNotFoundError(
                f"Cannot read file stats: {e}"
            )

        if file_size == 0:
            raise EmptyFileError(
                f"File '{file_path.name}' is empty."
            )

        if file_size > max_size:
            size_mb = file_size / (1024 * 1024)
            max_mb = max_size / (1024 * 1024)

            raise FileTooLargeError(
                f"File '{file_path.name}' is {size_mb:.2f} MB. "
                f"Maximum allowed size is {max_mb:.0f} MB."
            )

        return file_size

    @staticmethod
    def validate_mime_type(file_path: Path) -> str:
        """Detect and validate MIME type of file."""
        mime_type, _ = mimetypes.guess_type(str(file_path))

        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
        except OSError as e:
            raise CorruptedFileError(f"Cannot read file: {e}")

        # Check PDF signature
        if file_path.suffix.lower() == '.pdf':
            if not header.startswith(b'%PDF-'):
                raise CorruptedFileError(
                    f"File has .pdf extension but does not appear to be a valid PDF."
                )
            mime_type = 'application/pdf'

        # Check text files
        elif file_path.suffix.lower() in ['.txt', '.md']:
            if b'\x00' in header:
                raise CorruptedFileError(
                    f"File appears to be binary, not text."
                )
            if mime_type is None:
                mime_type = 'text/plain'

        # Check DOCX signature
        elif file_path.suffix.lower() == '.docx':
            if header[:2] != b'PK':
                raise CorruptedFileError(
                    f"File has .docx extension but doesn't appear to be a valid DOCX."
                )
            mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

        # Check if we got a valid MIME type
        if mime_type is None:
            raise CorruptedFileError(
                f"Could not determine MIME type for: {file_path.name}"
            )

        # Validate against allowed types
        if mime_type not in ALLOWED_MIME_TYPES:
            raise InvalidFileTypeError(
                f"Unsupported MIME type '{mime_type}'. "
                f"Allowed: {', '.join(sorted(ALLOWED_MIME_TYPES))}"
            )

        return mime_type

    @staticmethod
    def validate_pdf_readable(file_path: Path) -> dict:
        """Verify PDF can be opened and read by PyMuPDF."""
        if file_path.suffix.lower() != '.pdf':
            return {"page_count": 0, "is_encrypted": False}

        doc = None
        try:
            doc = fitz.open(str(file_path))

            if doc.is_encrypted:
                raise CorruptedFileError(
                    "PDF is encrypted/password-protected. "
                    "Cannot process encrypted documents."
                )

            page_count = doc.page_count
            if page_count == 0:
                raise CorruptedFileError("PDF has no pages.")

            # Try reading first page to verify content is accessible
            try:
                first_page = doc[0]
                _ = first_page.get_text("text")
            except Exception:
                raise CorruptedFileError(
                    "PDF pages exist but content cannot be read. "
                    "The file may be scanned images only or corrupted."
                )

            return {
                "page_count": page_count,
                "is_encrypted": False,
            }

        except fitz.FileDataError as e:
            raise CorruptedFileError(f"PDF is corrupted or malformed: {e}")
        except Exception as e:
            raise CorruptedFileError(f"PDF validation failed: {e}")
        finally:
            if doc:
                doc.close()

    @classmethod
    def validate(
        cls,
        file_path: Path,
        check_pdf: bool = True,
    ) -> dict:
        """
        Run all validations in sequence.

        Returns dict with validation results.
        """
        result = {"is_valid": False}

        # 1. Existence
        absolute_path = cls.validate_file_exists(file_path)
        result["path"] = str(absolute_path)

        # 2. Extension
        extension = cls.validate_file_extension(absolute_path)
        result["extension"] = extension

        # 3. Size
        size_bytes = cls.validate_file_size(absolute_path)
        result["size_bytes"] = size_bytes
        result["size_mb"] = round(size_bytes / (1024 * 1024), 2)

        # 4. MIME Type
        mime_type = cls.validate_mime_type(absolute_path)
        result["mime_type"] = mime_type

        # 5. PDF-specific checks
        if check_pdf and extension == '.pdf':
            pdf_info = cls.validate_pdf_readable(absolute_path)
            result.update(pdf_info)

        result["is_valid"] = True
        return result