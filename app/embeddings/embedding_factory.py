"""
Factory to create embeddings services based on configuration .
"""

from app.config.settings import settings
from app.embeddings.minilm import MiniLMEmbedder
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.cache import EmbeddingCache


def create_embedding_service()-> EmbeddingService:
    embedder = MiniLMEmbedder(model_name = settings.EMBEDDING_MODEL , device = 'cpu')

    cache = EmbeddingCache(max_size = 10000)

    return EmbeddingService(embedder = embedder , cache = cache)

