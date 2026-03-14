import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.models.base import Base
import backend.models.post  # noqa: F401
import backend.models.analysis  # noqa: F401
from backend.repositories.post_repository import PostRepository
from backend.repositories.analysis_repository import AnalysisRepository
from backend.services.post_service import PostService
from backend.services.analysis_service import AnalysisService


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def services(db_session):
    post_repo = PostRepository(db_session)
    analysis_repo = AnalysisRepository(db_session)
    post_service = PostService(post_repo)
    analysis_service = AnalysisService(post_service, analysis_repo)
    return post_service, analysis_service


@pytest.mark.slow
def test_run_analysis_returns_structure(services, sample_posts):
    post_service, analysis_service = services
    dataset_id = post_service.ingest_posts(sample_posts)
    result = analysis_service.run_analysis(dataset_id)
    assert "dataset_id" in result
    assert "post_count" in result
    assert "lexical_similarity" in result
    assert "semantic_similarity" in result
    assert "cluster_summary" in result
    assert "bubble_score" in result
    assert result["post_count"] == len(sample_posts)


@pytest.mark.slow
def test_run_analysis_persists_result(services, sample_posts):
    post_service, analysis_service = services
    dataset_id = post_service.ingest_posts(sample_posts)
    analysis_service.run_analysis(dataset_id)
    loaded = analysis_service.get_analysis(dataset_id)
    assert loaded["dataset_id"] == dataset_id
