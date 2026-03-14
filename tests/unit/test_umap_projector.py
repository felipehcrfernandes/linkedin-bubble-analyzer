import numpy as np
import pytest

from backend.visualization.umap_projector import UmapProjector


@pytest.mark.slow
def test_projection_shape():
    np.random.seed(42)
    embeddings = np.random.rand(10, 384)
    projection = UmapProjector.project(embeddings)
    assert projection.shape == (10, 2)


@pytest.mark.slow
def test_project_with_metadata_fields():
    np.random.seed(42)
    embeddings = np.random.rand(5, 384)
    labels = [0, 0, 1, 1, 1]
    texts = ["text a", "text b", "text c", "text d", "text e"]
    points = UmapProjector.project_with_metadata(embeddings, labels, texts)
    assert len(points) == 5
    for point in points:
        assert "x" in point
        assert "y" in point
        assert "cluster" in point
        assert "text" in point
