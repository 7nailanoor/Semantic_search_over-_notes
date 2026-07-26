"""
Semantic Search Pipeline

Performs semantic search using:

1. Query Embedding
2. FAISS Vector Search
3. Hybrid Result Ranking

"""

from __future__ import annotations

from typing import List, Dict, Any

from embeddings.generate_embeddings import EmbeddingGenerator
from search.ranking import ResultRanker
from vector_store.faiss_manager import FAISSManager


class SemanticSearch:
    """
    Complete semantic search pipeline.
    """

    def __init__(self):

        self.embedding_generator = EmbeddingGenerator()
        self.faiss = FAISSManager()
        self.ranker = ResultRanker()

    # -----------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search documents using semantic similarity.

        Parameters
        ----------
        query : str

        top_k : int

        Returns
        -------
        List[dict]
        """

        if not query.strip():
            return []

        # Generate query embedding
        query_embedding = self.embedding_generator.generate_query_embedding(query)

        # Retrieve candidate results from FAISS
        candidates = self.faiss.search(query_embedding=query_embedding, top_k=top_k * 3)

        if not candidates:
            return []

        # Hybrid ranking
        ranked_results = self.ranker.rank(query=query, results=candidates)

        return ranked_results[:top_k]
