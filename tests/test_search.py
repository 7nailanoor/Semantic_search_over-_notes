"""
Unit Tests for Semantic Search

Run:
    pytest tests/

"""

from unittest.mock import MagicMock

from search.semantic_search import SemanticSearch


# ---------------------------------------------------------
# Sample Search Results
# ---------------------------------------------------------


def sample_results():

    return [
        {
            "document_id": "doc1",
            "filename": "expense.pdf",
            "page": 2,
            "chunk_id": 1,
            "text": "Python Flask MySQL Bootstrap",
            "similarity": 0.95,
        },
        {
            "document_id": "doc1",
            "filename": "expense.pdf",
            "page": 4,
            "chunk_id": 2,
            "text": "Expense tracking application",
            "similarity": 0.82,
        },
    ]


# ---------------------------------------------------------
# Test Successful Search
# ---------------------------------------------------------


def test_search_returns_results():

    search = SemanticSearch()

    search.embedding_generator.generate_query_embedding = MagicMock(
        return_value=[0.1] * 384
    )

    search.faiss.search = MagicMock(return_value=sample_results())

    search.ranker.rank = MagicMock(return_value=sample_results())

    results = search.search("What tools are used?")

    assert len(results) == 2

    assert results[0]["filename"] == "expense.pdf"


# ---------------------------------------------------------
# Test Empty Query
# ---------------------------------------------------------


def test_empty_query():

    search = SemanticSearch()

    results = search.search("")

    assert results == []


# ---------------------------------------------------------
# Test No Search Results
# ---------------------------------------------------------


def test_no_results():

    search = SemanticSearch()

    search.embedding_generator.generate_query_embedding = MagicMock(
        return_value=[0.1] * 384
    )

    search.faiss.search = MagicMock(return_value=[])

    results = search.search("Artificial Intelligence")

    assert results == []


# ---------------------------------------------------------
# Test Top K Results
# ---------------------------------------------------------


def test_top_k_results():

    search = SemanticSearch()

    fake_results = sample_results() * 5

    search.embedding_generator.generate_query_embedding = MagicMock(
        return_value=[0.1] * 384
    )

    search.faiss.search = MagicMock(return_value=fake_results)

    search.ranker.rank = MagicMock(return_value=fake_results)

    results = search.search("Python", top_k=3)

    assert len(results) == 3


# ---------------------------------------------------------
# Test Ranking Called
# ---------------------------------------------------------


def test_ranking_called():

    search = SemanticSearch()

    search.embedding_generator.generate_query_embedding = MagicMock(
        return_value=[0.1] * 384
    )

    search.faiss.search = MagicMock(return_value=sample_results())

    search.ranker.rank = MagicMock(return_value=sample_results())

    search.search("Python")

    search.ranker.rank.assert_called_once()


# ---------------------------------------------------------
# Test Query Embedding Called
# ---------------------------------------------------------


def test_query_embedding_called():

    search = SemanticSearch()

    search.embedding_generator.generate_query_embedding = MagicMock(
        return_value=[0.1] * 384
    )

    search.faiss.search = MagicMock(return_value=[])

    search.search("Machine Learning")

    search.embedding_generator.generate_query_embedding.assert_called_once()


# ---------------------------------------------------------
# Test FAISS Search Called
# ---------------------------------------------------------


def test_faiss_search_called():

    search = SemanticSearch()

    search.embedding_generator.generate_query_embedding = MagicMock(
        return_value=[0.1] * 384
    )

    search.faiss.search = MagicMock(return_value=[])

    search.search("Flask")

    search.faiss.search.assert_called_once()
