"""
Unit Tests for Embedding Generation

Run:
    pytest tests/

"""

import pytest
import numpy as np

from embeddings.embedding_model import EmbeddingModel
from embeddings.generate_embeddings import EmbeddingGenerator


# ---------------------------------------------------------
# Sample Text
# ---------------------------------------------------------


@pytest.fixture
def sample_texts():
    return [
        "Python is a programming language.",
        "Flask is a lightweight web framework.",
        "FAISS is used for semantic search.",
    ]


# ---------------------------------------------------------
# Test Model Loading
# ---------------------------------------------------------


def test_model_loading():

    model = EmbeddingModel()

    assert model.model is not None


# ---------------------------------------------------------
# Test Single Text Embedding
# ---------------------------------------------------------


def test_single_embedding():

    model = EmbeddingModel()

    embedding = model.encode("Machine Learning")

    assert isinstance(embedding, np.ndarray)

    assert embedding.shape[0] == 1


# ---------------------------------------------------------
# Test Multiple Embeddings
# ---------------------------------------------------------


def test_multiple_embeddings(sample_texts):

    model = EmbeddingModel()

    embeddings = model.encode(sample_texts)

    assert len(embeddings) == len(sample_texts)


# ---------------------------------------------------------
# Test Embedding Dimension
# ---------------------------------------------------------


def test_embedding_dimension():

    model = EmbeddingModel()

    dimension = model.embedding_dimension()

    embedding = model.encode("Python")

    assert embedding.shape[1] == dimension


# ---------------------------------------------------------
# Test Query Embedding
# ---------------------------------------------------------


def test_query_embedding():

    generator = EmbeddingGenerator()

    query_embedding = generator.generate_query_embedding("What tools are used?")

    assert isinstance(query_embedding, np.ndarray)

    assert len(query_embedding.shape) == 1


# ---------------------------------------------------------
# Test Chunk Embeddings
# ---------------------------------------------------------


def test_generate_embeddings():

    chunks = [
        {"chunk_id": 1, "text": "Python Flask MySQL"},
        {"chunk_id": 2, "text": "Machine Learning and AI"},
    ]

    generator = EmbeddingGenerator()

    result = generator.generate(chunks)

    assert len(result) == 2

    assert "embedding" in result[0]

    assert isinstance(result[0]["embedding"], np.ndarray)


# ---------------------------------------------------------
# Test Empty Input
# ---------------------------------------------------------


def test_empty_input():

    model = EmbeddingModel()

    with pytest.raises(ValueError):
        model.encode([])


# ---------------------------------------------------------
# Test Model Info
# ---------------------------------------------------------


def test_model_info():

    model = EmbeddingModel()

    info = model.model_info()

    assert "model_name" in info

    assert "device" in info

    assert "embedding_dimension" in info
