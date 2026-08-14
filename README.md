# Summify

Summify is a backend service for document processing and summarization. It provides document ingestion, chunking, embedding generation, vector storage, and LLM-powered summarization and query handling. The project is implemented primarily in Python with supporting TypeScript components.

Key features

- Document ingestion (PDF and text)
- Text cleaning, normalization, and chunking
- Embedding generation with support for multiple models and a caching layer
- Persistent vector store (ChromaDB) and similarity search
- LLM integration with support for multiple providers and streaming responses
- FastAPI-based API and scripts for common tasks (ingestion, testing, benchmarking)

Language composition

- Python (~63%) — core backend services, ingestion, embeddings, database models, and API
- TypeScript (~35%) — supporting tools and frontend-related utilities (if present)

Quick start

Prerequisites

- Python 3.10+ (or the project's required Python version)
- Git
- (Optional) Node.js and npm/yarn if you need to run TypeScript tools

1. Clone the repository

```bash
git clone https://github.com/sucxay/Summify.git
cd Summify
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment

Copy the example environment file and fill in the required values:

```bash
cp .env.example .env
# Edit .env and provide your DB connection, LLM API keys, embedding model settings, etc.
```

Important environment variables (examples)

- DATABASE_URL — SQLAlchemy-compatible database connection string
- LLM_API_KEY — API key for your LLM provider
- EMBEDDING_MODEL — embedding model identifier or name
- CHROMA_DB_DIR — path where ChromaDB should persist data (defaults to `chroma_db/`)

Run the application

```bash
python app/main.py
```

API

The project uses FastAPI as the web framework. The main application entrypoint is `app/main.py`. When running locally, the FastAPI server exposes endpoints for ingestion, query, and management of vector stores.

Project structure (high level)

- app/
  - ingestion/ — loaders, cleaners, chunkers, metadata extraction
  - embeddings/ — embedding model factories, caching, and model adapters
  - vectorstore/ — ChromaDB integrations and persistence configuration
  - llm/ — LLM provider adapters, streaming, and prompt orchestration
  - database/ — SQLAlchemy models, sessions, and migrations
  - main.py — FastAPI application and route definitions
- scripts/ — helper scripts for ingestion, testing, benchmarking, and database reset
- tests/ — unit and integration tests
- chroma_db/ — default persistence directory for ChromaDB (created at runtime)

Common commands

Development environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

Testing

```bash
python -m pytest tests/
python -m pytest tests/test_embedding_service.py
python -m pytest --cov=app tests/
```

Document-processing scripts

```bash
python scripts/ingest_documents.py
python scripts/test_embedding_service.py
python scripts/benchmark.py
python scripts/reset_database.py
```

Configuration notes

- ChromaDB persistence is configured in `app/vectorstore/persistence.py`. By default data is stored under `chroma_db/` in the repository root — consider mounting or moving this for production.
- Keep LLM API keys and database credentials out of source control. Use `.env` and your platform's secret management.

Testing and CI

- Unit tests live in `tests/`. The project uses pytest.
- Add CI configuration (GitHub Actions) as needed to run linting, tests, and coverage.

Contributing

Contributions are welcome. Typical workflow:

1. Fork the repository
2. Create a feature branch
3. Add tests for new behavior
4. Open a pull request describing your change

Please follow existing code style and add tests where appropriate.

License

This repository does not include an explicit license file. If you want to add one, consider adding an OSI-approved license such as MIT or Apache-2.0.

Contact

For questions or help, open an issue in the repository or reach out to the maintainers.
