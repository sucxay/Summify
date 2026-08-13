"""
LLM Client - Main interface for all LLM interactions.
"""

from typing import Optional, Generator, Any
import logging

from openai import OpenAI

from app.llm.models import LLMConfig
from app.llm.prompts import get_system_prompt
from app.config.settings import settings
from app.config.constants import (
    LLM_TIMEOUT_SECONDS,
    LLM_MAX_RETRIES,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
)
from app.utils.timers import timeit

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig(
            model=settings.MODEL_NAME,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            timeout=LLM_TIMEOUT_SECONDS,
            max_retries=LLM_MAX_RETRIES,
            base_url=getattr(settings, "OPENAI_BASE_URL", None),
            api_key=getattr(settings, "OPENAI_API_KEY", None),
        )

        self._backend = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
        )

    @timeit
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a completion using the configured OpenAI-compatible API.
        """

        sys_prompt = system_prompt or get_system_prompt("local")

        response = self._backend.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "system",
                    "content": sys_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=(
                temperature
                if temperature is not None
                else self.config.temperature
            ),
            max_tokens=(
                max_tokens
                if max_tokens is not None
                else self.config.max_tokens
            ),
        )

        return response.choices[0].message.content or ""

    @timeit
    def chat(
        self,
        messages: list,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Any:
        """
        Send a chat completion using the configured OpenAI-compatible API.
        """

        sys_prompt = system_prompt or get_system_prompt("local")

        full_messages = [
            {
                "role": "system",
                "content": sys_prompt,
            }
        ] + messages

        response = self._backend.chat.completions.create(
            model=self.config.model,
            messages=full_messages,
            temperature=(
                temperature
                if temperature is not None
                else self.config.temperature
            ),
            max_tokens=(
                max_tokens
                if max_tokens is not None
                else self.config.max_tokens
            ),
        )

        return response

    def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Generator[str, None, None]:
        """
        Stream a completion token-by-token.
        """

        sys_prompt = system_prompt or get_system_prompt("local")

        stream = self._backend.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "system",
                    "content": sys_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=(
                temperature
                if temperature is not None
                else self.config.temperature
            ),
            max_tokens=(
                max_tokens
                if max_tokens is not None
                else self.config.max_tokens
            ),
            stream=True,
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def generate_with_context(
        self,
        context: str,
        query: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate an answer using retrieved RAG context.
        """

        prompt = (
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Answer:"
        )

        return self.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            **kwargs,
        )