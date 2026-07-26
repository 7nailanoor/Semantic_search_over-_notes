"""
Embedding Model Manager

Loads and manages Sentence Transformer models for semantic search.

Features
--------
- Singleton model loading
- Automatic GPU/CPU selection
- Batch encoding
- L2 normalized embeddings
- Logging
- Input validation

"""

from __future__ import annotations

import logging
from typing import List, Sequence, Union

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """
    Wrapper around SentenceTransformer.

    The model is loaded only once and reused across the
    application.
    """

    _model = None

    DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name: str | None = None,
    ):

        self.model_name = model_name or self.DEFAULT_MODEL

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if EmbeddingModel._model is None:
            logger.info(
                "Loading embedding model: %s",
                self.model_name,
            )

            EmbeddingModel._model = SentenceTransformer(
                self.model_name,
                device=self.device,
            )

            logger.info(
                "Embedding model loaded on %s",
                self.device,
            )

        self.model = EmbeddingModel._model

    # ---------------------------------------------------------
    # Public Methods
    # ---------------------------------------------------------

    def encode(
        self,
        texts: Union[str, Sequence[str]],
        batch_size: int = 32,
        normalize: bool = True,
    ) -> np.ndarray:
        """
        Encode one or multiple texts.

        Parameters
        ----------
        texts
            Single string or list of strings.

        batch_size
            Encoding batch size.

        normalize
            L2 normalize vectors.

        Returns
        -------
        numpy.ndarray
        """

        if isinstance(texts, str):
            texts = [texts]

        texts = [
            text.strip() for text in texts if isinstance(text, str) and text.strip()
        ]

        if not texts:
            raise ValueError("No valid text provided for embedding.")

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
        )

        return embeddings.astype(np.float32)

    def encode_document(
        self,
        document: dict,
        text_key: str = "text",
    ) -> np.ndarray:
        """
        Encode a document dictionary.

        Parameters
        ----------
        document

        text_key

        Returns
        -------
        numpy.ndarray
        """

        if text_key not in document:
            raise KeyError(f"'{text_key}' not found in document.")

        return self.encode(document[text_key])

    def embedding_dimension(self) -> int:
        """
        Return embedding vector size.
        """

        return self.model.get_sentence_embedding_dimension()

    def model_info(self) -> dict:
        """
        Return model information.
        """

        return {
            "model_name": self.model_name,
            "device": self.device,
            "embedding_dimension": self.embedding_dimension(),
        }
