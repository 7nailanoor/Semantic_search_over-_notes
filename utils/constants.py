"""
Project Constants

"""

from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

UPLOAD_DIR = DATA_DIR / "uploaded_files"

EXTRACTED_TEXT_DIR = DATA_DIR / "extracted_text"

VECTOR_INDEX_DIR = PROJECT_ROOT / "vector_store" / "index"

METADATA_FILE = DATA_DIR / "metadata.json"

# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_FILE_TYPES = [".pdf", ".docx", ".txt"]

# ==========================================================
# Embedding Model
# ==========================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ==========================================================
# Chunking
# ==========================================================

CHUNK_SIZE = 200

CHUNK_OVERLAP = 40

# ==========================================================
# Search
# ==========================================================

DEFAULT_TOP_K = 5

FAISS_SEARCH_MULTIPLIER = 3

# ==========================================================
# UI
# ==========================================================

MAX_UPLOAD_SIZE_MB = 100

APP_TITLE = "Semantic Search over Notes"

APP_ICON = "📚"
