import pytest

from backend.services.bubble_score_service import BubbleScoreService


def test_compute_returns_structure():
    distribution = {0: 0.5, 1: 0.3, 2: 0.2}
    result = BubbleScoreService.compute(distribution)
    assert "score" in result
    assert "interpretation" in result
    assert 0.0 <= result["score"] <= 1.0


def test_uniform_is_diverse():
    distribution = {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25}
    result = BubbleScoreService.compute(distribution)
    assert result["interpretation"] == "diverse feed"


def test_single_cluster_is_strong_bubble():
    distribution = {0: 1.0}
    result = BubbleScoreService.compute(distribution)
    assert result["interpretation"] == "strong bubble"
