import json

import numpy as np
import pytest

from backend.services.visualization_service import VisualizationService


@pytest.mark.slow
def test_generate_all_charts():
    np.random.seed(42)
    embeddings = np.random.rand(10, 384)
    labels = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    texts = [f"post {i}" for i in range(10)]
    cluster_summary = [
        {"cluster_id": 0, "proportion": 0.5, "top_words": ["ai", "ml"], "post_count": 5},
        {"cluster_id": 1, "proportion": 0.5, "top_words": ["web", "react"], "post_count": 5},
    ]
    bubble_score = {"score": 1.0, "interpretation": "diverse feed"}

    result = VisualizationService.generate_all_charts(
        embeddings=embeddings,
        labels=labels,
        texts=texts,
        cluster_summary=cluster_summary,
        bubble_score=bubble_score,
    )
    assert "topic_map" in result
    assert "distribution_chart" in result
    assert "bubble_indicator" in result
    for chart in result.values():
        parsed = json.loads(chart)
        assert "data" in parsed
