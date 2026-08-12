import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Determine the absolute path to the backend directory
# This works regardless of where the script is run from
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    """
    Central configuration for the entire application.
    Values are loaded from backend/.env.
    """

    # =========================
    # Application
    # =========================
    APP_NAME: str = "Summify"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # =========================
    # Storage
    # =========================
    UPLOAD_DIR: str = "app/storage/uploads"
    PROCESSED_DIR: str = "app/storage/processed"
    EXPORT_DIR: str = "app/storage/exports"

    # =========================
    # PDF Chunking
    # =========================
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    # =========================
    # Embeddings
    # =========================
    EMBEDDING_MODEL: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    NORMALIZE_EMBEDDINGS: bool = True

    # =========================
    # ChromaDB
    # =========================
    CHROMA_DB_PATH: str = str(BACKEND_DIR / "chroma_db")
    CHROMA_COLLECTION: str = "summify_documents"

    # =========================
    # LLM
    # =========================
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    MODEL_NAME: str = "auto"

    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_TOKENS: int = 4096
    LLM_TIMEOUT: int = 60
    LLM_MAX_RETRIES: int = 3

    # =========================
    # Retrieval
    # =========================
    RETRIEVAL_K: int = 5

    # =========================
    # LangSmith
    # =========================
    LANGCHAIN_API_KEY: str
    LANGCHAIN_PROJECT: str = "Summify"

    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding='utf-8',
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()