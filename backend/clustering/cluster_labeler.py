from sklearn.feature_extraction.text import TfidfVectorizer


class ClusterLabeler:
    @staticmethod
    def label_clusters(
        texts: list[str], labels: list[int], top_n: int = 5
    ) -> dict[int, list[str]]:
        cluster_ids = sorted(set(labels))
        cluster_texts = {}
        for cluster_id in cluster_ids:
            cluster_texts[cluster_id] = " ".join(
                text for text, label in zip(texts, labels) if label == cluster_id
            )

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(cluster_texts.values())
        feature_names = vectorizer.get_feature_names_out()

        result = {}
        for idx, cluster_id in enumerate(cluster_ids):
            scores = tfidf_matrix[idx].toarray().flatten()
            top_indices = scores.argsort()[-top_n:][::-1]
            result[cluster_id] = [feature_names[i] for i in top_indices]
        return result

    @staticmethod
    def format_cluster_summary(
        labels: list[int],
        distribution: dict[int, float],
        cluster_labels: dict[int, list[str]],
    ) -> list[dict]:
        summary = []
        for cluster_id in sorted(distribution.keys()):
            post_count = labels.count(cluster_id)
            summary.append({
                "cluster_id": cluster_id,
                "proportion": distribution[cluster_id],
                "top_words": cluster_labels.get(cluster_id, []),
                "post_count": post_count,
            })
        return summary
