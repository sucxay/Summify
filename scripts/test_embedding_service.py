"""Test the full embedding layer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.embeddings.embedding_factory import create_embedding_service

service = create_embedding_service()
print(f"Service ready. Dimension: {service.dimension}")

texts = [
    "Machine learning is a subset of artificial intelligence.",
    "Python is a popular language for data science.",
    "RAG combines retrieval and generation.",
]

# First call – should be a cache miss
embeddings = service.embed(texts)
print(f"Embedded {len(embeddings)} texts. Each has length {len(embeddings[0])}")

# Second call with same texts – should hit cache
embeddings2 = service.embed(texts)
print(f"Second call done.")

# Check stats
stats = service.get_cache_stats()
if stats:
    print(f"Cache stats: {stats}")

# Test embed_chunks with dummy objects (simulate chunks)
class FakeChunk:
    def __init__(self, text):
        self.text = text

fake_chunks = [FakeChunk(t) for t in texts]
chunk_embeddings = service.embed_chunks(fake_chunks)
print(f"Chunk embeddings: {len(chunk_embeddings)}")