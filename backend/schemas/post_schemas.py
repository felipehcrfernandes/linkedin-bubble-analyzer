from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    author: str
    content: str
    date: str | None = None


class PostResponse(BaseModel):
    author: str
    content: str
    cleaned_text: str | None = None
    date: str | None = None

    model_config = {"from_attributes": True}


class PostUploadRequest(BaseModel):
    posts: list[PostCreate] = Field(..., min_length=1)


class PostUploadResponse(BaseModel):
    dataset_id: str
    post_count: int


class DatasetListResponse(BaseModel):
    datasets: list[str]
