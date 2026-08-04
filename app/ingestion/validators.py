"""
Document validators - file , existence , extension , size , MIME, type , and pdf integrity.
"""

import mimetypes 
from pathlib import Path
from typing import Tuple , Optional 

import fitz 

from app.config.constants import (
    ALLOWED_EXTENSIONS , ALLOWED_MIME_TYPES , MAX_FILE_SIZE_MB  #50mb 
)

from app.exceptions.custom_exceptions import (
    FileNotFoundError , 
    InvalidFileTypeError ,
    FileTooLargeError,
    CorruptedFileError,
    EmptyFileError,
)

class DocumentValidator:
    """
    Comprehensive document validation before processing. 

    validator = DocumentValidator
    validator.validate(Path('document.pdf'))
    """

    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS
    ALLOWED_MIME_TYPES = ALLOWED_MIME_TYPES
    MAX_SIZE_BYTES = MAX_FILE_SIZE_MB*1024*1024

    def validate_file_exists (file_path : Path) -> Path :
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found : {file_path}"
            )
        
        if not file_path.is_file():
            raise FileNotFoundError(
                f"Path is not a file : {file_path}"
            )
        return file_path.resolve()
    
    def validate_file_extension(file_path : Path) -> str : #returns string
        suffix = file_path.suffix.lower() #suffix = .pdf or jpg 

        if not suffix :
            raise InvalidFileTypeError(
                f"File has no extensions : {file_path.name}"
            )
        
        if suffix not in ALLOWED_EXTENSIONS:
            raise InvalidFileTypeError(
                f"Unsupported file type '{suffix}'."
                f"Allowed types: {','.join(sorted(ALLOWED_EXTENSIONS))} " 
            )
        return suffix 

       

    @staticmethod
    def validate_file_size(
        self,
        file_path: Path,
        max_size_bytes: Optional[int] = None,
    ) -> int:
        """Validate file size against maximum allowed size."""
        max_size = (
            max_size_bytes
            if max_size_bytes is not None
            else self.MAX_SIZE_BYTES
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
                f"Maximum allowed size is {max_mb:.2f} MB."
            )

        return file_size

    def validate_mime_type(self, file_path: Path) -> str:
        """Validate file MIME type against allowed MIME types."""
        mime_type, _ = mimetypes.guess_type(file_path)

        if not mime_type:
            raise InvalidFileTypeError(
                f"Could not determine MIME type for file: {file_path.name}"
            )

        if mime_type not in self.ALLOWED_MIME_TYPES:
            raise InvalidFileTypeError(
                f"Unsupported MIME type '{mime_type}'. "
                f"Allowed types: {','.join(sorted(self.ALLOWED_MIME_TYPES))}"
            )

        return mime_type

    def validate_pdf_integrity(self, file_path: Path) -> bool:
        """Validate PDF file integrity using PyMuPDF."""
        try:
            doc = fitz.open(file_path)
            doc.close()
            return True
        except Exception as e:
            raise CorruptedFileError(
                f"PDF file '{file_path.name}' is corrupted: {str(e)}"
            )

    def validate(self, file_path: Path) -> Path:
        """Run all validations on the file."""
        file_path = self.validate_file_exists(file_path)
        self.validate_file_extension(file_path)
        self.validate_file_size(file_path)
        self.validate_mime_type(file_path)

        # Only validate PDF integrity if it's a PDF
        if file_path.suffix.lower() == '.pdf':
            self.validate_pdf_integrity(file_path)

        return file_path
            


