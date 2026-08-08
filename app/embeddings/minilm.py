"""
Local embedding implementations for Summify. (all-MiniLM-L6-v2 model)
"""

from typing import List
from sentence_transformers import SentenceTransformer
from app.config.settings import settings


class MiniLMEmbedder:
    """
    Local embedding model using SentenceTransformers.

    Model: all-MiniLM-L6-v2
    Dimension: 384
    Max tokens: 256 (model limit)

    Usage:
        embedder = MiniLMEmbedder()
        vectors = embedder.embed(["text one", "text two"])
    """

    def __init__(self, model_name: str = None, device: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.device = device or settings.EMBEDDING_DEVICE
        self._model = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy load the model on first use."""
        if self._model is None:
            self._model = SentenceTransformer(
                self.model_name, device=self.device
            )
        return self._model

    @property
    def dimension(self) -> int:
        """Dimension of the embedding vectors (384 for MiniLM)."""
        return self.model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of strings to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def embed_single(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: String to embed

        Returns:
            Embedding vector
        """
        if not text:
            return []

        embeddings = self.model.encode(
            [text],
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings[0].tolist()

    def embed_batch(
        self, texts: List[str], batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings with explicit batch size.

        Args:
            texts: List of strings to embed
            batch_size: Number of texts per batch

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            batch_size=batch_size,
        )

        return embeddings.tolist()

    def __repr__(self) -> str:
        return (
            f"MiniLMEmbedder("
            f"model_name={self.model_name}, "
            f"device={self.device})"
        )