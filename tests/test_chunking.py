"""
Unit Tests for TextChunker

Run:
    pytest tests/

"""

import pytest

from preprocessing.chunker import TextChunker


# ---------------------------------------------------------
# Sample Document
# ---------------------------------------------------------


@pytest.fixture
def sample_document():

    text = " ".join([f"word{i}" for i in range(1, 501)])

    return {
        "document_id": "doc001",
        "filename": "sample.pdf",
        "filetype": "pdf",
        "page_texts": [{"page": 1, "text": text}],
    }


# ---------------------------------------------------------
# Test Chunk Creation
# ---------------------------------------------------------


def test_chunk_creation(sample_document):

    chunker = TextChunker(chunk_size=100, overlap=20)

    chunks = chunker.chunk_document(sample_document)

    assert len(chunks) > 0

    assert chunks[0]["chunk_id"] == 1

    assert chunks[0]["page"] == 1

    assert chunks[0]["filename"] == "sample.pdf"


# ---------------------------------------------------------
# Test Word Limit
# ---------------------------------------------------------


def test_chunk_size_limit(sample_document):

    chunker = TextChunker(chunk_size=100, overlap=20)

    chunks = chunker.chunk_document(sample_document)

    for chunk in chunks:
        assert chunk["word_count"] <= 100


# ---------------------------------------------------------
# Test Overlap
# ---------------------------------------------------------


def test_overlap(sample_document):

    chunker = TextChunker(chunk_size=100, overlap=20)

    chunks = chunker.chunk_document(sample_document)

    first_words = chunks[0]["text"].split()

    second_words = chunks[1]["text"].split()

    overlap = set(first_words[-20:]) & set(second_words[:20])

    assert len(overlap) == 20


# ---------------------------------------------------------
# Test Empty Document
# ---------------------------------------------------------


def test_empty_document():

    document = {
        "document_id": "1",
        "filename": "empty.pdf",
        "filetype": "pdf",
        "page_texts": [],
    }

    chunker = TextChunker()

    chunks = chunker.chunk_document(document)

    assert chunks == []


# ---------------------------------------------------------
# Test Metadata
# ---------------------------------------------------------


def test_metadata_preserved(sample_document):

    chunker = TextChunker()

    chunks = chunker.chunk_document(sample_document)

    for chunk in chunks:
        assert chunk["document_id"] == "doc001"

        assert chunk["filename"] == "sample.pdf"

        assert chunk["filetype"] == "pdf"


# ---------------------------------------------------------
# Test Invalid Overlap
# ---------------------------------------------------------


def test_invalid_overlap():

    with pytest.raises(ValueError):
        TextChunker(chunk_size=100, overlap=100)


# ---------------------------------------------------------
# Test Small Document
# ---------------------------------------------------------


def test_small_document():

    document = {
        "document_id": "1",
        "filename": "small.txt",
        "filetype": "txt",
        "page_texts": [{"page": 1, "text": "Python Flask MySQL"}],
    }

    chunker = TextChunker(chunk_size=100)

    chunks = chunker.chunk_document(document)

    assert len(chunks) == 1

    assert chunks[0]["word_count"] == 3


# ---------------------------------------------------------
# Test Chunk IDs
# ---------------------------------------------------------


def test_chunk_ids_are_unique(sample_document):

    chunker = TextChunker()

    chunks = chunker.chunk_document(sample_document)

    ids = [chunk["chunk_id"] for chunk in chunks]

    assert len(ids) == len(set(ids))
