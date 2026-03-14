import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models.base import Base
from backend.repositories.post_repository import PostRepository
from backend.services.post_service import PostService


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def service(db_session):
    repo = PostRepository(db_session)
    return PostService(repo)


def test_ingest_posts_cleans_and_persists(service, sample_posts):
    dataset_id = service.ingest_posts(sample_posts)
    posts = service.get_posts(dataset_id)
    assert len(posts) == len(sample_posts)
    for post in posts:
        assert "cleaned_text" in post
        assert post["cleaned_text"] is not None


def test_ingest_posts_returns_dataset_id(service, sample_posts):
    dataset_id = service.ingest_posts(sample_posts)
    assert isinstance(dataset_id, int)
    assert dataset_id >= 1


def test_get_posts_retrieves_ingested(service, sample_posts):
    dataset_id = service.ingest_posts(sample_posts)
    posts = service.get_posts(dataset_id)
    assert posts[0]["author"] == sample_posts[0]["author"]
