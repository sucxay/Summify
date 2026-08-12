"""
LLM Client - Main interface for all LLM interactions.
"""
from typing import Optional, Dict, Any, Generator
import logging

from app.llm.models import LLMConfig, LLMResponse, ChatMessage, ChatResponse
from app.llm.freellmapi import FreeLLMAPI
from app.llm.prompts import get_system_prompt
from app.config.settings import settings
from app.config.constants import LLM_TIMEOUT_SECONDS, LLM_MAX_RETRIES, LLM_TEMPERATURE, LLM_MAX_TOKENS
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
            base_url=getattr(settings, 'OPENAI_BASE_URL', None),
            api_key=getattr(settings, 'OPENAI_API_KEY', None),
        )
        self._backend = None

    @property
    def backend(self):
        if self._backend is None:
            self._backend = FreeLLMAPI(self.config)
        return self._backend

    @timeit
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        sys_prompt = system_prompt or get_system_prompt("local")
        full_prompt = f"{sys_prompt}\n\n{prompt}"

        return self.backend.complete(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    @timeit
    def chat(
        self,
        messages: list,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> ChatResponse:
        sys_prompt = system_prompt or get_system_prompt("local")
        full_messages = [{"role": "system", "content": sys_prompt}] + messages

        return self.backend.chat(
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Generator[str, None, None]:
        sys_prompt = system_prompt or get_system_prompt("local")
        full_prompt = f"{sys_prompt}\n\n{prompt}"

        yield from self.backend.stream_complete(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def generate_with_context(
        self,
        context: str,
        query: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        return self.complete(prompt=prompt, system_prompt=system_prompt, **kwargs)