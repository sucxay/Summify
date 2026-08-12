"""
Streaming utilities for LLM responses.
"""
from typing import Generator, Optional, Callable
import asyncio
import logging

logger = logging.getLogger(__name__)


class StreamHandler:
    def __init__(self, on_token: Optional[Callable] = None):
        self.on_token = on_token
        self.accumulated_text = ""

    def process_stream(self, token_stream: Generator[str, None, None]) -> str:
        for token in token_stream:
            self.accumulated_text += token
            if self.on_token:
                self.on_token(token)
        return self.accumulated_text

    def reset(self):
        self.accumulated_text = ""


async def async_stream_wrapper(
    token_stream: Generator[str, None, None],
    on_token: Optional[Callable] = None,
) -> str:
    accumulated = ""
    for token in token_stream:
        accumulated += token
        if on_token:
            await on_token(token) if asyncio.iscoroutinefunction(on_token) else on_token(token)
    return accumulated


def create_sse_response(token_generator: Generator[str, None, None]):
    for token in token_generator:
        yield f"data: {token}\n\n"
    yield "data: [DONE]\n\n"