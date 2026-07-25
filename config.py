"""
Application Configuration

Central configuration file for Semantic Search over Notes.

Contains:
- Model configuration
- Chunking settings
- Search settings
- Supported file types
- Application metadata

Author: Naila Noor
Project: Semantic Search over Notes
"""

from pathlib import Path


# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "Semantic Search over Notes"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "AI-powered semantic search across PDF, DOCX and TXT documents "
    "using embeddings and FAISS."
)


# ==========================================================
# Supported Documents
# ==========================================================

SUPPORTED_FILE_TYPES = [
    "pdf",
    "docx",
    "txt",
]


SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".txt",
]


# ==========================================================
# Embedding Model Configuration
# ==========================================================

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


EMBEDDING_DIMENSION = 384


# ==========================================================
# Text Chunking Configuration
# ==========================================================

CHUNK_SIZE = 200

CHUNK_OVERLAP = 40


# ==========================================================
# Semantic Search Configuration
# ==========================================================

DEFAULT_TOP_K = 5

MAX_TOP_K = 10


# Number of FAISS candidates before ranking

FAISS_SEARCH_K = 20


# ==========================================================
# Similarity Configuration
# ==========================================================

SIMILARITY_THRESHOLD = 0.30


# ==========================================================
# Ranking Weights
# ==========================================================

SEMANTIC_WEIGHT = 0.75

KEYWORD_WEIGHT = 0.20

LENGTH_WEIGHT = 0.05


# ==========================================================
# Upload Configuration
# ==========================================================

MAX_FILE_SIZE_MB = 100


# ==========================================================
# Directory Configuration
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent


DATA_DIR = BASE_DIR / "data"


UPLOAD_DIR = DATA_DIR / "uploaded_files"


EXTRACTED_TEXT_DIR = DATA_DIR / "extracted_text"


VECTOR_STORE_DIR = BASE_DIR / "vector_store" / "index"


LOG_DIR = BASE_DIR / "logs"


# ==========================================================
# UI Configuration
# ==========================================================

PAGE_TITLE = "Semantic Search over Notes"

PAGE_ICON = "📚"

LAYOUT = "wide"


# ==========================================================
# Logging Configuration
# ==========================================================

LOG_FILE = LOG_DIR / "semantic_search.log"

LOG_LEVEL = "INFO"
