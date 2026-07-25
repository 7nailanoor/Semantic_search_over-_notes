"""
Similarity Utilities

Provides helper functions to calculate similarity
between embedding vectors.

Author: Naila Noor
Project: Semantic Search over Notes
"""

from typing import List

import numpy as np


class Similarity:
    """
    Utility class for similarity calculations.
    """

    @staticmethod
    def cosine_similarity(vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Returns
        -------
        float
            Similarity score between -1 and 1.
        """

        vector1 = np.asarray(vector1, dtype=np.float32)
        vector2 = np.asarray(vector2, dtype=np.float32)

        denominator = np.linalg.norm(vector1) * np.linalg.norm(vector2)

        if denominator == 0:
            return 0.0

        similarity = np.dot(vector1, vector2) / denominator

        return float(similarity)

    @staticmethod
    def batch_similarity(
        query_vector: np.ndarray, embeddings: List[np.ndarray]
    ) -> List[float]:
        """
        Calculate cosine similarity between a query vector
        and multiple embedding vectors.

        Returns
        -------
        List[float]
        """

        scores = []

        for embedding in embeddings:
            score = Similarity.cosine_similarity(query_vector, embedding)

            scores.append(score)

        return scores

    @staticmethod
    def most_similar(
        query_vector: np.ndarray, embeddings: List[np.ndarray], top_k: int = 5
    ):
        """
        Return indices and scores of the most similar vectors.

        Returns
        -------
        List[Tuple[int, float]]
        """

        scores = Similarity.batch_similarity(query_vector, embeddings)

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        return ranked[:top_k]
