"""
Free/local LLM API client using llama-cpp-python or Ollama.
"""
from typing import Optional, Dict, Any, Generator
import logging

from app.llm.models import LLMConfig, LLMResponse, ChatMessage, ChatResponse

logger = logging.getLogger(__name__)


class FreeLLMAPI:
    def __init__(self, config: LLMConfig):
        self.config = config
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._initialize_client()
        return self._client

    def _initialize_client(self):
        try:
            import openai
            self._client = openai.OpenAI(
                base_url=self.config.base_url or "http://localhost:1234/v1",
                api_key=self.config.api_key or "not-needed",
            )
            self._client_type = "openai_compatible"
            logger.info(f"Initialized OpenAI-compatible client: {self.config.base_url}")
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            raise

    def complete(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        try:
            response = self.client.completions.create(
                model=self.config.model,
                prompt=prompt,
                temperature=temperature or self.config.temperature,
                max_tokens=max_tokens or self.config.max_tokens,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logger.error(f"Completion failed: {e}")
            return f"Error generating response: {str(e)}"

    def chat(
        self,
        messages: list,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> ChatResponse:
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature or self.config.temperature,
                max_tokens=max_tokens or self.config.max_tokens,
            )
            return ChatResponse(
                message=ChatMessage(
                    role=response.choices[0].message.role,
                    content=response.choices[0].message.content,
                ),
                finish_reason=response.choices[0].finish_reason,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            )
        except Exception as e:
            logger.error(f"Chat failed: {e}")
            return ChatResponse(
                message=ChatMessage(role="assistant", content=f"Error: {str(e)}")
            )

    def stream_complete(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Generator[str, None, None]:
        try:
            stream = self.client.completions.create(
                model=self.config.model,
                prompt=prompt,
                temperature=temperature or self.config.temperature,
                max_tokens=max_tokens or self.config.max_tokens,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].text:
                    yield chunk.choices[0].text
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield f"Error: {str(e)}"