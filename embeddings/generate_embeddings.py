"""
Generate Embeddings

Converts text chunks into embedding vectors using
the Sentence Transformer model.

"""

from typing import List, Dict, Any

import numpy as np

from embeddings.embedding_model import EmbeddingModel


class EmbeddingGenerator:
    """
    Generates embeddings for document chunks.
    """

    def __init__(self):

        self.model = EmbeddingModel()

    def generate(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for all chunks.

        Parameters
        ----------
        chunks : list
            List of chunk dictionaries.

        Returns
        -------
        list
            Chunks with embeddings attached.
        """

        if not chunks:
            return []

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        return chunks

    def generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate embedding for a search query.

        Parameters
        ----------
        query : str

        Returns
        -------
        numpy.ndarray
        """

        return self.model.encode(query)[0]
