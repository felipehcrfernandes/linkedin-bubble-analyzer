import numpy as np
import pytest

from backend.similarity.cosine_similarity import (
    cosine_similarity_matrix,
    find_similar_pairs,
    average_similarity,
)


def test_identical_vectors_similarity_one():
    v = np.array([[1.0, 0.0, 0.0]])
    matrix = cosine_similarity_matrix(v)
    assert matrix[0][0] == pytest.approx(1.0)


def test_orthogonal_vectors_similarity_zero():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0]])
    matrix = cosine_similarity_matrix(vectors)
    assert matrix[0][1] == pytest.approx(0.0, abs=1e-6)


def test_matrix_dimensions():
    vectors = np.random.rand(5, 10)
    matrix = cosine_similarity_matrix(vectors)
    assert matrix.shape == (5, 5)


def test_find_similar_pairs_threshold():
    vectors = np.array([
        [1.0, 0.0, 0.0],
        [0.99, 0.1, 0.0],
        [0.0, 0.0, 1.0],
    ])
    pairs = find_similar_pairs(vectors, threshold=0.9)
    assert len(pairs) >= 1
    assert any(p["i"] == 0 and p["j"] == 1 for p in pairs)
    assert not any(p["i"] == 0 and p["j"] == 2 for p in pairs)


def test_average_similarity_excludes_diagonal():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0]])
    avg = average_similarity(vectors)
    assert avg == pytest.approx(0.0, abs=1e-6)
