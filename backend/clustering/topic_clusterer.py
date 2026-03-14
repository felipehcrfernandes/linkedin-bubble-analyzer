import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class TopicClusterer:
    @staticmethod
    def cluster(
        embeddings: np.ndarray, n_clusters: int = 5
    ) -> tuple[list[int], dict[int, float]]:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings).tolist()
        distribution = {}
        total = len(labels)
        for cluster_id in range(n_clusters):
            count = labels.count(cluster_id)
            distribution[cluster_id] = count / total
        return labels, distribution

    @staticmethod
    def find_optimal_k(
        embeddings: np.ndarray, k_range: tuple[int, int] = (2, 8)
    ) -> int:
        best_k = k_range[0]
        best_score = -1.0
        for k in range(k_range[0], k_range[1] + 1):
            if k >= len(embeddings):
                break
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels)
            if score > best_score:
                best_score = score
                best_k = k
        return best_k
