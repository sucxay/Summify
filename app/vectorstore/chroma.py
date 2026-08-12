import chromadb
from chromadb.config import Settings as ChromaSettings
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

class ChromaClient:
    """Singleton client for ChromaDB persistent storage."""
    _client = None

    @classmethod
    def get_client(cls):
        """
        Get a persistent ChromaDB client.

        Returns:
            ChromaDB PersistentClient instance

        Raises:
            RuntimeError: If client initialization fails
        """
        if cls._client is None:
            try:
                cls._client = chromadb.PersistentClient(
                    path=str(settings.CHROMA_DB_PATH),
                    settings=ChromaSettings(anonymized_telemetry=False)
                )
                logger.info('ChromaDB client initialized at %s', settings.CHROMA_DB_PATH)
                return cls._client
            except Exception as e:
                logger.error('Failed to initialize ChromaDB client: %s', e)
                raise RuntimeError(f'ChromaDB initialization failed: {e}')

        return cls._client

    @classmethod
    def reset(cls) -> None:
        """Reset the ChromaDB client singleton."""
        cls._client = None
        logger.warning('ChromaDB client reset.')

