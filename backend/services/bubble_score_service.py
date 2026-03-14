from backend.metrics.bubble_score import compute_bubble_score, interpret_score


class BubbleScoreService:
    @staticmethod
    def compute(distribution: dict[int, float]) -> dict:
        score = compute_bubble_score(distribution)
        return {
            "score": score,
            "interpretation": interpret_score(score),
        }
