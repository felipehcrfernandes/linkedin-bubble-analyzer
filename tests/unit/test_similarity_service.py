import numpy as np
import pytest

from backend.services.similarity_service import SimilarityService


def test_compute_lexical_similarity_returns_structure():
    texts = [
        "machine learning is transforming healthcare",
        "deep learning models for medical diagnosis",
        "the best pizza recipe with mozzarella cheese",
    ]
    result = SimilarityService.compute_lexical_similarity(texts)
    assert "simhash_matrix" in result
    assert "near_duplicates" in result
    assert "duplicate_count" in result
    assert len(result["simhash_matrix"]) == 3


def test_near_duplicates_detected():
    texts = [
        "machine learning is transforming healthcare diagnostics today",
        "machine learning is transforming healthcare diagnostics now",
        "the best pizza in town is absolutely amazing and delicious",
    ]
    result = SimilarityService.compute_lexical_similarity(texts, threshold=15)
    assert result["duplicate_count"] >= 1
    assert any(
        d["i"] == 0 and d["j"] == 1 for d in result["near_duplicates"]
    )


@pytest.mark.slow
def test_compute_semantic_similarity_returns_structure():
    texts = [
        "machine learning is transforming healthcare",
        "AI for medical diagnosis",
        "the best pizza recipe",
    ]
    result = SimilarityService.compute_semantic_similarity(texts)
    assert "embeddings" in result
    assert "cosine_matrix" in result
    assert "similar_pairs" in result
    assert "average_similarity" in result
    assert isinstance(result["embeddings"], np.ndarray)
    assert result["embeddings"].shape[0] == 3


@pytest.mark.slow
def test_semantic_similar_pairs_found():
    texts = [
        "machine learning is transforming healthcare",
        "AI is revolutionizing medical diagnosis",
        "the best pizza recipe with mozzarella",
    ]
    result = SimilarityService.compute_semantic_similarity(texts, threshold=0.3)
    assert any(
        p["i"] == 0 and p["j"] == 1 for p in result["similar_pairs"]
    )
