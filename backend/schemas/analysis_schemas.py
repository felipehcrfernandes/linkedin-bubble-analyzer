from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    dataset_id: int
    n_clusters: int | None = None


class ClusterSummaryItem(BaseModel):
    cluster_id: int
    proportion: float
    top_words: list[str]
    post_count: int


class BubbleScoreResult(BaseModel):
    score: float
    interpretation: str


class LexicalSimilarityResult(BaseModel):
    near_duplicates: list[dict]
    duplicate_count: int


class SemanticSimilarityResult(BaseModel):
    similar_pairs: list[dict]
    average_similarity: float


class AnalysisResponse(BaseModel):
    dataset_id: int
    post_count: int
    lexical_similarity: LexicalSimilarityResult
    semantic_similarity: SemanticSimilarityResult
    cluster_summary: list[ClusterSummaryItem]
    bubble_score: BubbleScoreResult
