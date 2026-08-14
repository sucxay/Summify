# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Summify is a backend service for document processing and summarization. It includes functionality for document ingestion, embedding generation, vector storage, and LLM interactions.

## Common Commands

### Development Environment

1. Set up virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app/main.py
   ```

### Testing

1. Run all tests:
   ```bash
   python -m pytest tests/
   ```

2. Run a specific test file:
   ```bash
   python -m pytest tests/test_embedding_service.py
   ```

3. Run tests with coverage:
   ```bash
   python -m pytest --cov=app tests/
   ```

### Document Processing Scripts

1. Ingest documents:
   ```bash
   python scripts/ingest_documents.py
   ```

2. Test embedding service:
   ```bash
   python scripts/test_embedding_service.py
   ```

3. Benchmark performance:
   ```bash
   python scripts/benchmark.py
   ```

4. Reset database:
   ```bash
   python scripts/reset_database.py
   ```

## Code Architecture

### Core Components

1. **Ingestion Pipeline** (`app/ingestion/`):
   - Document loading (PDF, text)
   - Text cleaning and normalization
   - Document chunking
   - Metadata extraction

2. **Embedding Service** (`app/embeddings/`):
   - Generates vector embeddings for document chunks
   - Supports multiple embedding models
   - Caching layer for efficiency

3. **Vector Store** (`app/vectorstore/`):
   - Persistence layer for embeddings
   - Uses ChromaDB for vector storage
   - Similarity search functionality

4. **LLM Integration** (`app/llm/`):
   - Manages interactions with language models
   - Supports multiple LLM providers
   - Handles streaming responses

5. **Database** (`app/database/`):
   - SQLAlchemy models and session management
   - Document and chunk storage

6. **API Layer** (`app/main.py`):
   - FastAPI application entry point
   - Route definitions and request handling

## Key Data Flows

1. **Document Ingestion**:
   `PDF/Text File → Loader → Cleaner → Chunker → Metadata Extraction → Storage`

2. **Embedding Generation**:
   `Document Chunk → Embedding Model → Vector Store → Similarity Search`

3. **Query Processing**:
   `User Query → Embedding → Similarity Search → Context Retrieval → LLM Response`

## Important Configuration

1. Environment variables (see `.env.example`):
   - Database connection strings
   - LLM API keys
   - Embedding model configuration
   - ChromaDB settings

2. Vector store persistence:
   - ChromaDB data is stored in `chroma_db/` directory
   - Configuration in `app/vectorstore/persistence.py`

## Development Notes

1. The project uses:
   - FastAPI for the web framework
   - SQLAlchemy for database ORM
   - ChromaDB for vector storage
   - Pydantic for data validation

2. Key patterns:
   - Factory pattern for embedding model selection
   - Repository pattern for data access
   - Dependency injection for services

3. Testing:
   - Unit tests for individual components
   - Integration tests for data flows
   - Benchmark scripts for performance testing