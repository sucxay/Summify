"""
Caching layer for embeddings to avoid redundant computations and improve performance.
"""

import hashlib
from collections import OrderedDict
from typing import List , Optional 

class EmbeddingCache :
    def __init__(self,max_size:int = 10000):
        self.max_size = max_size

        self.cache : OrderedDict[str, List[float]] = OrderedDict()

        self._hits = 0
        self._misses = 0

    @staticmethod
    def _hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    
    def get(self, text: str) -> Optional[List[float]]:
        key = self._hash(text)
        if key in self.cache:
            self.cache.move_to_end(key)
            self._hits += 1
            return self.cache[key]
        self._misses += 1
        return None
    

    def put(self, text: str, embedding: List[float]) -> None:
        key = self._hash(text)
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = embedding
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def clear(self) -> None:
        self.cache.clear()
        self._hits = 0
        self._misses = 0

    @property
    def size(self) -> int:
        return len(self.cache)
    

    @property
    def stats(self)->dict:
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0.0
        return {
            "size": self.size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
        }
    

