from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # =========================
    # ChromaDB
    # =========================
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION: str = "summify_documents"

    # =========================
    # LLM
    # =========================
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str

    MODEL_NAME: str = "auto"

    TEMPERATURE: float = 0.2
    MAX_TOKENS: int = 4096

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
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()