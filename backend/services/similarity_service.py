from backend.core.config import settings
from backend.similarity.cosine_similarity import (
    average_similarity,
    cosine_similarity_matrix,
    find_similar_pairs,
)
from backend.similarity.embedding_generator import EmbeddingGenerator
from backend.similarity.simhash_analyzer import (
    compute_simhash_matrix,
    find_near_duplicates,
)

_embedding_generator: EmbeddingGenerator | None = None


def _get_embedding_generator() -> EmbeddingGenerator:
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator


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

    @staticmethod
    def compute_semantic_similarity(
        texts: list[str], threshold: float | None = None
    ) -> dict:
        if threshold is None:
            threshold = settings.cosine_similarity_threshold
        generator = _get_embedding_generator()
        embeddings = generator.generate(texts)
        cosine_matrix = cosine_similarity_matrix(embeddings)
        similar_pairs = find_similar_pairs(embeddings, threshold=threshold)
        avg_sim = average_similarity(embeddings)
        return {
            "embeddings": embeddings,
            "cosine_matrix": cosine_matrix.tolist(),
            "similar_pairs": similar_pairs,
            "average_similarity": avg_sim,
        }
