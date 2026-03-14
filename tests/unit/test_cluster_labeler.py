from backend.clustering.cluster_labeler import ClusterLabeler


def test_label_clusters_keys_match_labels():
    texts = [
        "ai machine learning healthcare",
        "deep learning medical diagnosis",
        "react frontend web development",
        "vue angular javascript frameworks",
    ]
    labels = [0, 0, 1, 1]
    result = ClusterLabeler.label_clusters(texts, labels)
    assert 0 in result
    assert 1 in result


def test_top_words_count():
    texts = [
        "ai machine learning healthcare diagnosis",
        "deep learning medical ai models",
        "react frontend web development javascript",
        "vue angular javascript frameworks web",
    ]
    labels = [0, 0, 1, 1]
    result = ClusterLabeler.label_clusters(texts, labels, top_n=3)
    for cluster_id in result:
        assert len(result[cluster_id]) == 3


def test_format_cluster_summary_structure():
    labels = [0, 0, 1, 1]
    distribution = {0: 0.5, 1: 0.5}
    cluster_labels = {0: ["ai", "healthcare"], 1: ["react", "frontend"]}
    summary = ClusterLabeler.format_cluster_summary(
        labels, distribution, cluster_labels
    )
    assert len(summary) == 2
    assert summary[0]["cluster_id"] == 0
    assert summary[0]["proportion"] == 0.5
    assert summary[0]["top_words"] == ["ai", "healthcare"]
    assert summary[0]["post_count"] == 2
