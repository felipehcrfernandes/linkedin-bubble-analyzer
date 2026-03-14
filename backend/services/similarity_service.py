from backend.core.config import settings
from backend.similarity.simhash_analyzer import (
    compute_simhash_matrix,
    find_near_duplicates,
)


class SimilarityService:
    @staticmethod
    def compute_lexical_similarity(
        texts: list[str], threshold: int | None = None
    ) -> dict:
        if threshold is None:
            threshold = settings.simhash_distance_threshold
        matrix = compute_simhash_matrix(texts)
        duplicates = find_near_duplicates(texts, threshold=threshold)
        return {
            "simhash_matrix": matrix,
            "near_duplicates": duplicates,
            "duplicate_count": len(duplicates),
        }
