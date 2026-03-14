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


@pytest.mark.slow
def test_full_pipeline_upload_analyze_visualize(client, sample_posts):
    # Step 1: Upload posts
    upload_response = client.post("/posts/upload", json={"posts": sample_posts})
    assert upload_response.status_code == 201
    dataset_id = upload_response.json()["dataset_id"]
    assert isinstance(dataset_id, int)

    # Step 2: Run analysis
    analysis_response = client.post(
        "/analysis/run", json={"dataset_id": dataset_id}
    )
    assert analysis_response.status_code == 200
    analysis = analysis_response.json()

    assert analysis["dataset_id"] == dataset_id
    assert analysis["post_count"] == len(sample_posts)
    assert len(analysis["cluster_summary"]) > 0
    assert 0 <= analysis["bubble_score"]["score"] <= 1
    assert analysis["bubble_score"]["interpretation"] in (
        "strong bubble",
        "moderate bubble",
        "diverse feed",
    )

    # Step 3: Retrieve stored analysis
    get_response = client.get(f"/analysis/{dataset_id}")
    assert get_response.status_code == 200
    assert get_response.json()["dataset_id"] == dataset_id

    # Step 4: Get visualization
    viz_response = client.get(f"/visualization/{dataset_id}")
    assert viz_response.status_code == 200
    viz = viz_response.json()

    assert viz["dataset_id"] == dataset_id
    topic_map = json.loads(viz["topic_map"])
    distribution = json.loads(viz["distribution_chart"])
    indicator = json.loads(viz["bubble_indicator"])

    assert "data" in topic_map
    assert "data" in distribution
    assert "data" in indicator
