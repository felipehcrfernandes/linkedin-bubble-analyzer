import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine


def cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    return sklearn_cosine(vectors)


def find_similar_pairs(
    vectors: np.ndarray, threshold: float = 0.8
) -> list[dict]:
    matrix = cosine_similarity_matrix(vectors)
    n = matrix.shape[0]
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] >= threshold:
                pairs.append({"i": i, "j": j, "similarity": float(matrix[i][j])})
    return pairs


def average_similarity(vectors: np.ndarray) -> float:
    matrix = cosine_similarity_matrix(vectors)
    n = matrix.shape[0]
    if n < 2:
        return 0.0
    total = matrix.sum() - np.trace(matrix)
    count = n * (n - 1)
    return float(total / count)
