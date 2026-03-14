import json

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
def analyzed_dataset_id(client, sample_posts):
    response = client.post("/posts/upload", json={"posts": sample_posts})
    dataset_id = response.json()["dataset_id"]
    client.post("/analysis/run", json={"dataset_id": dataset_id})
    return dataset_id


@pytest.mark.slow
def test_get_visualization_returns_200(client, analyzed_dataset_id):
    response = client.get(f"/visualization/{analyzed_dataset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["dataset_id"] == analyzed_dataset_id
    assert "topic_map" in data
    assert "distribution_chart" in data
    assert "bubble_indicator" in data


@pytest.mark.slow
def test_get_visualization_charts_are_valid_json(client, analyzed_dataset_id):
    response = client.get(f"/visualization/{analyzed_dataset_id}")
    data = response.json()
    json.loads(data["topic_map"])
    json.loads(data["distribution_chart"])
    json.loads(data["bubble_indicator"])


def test_get_visualization_nonexistent_dataset_returns_404(client):
    response = client.get("/visualization/999")
    assert response.status_code == 404
