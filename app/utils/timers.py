"""
Timing utilities for measuring function execution time.
"""
import time
import functools
import logging

logger = logging.getLogger(__name__)


def timeit(func):
    """
    Decorator that logs the execution time of a function.

    Usage:
        @timeit
        def my_function():
            pass

    The log level is DEBUG, so it won't clutter your console
    unless you set logging to DEBUG.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(
            f"{func.__name__} completed in {elapsed:.4f} seconds"
        )
        return result
    return wrapper