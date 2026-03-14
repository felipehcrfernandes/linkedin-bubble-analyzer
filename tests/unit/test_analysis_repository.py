import json

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.exceptions import AnalysisNotFoundError
from backend.models.base import Base
import backend.models.analysis  # noqa: F401
from backend.repositories.analysis_repository import AnalysisRepository


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
def repo(db_session):
    return AnalysisRepository(db_session)


def test_save_and_load_analysis(repo):
    result = {"score": 0.75, "interpretation": "diverse feed"}
    repo.save_analysis(1, result)
    loaded = repo.load_analysis(1)
    assert loaded["score"] == 0.75


def test_load_nonexistent_raises(repo):
    with pytest.raises(AnalysisNotFoundError):
        repo.load_analysis(999)


def test_save_overwrites_existing(repo):
    repo.save_analysis(1, {"score": 0.5})
    repo.save_analysis(1, {"score": 0.8})
    loaded = repo.load_analysis(1)
    assert loaded["score"] == 0.8
