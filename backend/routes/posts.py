from fastapi import APIRouter, Depends, HTTPException, status

from backend.core.dependencies import get_post_service
from backend.core.exceptions import PostsNotFoundError
from backend.schemas.post_schemas import (
    DatasetListResponse,
    PostResponse,
    PostUploadRequest,
    PostUploadResponse,
)
from backend.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/upload", response_model=PostUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_posts(
    request: PostUploadRequest,
    service: PostService = Depends(get_post_service),
):
    posts_data = [post.model_dump() for post in request.posts]
    dataset_id = service.ingest_posts(posts_data)
    return PostUploadResponse(dataset_id=dataset_id, post_count=len(posts_data))


@router.get("/datasets", response_model=DatasetListResponse)
def list_datasets(service: PostService = Depends(get_post_service)):
    datasets = service.list_datasets()
    return DatasetListResponse(datasets=datasets)


@router.get("/{dataset_id}", response_model=list[PostResponse])
def get_posts(
    dataset_id: int,
    service: PostService = Depends(get_post_service),
):
    try:
        return service.get_posts(dataset_id)
    except PostsNotFoundError:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
