from backend.similarity.simhash_analyzer import (
    compute_simhash,
    hamming_distance,
    compute_simhash_matrix,
    find_near_duplicates,
)


def test_identical_texts_zero_distance():
    text = "machine learning is transforming healthcare"
    h1 = compute_simhash(text)
    h2 = compute_simhash(text)
    assert hamming_distance(h1, h2) == 0


def test_similar_texts_small_distance():
    h1 = compute_simhash("machine learning is transforming healthcare diagnostics")
    h2 = compute_simhash("machine learning is revolutionizing healthcare diagnostics")
    dist = hamming_distance(h1, h2)
    assert dist < 20


def test_different_texts_large_distance():
    h1 = compute_simhash("machine learning is transforming healthcare")
    h2 = compute_simhash("the best pizza in town is from that italian restaurant")
    dist = hamming_distance(h1, h2)
    assert dist > 10


def test_find_near_duplicates():
    texts = [
        "machine learning is transforming healthcare diagnostics",
        "machine learning is revolutionizing healthcare diagnostics",
        "the best pizza in town is amazing",
    ]
    duplicates = find_near_duplicates(texts, threshold=15)
    assert len(duplicates) >= 1
    pair = duplicates[0]
    assert pair["i"] == 0
    assert pair["j"] == 1


def test_compute_simhash_matrix_shape():
    texts = ["hello world", "foo bar", "baz qux"]
    matrix = compute_simhash_matrix(texts)
    assert len(matrix) == 3
    assert len(matrix[0]) == 3
    assert matrix[0][0] == 0  # self-distance is 0
