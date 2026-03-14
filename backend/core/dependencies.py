from fastapi import Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.repositories.post_repository import PostRepository
from backend.services.post_service import PostService


def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(db)


def get_post_service(
    repo: PostRepository = Depends(get_post_repository),
) -> PostService:
    return PostService(repo)
