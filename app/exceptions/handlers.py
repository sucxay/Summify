"""
FastAPI exception handlers for custom exceptions.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import (
    SummifyException,
    FileNotFoundError,
    InvalidFileTypeError,
    FileTooLargeError,
    EmptyFileError,
    CorruptedFileError,
    DocumentProcessingError,
)


def setup_exception_handlers(app):
    """Register all exception handlers with the FastAPI app."""

    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(request: Request, exc: FileNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "error": "file_not_found",
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(InvalidFileTypeError)
    async def invalid_file_type_handler(request: Request, exc: InvalidFileTypeError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_file_type",
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(FileTooLargeError)
    async def file_too_large_handler(request: Request, exc: FileTooLargeError):
        return JSONResponse(
            status_code=413,
            content={
                "error": "file_too_large",
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(EmptyFileError)
    async def empty_file_handler(request: Request, exc: EmptyFileError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "empty_file",
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(CorruptedFileError)
    async def corrupted_file_handler(request: Request, exc: CorruptedFileError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "corrupted_file",
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(DocumentProcessingError)
    async def processing_error_handler(request: Request, exc: DocumentProcessingError):
        return JSONResponse(
            status_code=500,
            content={
                "error": "processing_error",
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(SummifyException)
    async def general_summify_handler(request: Request, exc: SummifyException):
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Catch-all for unexpected errors."""
        return JSONResponse(
            status_code=500,
            content={
                "error": "unexpected_error",
                "message": "An unexpected error occurred",
                "detail": {"exception_type": type(exc).__name__},
            },
        )