from fastapi import APIRouter, Depends, HTTPException

from backend.core.dependencies import get_analysis_service, get_post_service
from backend.core.exceptions import AnalysisNotFoundError, PostsNotFoundError
from backend.schemas.visualization_schemas import VisualizationResponse
from backend.services.analysis_service import AnalysisService
from backend.services.clustering_service import ClusteringService
from backend.services.post_service import PostService
from backend.services.similarity_service import SimilarityService
from backend.services.visualization_service import VisualizationService

router = APIRouter(prefix="/visualization", tags=["visualization"])


@router.get("/{dataset_id}", response_model=VisualizationResponse)
def get_visualization(
    dataset_id: int,
    post_service: PostService = Depends(get_post_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        analysis = analysis_service.get_analysis(dataset_id)
    except AnalysisNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis for dataset {dataset_id} not found",
        )

    try:
        posts = post_service.get_posts(dataset_id)
    except PostsNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Dataset {dataset_id} not found"
        )

    texts = [p["cleaned_text"] for p in posts]

    semantic = SimilarityService.compute_semantic_similarity(texts)
    n_clusters = len(analysis["cluster_summary"])
    clustering = ClusteringService.cluster_and_label(
        texts, semantic["embeddings"], n_clusters=n_clusters
    )

    charts = VisualizationService.generate_all_charts(
        embeddings=semantic["embeddings"],
        labels=clustering["labels"],
        texts=texts,
        cluster_summary=analysis["cluster_summary"],
        bubble_score=analysis["bubble_score"],
    )

    return {"dataset_id": dataset_id, **charts}
