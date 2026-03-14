from fastapi import APIRouter, Depends, HTTPException

from backend.core.dependencies import get_analysis_service
from backend.core.exceptions import AnalysisNotFoundError, PostsNotFoundError
from backend.schemas.analysis_schemas import (
    AnalysisRequest,
    AnalysisResponse,
)
from backend.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/run", response_model=AnalysisResponse)
def run_analysis(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),
):
    try:
        result = service.run_analysis(
            request.dataset_id, n_clusters=request.n_clusters
        )
        return result
    except PostsNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Dataset {request.dataset_id} not found"
        )


@router.get("/{dataset_id}", response_model=AnalysisResponse)
def get_analysis(
    dataset_id: int,
    service: AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.get_analysis(dataset_id)
    except AnalysisNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis for dataset {dataset_id} not found",
        )
