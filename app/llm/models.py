"""
LLM models and data structures.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    LOCAL = "local"


@dataclass
class LLMConfig:
    provider: LLMProvider = LLMProvider.LOCAL
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0.3
    max_tokens: int = 1024
    timeout: int = 60
    max_retries: int = 3
    api_key: Optional[str] = None
    base_url: Optional[str] = None


@dataclass
class LLMResponse:
    text: str
    model: str = ""
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatRequest:
    messages: List[ChatMessage]
    temperature: float = 0.3
    max_tokens: int = 1024


@dataclass
class ChatResponse:
    message: ChatMessage
    finish_reason: str = ""
    usage: Dict[str, int] = field(default_factory=dict)