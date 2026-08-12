"""
Base service class providing common functionality such as logging and error handling.
"""

import logging
from abc import ABC
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T")


class BaseService(ABC):
    """Abstract base class for all service classes.

    Provides a logger instance scoped to the subclass name and common error handling.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle_exceptions(self, func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator to standardize error handling across services.
        Converts unexpected exceptions into ServiceException while preserving traceback.
        """
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return cast(T, func(*args, **kwargs))
            except ServiceException:
                # Re-raise our own exceptions
                raise
            except Exception as exc:
                self.logger.exception(f"Error in {func.__name__}: {exc}")
                raise ServiceException(f"Service error: {exc}") from exc
        return wrapper


class ServiceException(Exception):
    """Base class for all service-layer exceptions."""

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(message)
        self.details = details