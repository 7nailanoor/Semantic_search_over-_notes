

"""
FAISS Vector Store Manager

Handles:
- Creating FAISS index
- Adding document embeddings
- Searching similar vectors
- Saving/loading index
- Managing metadata


"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import faiss
import numpy as np

from vector_store.metadata_store import MetadataStore


class FAISSManager:
    """
    Manages FAISS vector database for semantic search.
    """

    def __init__(
        self,
        dimension: int = 384,
        index_path: str = "vector_store/index/faiss.index",
    ):

        self.dimension = dimension

        self.index_path = Path(index_path)

        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        self.metadata_store = MetadataStore()

        if self.index_path.exists():
            self.load()

        else:
            self.index = self._create_index()

    # =====================================================
    # Create Index
    # =====================================================

    def _create_index(self):
        """
        Create FAISS cosine similarity index.

        IndexFlatIP + normalized vectors
        = cosine similarity
        """

        return faiss.IndexFlatIP(self.dimension)

    # =====================================================
    # Add Documents
    # =====================================================

    def add_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Add embedded chunks into FAISS.
        """

        if not chunks:
            return

        vectors = []

        metadata = []

        for chunk in chunks:
            embedding = chunk.get("embedding")

            if embedding is None:
                continue

            vectors.append(embedding)

            metadata.append(
                {
                    "document_id": chunk.get("document_id"),
                    "filename": chunk.get("filename"),
                    "filetype": chunk.get("filetype"),
                    "page": chunk.get("page", 1),
                    "chunk_id": chunk.get("chunk_id"),
                    "section": chunk.get("section", ""),
                    "text": chunk.get("text", ""),
                }
            )

        if not vectors:
            return

        vectors = np.asarray(vectors, dtype=np.float32)

        # Normalize for cosine similarity

        faiss.normalize_L2(vectors)

        self.index.add(vectors)

        self.metadata_store.add(metadata)

    # =====================================================
    # Search
    # =====================================================

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search most similar chunks.
        """

        if self.index.ntotal == 0:
            return []

        query = np.asarray([query_embedding], dtype=np.float32)

        faiss.normalize_L2(query)

        scores, indices = self.index.search(query, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            metadata = self.metadata_store.get(idx)

            if metadata is None:
                continue

            result = metadata.copy()

            result["similarity"] = round(float(score), 4)

            results.append(result)

        return results

    # =====================================================
    # Save
    # =====================================================

    def save(self):
        """
        Save FAISS index and metadata.
        """

        faiss.write_index(self.index, str(self.index_path))

        self.metadata_store.save()

    # =====================================================
    # Load
    # =====================================================

    def load(self):
        """
        Load existing FAISS index.
        """

        self.index = faiss.read_index(str(self.index_path))

        self.metadata_store.load()

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):
        """
        Remove all vectors.
        """

        self.index = self._create_index()

        self.metadata_store.clear()

    # =====================================================
    # Stats
    # =====================================================

    @property
    def total_vectors(self):
        """
        Return number of stored embeddings.
        """

        return self.index.ntotal
