import json

from backend.visualization.chart_builder import ChartBuilder


def test_topic_map_returns_valid_json():
    points = [
        {"x": 1.0, "y": 2.0, "cluster": 0, "text": "hello"},
        {"x": 3.0, "y": 4.0, "cluster": 1, "text": "world"},
    ]
    result = ChartBuilder.topic_map(points)
    parsed = json.loads(result)
    assert "data" in parsed
    assert "layout" in parsed


def test_distribution_chart_valid_json():
    cluster_summary = [
        {"cluster_id": 0, "proportion": 0.6, "top_words": ["ai", "ml"], "post_count": 6},
        {"cluster_id": 1, "proportion": 0.4, "top_words": ["web", "react"], "post_count": 4},
    ]
    result = ChartBuilder.distribution_chart(cluster_summary)
    parsed = json.loads(result)
    assert "data" in parsed
    assert "layout" in parsed


def test_bubble_indicator_valid_json():
    result = ChartBuilder.bubble_indicator(score=0.65, interpretation="diverse feed")
    parsed = json.loads(result)
    assert "data" in parsed
    assert "layout" in parsed
