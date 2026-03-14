import pytest

from backend.metrics.bubble_score import compute_bubble_score, interpret_score


def test_uniform_distribution_score_near_one():
    distribution = {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25}
    score = compute_bubble_score(distribution)
    assert score == pytest.approx(1.0, abs=0.01)


def test_single_cluster_score_zero():
    distribution = {0: 1.0}
    score = compute_bubble_score(distribution)
    assert score == pytest.approx(0.0)


def test_skewed_distribution_intermediate():
    distribution = {0: 0.8, 1: 0.1, 2: 0.1}
    score = compute_bubble_score(distribution)
    assert 0.0 < score < 1.0


def test_interpret_strong_bubble():
    label = interpret_score(0.20)
    assert label == "strong bubble"


def test_interpret_moderate():
    label = interpret_score(0.45)
    assert label == "moderate bubble"


def test_interpret_diverse():
    label = interpret_score(0.75)
    assert label == "diverse feed"
