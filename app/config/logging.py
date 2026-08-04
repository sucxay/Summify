"""
Structured logging configuration.
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from loguru import logger


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    json_format: bool = False,
):
    """
    Configure logging for the application.

    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        json_format: Use JSON format (better for production log aggregation)
    """
    # Remove default handler
    logger.remove()

    # Console handler (colored for development)
    if not json_format:
        logger.add(
            sys.stderr,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            level=log_level,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
    else:
        # JSON format for production (parseable by log aggregators)
        logger.add(
            sys.stderr,
            format="{time} {level} {name} {function} {line} {message}",
            level=log_level,
            serialize=True,  # JSON output
        )

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            rotation="10 MB",      # Rotate when file reaches 10MB
            retention="7 days",    # Keep logs for 7 days
            compression="gz",      # Compress rotated logs
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level=log_level,
        )

    # Intercept standard library logging
    logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)

    # Silence noisy libraries
    for lib in ["chromadb", "sentence_transformers", "httpx", "urllib3"]:
        logging.getLogger(lib).setLevel(logging.WARNING)

    logger.info(f"Logging configured: level={log_level}, file={log_file}")
    
    return logger


class _InterceptHandler(logging.Handler):
    """Redirects standard logging to loguru."""

    def emit(self, record: logging.LogRecord):
        # Get corresponding loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the log originated
        frame = logging.currentframe()
        depth = 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )