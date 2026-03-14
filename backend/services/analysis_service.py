from backend.repositories.analysis_repository import AnalysisRepository
from backend.services.bubble_score_service import BubbleScoreService
from backend.services.clustering_service import ClusteringService
from backend.services.post_service import PostService
from backend.services.similarity_service import SimilarityService


class AnalysisService:
    def __init__(
        self,
        post_service: PostService,
        analysis_repository: AnalysisRepository,
    ):
        self.post_service = post_service
        self.analysis_repository = analysis_repository

    def run_analysis(self, dataset_id: int, n_clusters: int | None = None) -> dict:
        posts = self.post_service.get_posts(dataset_id)
        texts = [p["cleaned_text"] for p in posts]

        lexical = SimilarityService.compute_lexical_similarity(texts)
        semantic = SimilarityService.compute_semantic_similarity(texts)
        clustering = ClusteringService.cluster_and_label(
            texts, semantic["embeddings"], n_clusters=n_clusters
        )
        bubble = BubbleScoreService.compute(clustering["distribution"])

        result = {
            "dataset_id": dataset_id,
            "post_count": len(posts),
            "lexical_similarity": {
                "near_duplicates": lexical["near_duplicates"],
                "duplicate_count": lexical["duplicate_count"],
            },
            "semantic_similarity": {
                "similar_pairs": semantic["similar_pairs"],
                "average_similarity": semantic["average_similarity"],
            },
            "cluster_summary": clustering["cluster_summary"],
            "bubble_score": bubble,
        }

        self.analysis_repository.save_analysis(dataset_id, result)
        return result

    def get_analysis(self, dataset_id: int) -> dict:
        return self.analysis_repository.load_analysis(dataset_id)
