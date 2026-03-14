import numpy as np
import pytest

from backend.services.clustering_service import ClusteringService


@pytest.fixture
def texts_and_embeddings():
    np.random.seed(42)
    texts = [
        "ai machine learning healthcare",
        "deep learning medical diagnosis",
        "neural networks for cancer detection",
        "react frontend web development",
        "vue angular javascript frameworks",
        "css html responsive design",
    ]
    cluster_1 = np.random.rand(3, 10) + [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cluster_2 = np.random.rand(3, 10) + [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    embeddings = np.vstack([cluster_1, cluster_2])
    return texts, embeddings


def test_cluster_and_label_returns_structure(texts_and_embeddings):
    texts, embeddings = texts_and_embeddings
    result = ClusteringService.cluster_and_label(texts, embeddings, n_clusters=2)
    assert "labels" in result
    assert "distribution" in result
    assert "cluster_summary" in result
    assert len(result["labels"]) == 6
    assert len(result["cluster_summary"]) == 2


def test_cluster_auto_k(texts_and_embeddings):
    texts, embeddings = texts_and_embeddings
    result = ClusteringService.cluster_and_label(texts, embeddings, n_clusters=None)
    assert "labels" in result
    assert len(set(result["labels"])) >= 2
