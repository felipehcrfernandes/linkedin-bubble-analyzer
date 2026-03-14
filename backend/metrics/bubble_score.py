import math


def compute_bubble_score(distribution: dict[int, float]) -> float:
    n = len(distribution)
    if n <= 1:
        return 0.0
    entropy = -sum(p * math.log2(p) for p in distribution.values() if p > 0)
    max_entropy = math.log2(n)
    return entropy / max_entropy


def interpret_score(score: float) -> str:
    if score < 0.30:
        return "strong bubble"
    elif score < 0.60:
        return "moderate bubble"
    else:
        return "diverse feed"
