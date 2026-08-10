"""
High-level service for generating embeddings with caching and batching. 
"""

from typing import Any, List, Optional
from app.embeddings.cache import EmbeddingCache

from app.utils.timers import timeit 

class EmbeddingService:
    """Provides a clean API for embedding text, with optional caching."""

    def __init__(self, embedder: Any, cache: Optional[EmbeddingCache] = None):
        self.embedder  = embedder
        self.cache = cache

    @property
    def dimension(self)-> int:
        return self.embedder.dimension
    

    @timeit
    def embed(self,texts:List[str])->List[List[float]]:

        if not texts:
            return []
        
        if self.cache is None :
            return self.embedder.embed(texts)
        

        results = []
        uncached_texts = []
        uncached_indices = []

        for i,text in enumerate(texts):
            cached = self.cache.get(text)
            if cached is not None:
                results.append(cached)
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
                results.append(None)  # Placeholder for now

        if uncached_texts:
            uncached_embeddings = self.embedder.embed(uncached_texts)
            for idx, embedding in zip(uncached_indices, uncached_embeddings):
                # idx is the position in the original `texts` list
                # map back to the corresponding uncached text using that index
                self.cache.put(texts[idx], embedding)
                results[idx] = embedding

        return results
    
    def embed_single(self,text:str)-> list[float]:
        result= self.embed([text])
        return result[0]
    

    def embed_batch(self,texts:List[str] ,batch_size:int = 32)->list[list[float]]:
        results = []
        for i in range(0,len(texts),batch_size):
            batch = texts[i:i+batch_size]
            batch_results = self.embed(batch)
            results.extend(batch_results)
        return results
    
    def embed_chunks(self, chunks) -> List[List[float]]:
        """
        Embed a list of text chunks, using caching if available.

        Args:
            chunks: List of text chunks to embed
            """

        texts = [chunk.text for chunk in chunks]
        return self.embed(texts)
    

    def get_cache_stats(self) -> Optional[dict]:
        if self.cache:
            return self.cache.stats
        return None
    
    def clear_cache(self) -> None:
        if self.cache:
            self.cache.clear()

            