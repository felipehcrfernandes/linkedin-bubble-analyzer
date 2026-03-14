import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.database import get_db
from backend.main import app
from backend.models.base import Base
import backend.models.post  # noqa: F401
import backend.models.analysis  # noqa: F401


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
def dataset_id(client, sample_posts):
    response = client.post("/posts/upload", json={"posts": sample_posts})
    return response.json()["dataset_id"]


@pytest.mark.slow
def test_run_analysis_returns_200(client, dataset_id):
    response = client.post("/analysis/run", json={"dataset_id": dataset_id})
    assert response.status_code == 200
    data = response.json()
    assert data["dataset_id"] == dataset_id
    assert "bubble_score" in data
    assert "cluster_summary" in data


@pytest.mark.slow
def test_get_analysis_after_run(client, dataset_id):
    client.post("/analysis/run", json={"dataset_id": dataset_id})
    response = client.get(f"/analysis/{dataset_id}")
    assert response.status_code == 200
    assert response.json()["dataset_id"] == dataset_id


def test_run_analysis_nonexistent_dataset_returns_404(client):
    response = client.post("/analysis/run", json={"dataset_id": 999})
    assert response.status_code == 404


def test_get_analysis_not_run_returns_404(client):
    response = client.get("/analysis/999")
    assert response.status_code == 404
