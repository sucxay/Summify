"""
Application-wide constants.
All magic numbers and hardcoded values live here.
"""

# ============================================
# File Handling
# ============================================
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.md', '.docx'}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'text/plain',
    'text/markdown',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
}
MAX_FILE_SIZE_MB = 50
MAX_PAGES_PER_DOCUMENT = 500
UPLOAD_DIR = "storage/uploads"
PROCESSED_DIR = "storage/processed"
EXPORT_DIR = "storage/exports"

# ============================================
# PDF Processing
# ============================================
DPI_FOR_IMAGE_EXTRACTION = 150
HEADING_FONT_THRESHOLD = 14.0  # Font size above which text is considered a heading

# ============================================
# Chunking
# ============================================
CHUNK_SIZE = 1000          # Target words per chunk
CHUNK_OVERLAP = 200        # Overlap words between chunks
MIN_CHUNK_SIZE = 50        # Minimum chunk size before merging with neighbor
MAX_CHUNK_SIZE = 2000      # Absolute maximum chunk size

# ============================================
# Embeddings
# ============================================
EMBEDDING_MODEL_LOCAL = "all-MiniLM-L6-v2"
EMBEDDING_MODEL_OPENAI = "text-embedding-3-small"
EMBEDDING_DIMENSION_LOCAL = 384   # all-MiniLM-L6-v2 dimension
EMBEDDING_DIMENSION_OPENAI = 1536 # text-embedding-3-small dimension
EMBEDDING_BATCH_SIZE = 32         # Batch size for embedding generation

# ============================================
# Vector Store (ChromaDB)
# ============================================
CHROMA_PERSIST_DIR = "chroma_db"
DEFAULT_COLLECTION_NAME = "summify_documents"
TOP_K_DEFAULT = 5                  # Default number of chunks to retrieve
TOP_K_MAX = 20                     # Maximum chunks to retrieve
SIMILARITY_THRESHOLD = 0.6         # Minimum similarity score for retrieval

# ============================================
# LLM
# ============================================
LLM_TIMEOUT_SECONDS = 60
LLM_MAX_RETRIES = 3
LLM_RETRY_DELAY = 1.0              # Initial delay in seconds (exponential backoff)
LLM_TEMPERATURE = 0.3              # Lower = more deterministic summaries
LLM_MAX_TOKENS = 1024              # Max tokens in generated summary

# ============================================
# Summarization
# ============================================
SUMMARY_TYPES = ["general", "executive", "bullet_points", "key_findings", "action_items"]
MAX_CONTEXT_TOKENS = 4000          # Max tokens to send as context to LLM

# ============================================
# Caching
# ============================================
CACHE_TTL_SECONDS = 3600           # 1 hour default cache TTL
EMBEDDING_CACHE_SIZE = 10000       # Max cached embeddings
QUERY_CACHE_SIZE = 1000            # Max cached query results

# ============================================
# API
# ============================================
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "Summify"
PROJECT_VERSION = "0.1.0"
PROJECT_DESCRIPTION = "Document Summarizer with RAG"
RATE_LIMIT_PER_MINUTE = 60

# ============================================
# Logging
# ============================================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"