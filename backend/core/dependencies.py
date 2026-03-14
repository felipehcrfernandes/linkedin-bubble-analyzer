from fastapi import Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.repositories.analysis_repository import AnalysisRepository
from backend.repositories.post_repository import PostRepository
from backend.services.analysis_service import AnalysisService
from backend.services.post_service import PostService
from backend.services.visualization_service import VisualizationService


def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(db)


def get_analysis_repository(db: Session = Depends(get_db)) -> AnalysisRepository:
    return AnalysisRepository(db)


def get_post_service(
    repo: PostRepository = Depends(get_post_repository),
) -> PostService:
    return PostService(repo)


def get_analysis_service(
    post_service: PostService = Depends(get_post_service),
    analysis_repo: AnalysisRepository = Depends(get_analysis_repository),
) -> AnalysisService:
    return AnalysisService(post_service, analysis_repo)
