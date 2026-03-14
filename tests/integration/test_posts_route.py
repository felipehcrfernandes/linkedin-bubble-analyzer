import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.database import get_db
from backend.main import app
from backend.models.base import Base
import backend.models.post  # noqa: F401 - register Post table with Base


@pytest.fixture(autouse=True)
def override_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def upload_payload(sample_posts):
    return {"posts": sample_posts}


def test_upload_posts_returns_201(client, upload_payload):
    response = client.post("/posts/upload", json=upload_payload)
    assert response.status_code == 201
    data = response.json()
    assert "dataset_id" in data
    assert isinstance(data["dataset_id"], int)
    assert data["post_count"] == 10


def test_upload_empty_list_returns_422(client):
    response = client.post("/posts/upload", json={"posts": []})
    assert response.status_code == 422


def test_get_posts_by_dataset(client, upload_payload):
    upload = client.post("/posts/upload", json=upload_payload)
    dataset_id = upload.json()["dataset_id"]
    response = client.get(f"/posts/{dataset_id}")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 10
    assert posts[0]["cleaned_text"] is not None


def test_get_nonexistent_dataset_returns_404(client):
    response = client.get("/posts/999")
    assert response.status_code == 404


def test_list_datasets(client, upload_payload):
    client.post("/posts/upload", json=upload_payload)
    response = client.get("/posts/datasets")
    assert response.status_code == 200
    data = response.json()
    assert len(data["datasets"]) == 1
