import numpy as np
import pytest

from backend.clustering.topic_clusterer import TopicClusterer


@pytest.fixture
def embeddings():
    np.random.seed(42)
    cluster_1 = np.random.rand(5, 10) + [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cluster_2 = np.random.rand(5, 10) + [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    return np.vstack([cluster_1, cluster_2])


def test_cluster_posts_correct_label_count(embeddings):
    labels, distribution = TopicClusterer.cluster(embeddings, n_clusters=2)
    unique_labels = set(labels)
    assert len(unique_labels) == 2


def test_all_posts_labeled(embeddings):
    labels, distribution = TopicClusterer.cluster(embeddings, n_clusters=2)
    assert len(labels) == 10


def test_distribution_sums_to_one(embeddings):
    labels, distribution = TopicClusterer.cluster(embeddings, n_clusters=2)
    assert sum(distribution.values()) == pytest.approx(1.0)


def test_find_optimal_k_in_range(embeddings):
    optimal_k = TopicClusterer.find_optimal_k(embeddings, k_range=(2, 5))
    assert 2 <= optimal_k <= 5
