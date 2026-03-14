import numpy as np

from backend.clustering.cluster_labeler import ClusterLabeler
from backend.clustering.topic_clusterer import TopicClusterer
from backend.core.config import settings


class ClusteringService:
    @staticmethod
    def cluster_and_label(
        texts: list[str],
        embeddings: np.ndarray,
        n_clusters: int | None = None,
    ) -> dict:
        if n_clusters is None:
            max_k = min(len(texts) - 1, 8)
            n_clusters = TopicClusterer.find_optimal_k(
                embeddings, k_range=(2, max_k)
            )

        labels, distribution = TopicClusterer.cluster(embeddings, n_clusters)
        cluster_labels = ClusterLabeler.label_clusters(texts, labels)
        cluster_summary = ClusterLabeler.format_cluster_summary(
            labels, distribution, cluster_labels
        )
        return {
            "labels": labels,
            "distribution": distribution,
            "cluster_labels": cluster_labels,
            "cluster_summary": cluster_summary,
        }
