import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.exceptions import PostsNotFoundError
from backend.models.base import Base
from backend.models.post import Post
from backend.repositories.post_repository import PostRepository


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def repo(db_session):
    return PostRepository(db_session)


def test_save_and_load_posts(repo):
    posts = [
        {"author": "Alice", "content": "Hello world", "cleaned_text": "hello world"},
        {"author": "Bob", "content": "Goodbye world", "cleaned_text": "goodbye world"},
    ]
    dataset_id = repo.save_posts(1, posts)
    loaded = repo.load_posts(dataset_id)
    assert len(loaded) == 2
    assert loaded[0]["author"] == "Alice"
    assert loaded[1]["author"] == "Bob"


def test_load_nonexistent_dataset_raises(repo):
    with pytest.raises(PostsNotFoundError):
        repo.load_posts(999)


def test_list_datasets(repo):
    repo.save_posts(1, [{"author": "A", "content": "x", "cleaned_text": "x"}])
    repo.save_posts(2, [{"author": "B", "content": "y", "cleaned_text": "y"}])
    datasets = repo.list_datasets()
    assert 1 in datasets
    assert 2 in datasets


def test_next_dataset_id_starts_at_one(repo):
    assert repo.next_dataset_id() == 1


def test_next_dataset_id_increments(repo):
    repo.save_posts(1, [{"author": "A", "content": "x", "cleaned_text": "x"}])
    assert repo.next_dataset_id() == 2
