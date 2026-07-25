"""
Application Settings

Central configuration for the Semantic Search project.

"""

from pathlib import Path


class Settings:
    """
    Application configuration.
    """

    # ======================================================
    # Project
    # ======================================================

    PROJECT_NAME = "Semantic Search over Notes"

    VERSION = "1.0.0"

    DEBUG = False

    # ======================================================
    # Paths
    # ======================================================

    BASE_DIR = Path(__file__).resolve().parent

    DATA_DIR = BASE_DIR / "data"

    UPLOAD_DIR = DATA_DIR / "uploaded_files"

    EXTRACTED_TEXT_DIR = DATA_DIR / "extracted_text"

    VECTOR_STORE_DIR = BASE_DIR / "vector_store" / "index"

    LOG_DIR = BASE_DIR / "logs"

    ASSETS_DIR = BASE_DIR / "assets"

    CSS_FILE = ASSETS_DIR / "styles.css"

    LOGO_FILE = ASSETS_DIR / "logo.png"

    BANNER_FILE = ASSETS_DIR / "banner.png"

    # ======================================================
    # Embedding Model
    # ======================================================

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    EMBEDDING_DIMENSION = 384

    # ======================================================
    # Chunking
    # ======================================================

    CHUNK_SIZE = 200

    CHUNK_OVERLAP = 40

    # ======================================================
    # Search
    # ======================================================

    DEFAULT_TOP_K = 5

    MAX_TOP_K = 10

    FAISS_CANDIDATES = 20

    # ======================================================
    # Upload
    # ======================================================

    MAX_FILE_SIZE_MB = 100

    ALLOWED_EXTENSIONS = [
        ".pdf",
        ".docx",
        ".txt",
    ]

    # ======================================================
    # UI
    # ======================================================

    PAGE_TITLE = "Semantic Search"

    PAGE_ICON = "📚"

    LAYOUT = "wide"

    INITIAL_SIDEBAR_STATE = "expanded"

    # ======================================================
    # Logging
    # ======================================================

    LOG_LEVEL = "INFO"

    LOG_FILE = LOG_DIR / "semantic_search.log"

    # ======================================================
    # Create Required Directories
    # ======================================================

    @classmethod
    def initialize(cls):
        """
        Create required directories if they don't exist.
        """

        directories = [
            cls.DATA_DIR,
            cls.UPLOAD_DIR,
            cls.EXTRACTED_TEXT_DIR,
            cls.VECTOR_STORE_DIR,
            cls.LOG_DIR,
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )
