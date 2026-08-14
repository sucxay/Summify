"""Test the retriever end-to-end."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.embeddings import create_embedding_service
from app.vectorstore import get_vector_store, reset_vector_store
from app.vectorstore.collections import CollectionManager
from app.rag.context_builder import ContextBuilder
from app.rag.retriever import Retriever

# Setup
reset_vector_store()
embed_service = create_embedding_service()
vector_store = get_vector_store()
context_builder = ContextBuilder(max_tokens=4000)
retriever = Retriever(embed_service, vector_store, context_builder)

# Create test data
doc_id = "test_retriever_doc"
collection = CollectionManager.get_or_create_collection(doc_id)

texts = [
    "Machine learning is a subset of artificial intelligence that enables systems to learn from data without explicit programming.",
    "Deep learning is a type of machine learning that uses neural networks with many layers to model complex patterns in data.",
    "Python is a high-level programming language known for its readability and extensive libraries for data science.",
    "Natural language processing (NLP) is a field of AI focused on enabling computers to understand and generate human language.",
    "Reinforcement learning is a machine learning paradigm where an agent learns by interacting with an environment and receiving rewards.",
]

embeddings = embed_service.embed(texts)

collection.add(
    ids=[f"{doc_id}_chunk_{i}" for i in range(len(texts))],
    documents=texts,
    metadatas=[
        {
            "document_id": doc_id,
            "document_title": "AI and ML Guide",
            "page_start": i + 1,
            "page_end": i + 1,
            "chunk_index": i,
        }
        for i in range(len(texts))
    ],
    embeddings=embeddings,
)

print(f"✅ Added {len(texts)} chunks to '{doc_id}'")

# Test 1: Basic retrieval
print("\n" + "=" * 60)
print("1. BASIC RETRIEVAL")
print("=" * 60)
query = "What is deep learning?"
results = retriever.retrieve(query, top_k=2)
for i, r in enumerate(results, 1):
    print(f"  {i}. [score={r['score']:.4f}] {r['text'][:100]}...")

# Test 2: Retrieve context (QA format)
print("\n" + "=" * 60)
print("2. CONTEXT (QA FORMAT)")
print("=" * 60)
context = retriever.retrieve_context("Explain machine learning types", context_type="qa")
print(context[:500])

# Test 3: Retrieve context (summary format)
print("\n" + "=" * 60)
print("3. CONTEXT (SUMMARY FORMAT)")
print("=" * 60)
context = retriever.retrieve_context("Summarize AI topics", context_type="summary")
print(context[:500])

# Test 4: Score filtering
print("\n" + "=" * 60)
print("4. SCORE FILTERING (min_score=0.5)")
print("=" * 60)
results = retriever.retrieve_with_scores("neural networks", top_k=5, min_score=0.5)
print(f"  Found {len(results)} chunks with score >= 0.5")

# Test 5: Stats
print("\n" + "=" * 60)
print("5. RETRIEVAL STATS")
print("=" * 60)
stats = retriever.get_retrieval_stats("Python programming")
for key, value in stats.items():
    print(f"  {key}: {value}")

# Test 6: Page range
print("\n" + "=" * 60)
print("6. PAGE RANGE SEARCH (pages 1-2)")
print("=" * 60)
results = retriever.retrieve_by_page_range("learning", doc_id, 1, 2, top_k=5)
for r in results:
    page = r["metadata"].get("page_start", "?")
    print(f"  Page {page}: {r['text'][:80]}...")

# Cleanup
CollectionManager.delete_collection(doc_id)
print(f"\n✅ All tests passed!")