import numpy as np
import pytest

from backend.similarity.embedding_generator import EmbeddingGenerator


@pytest.fixture(scope="module")
def generator():
    return EmbeddingGenerator()


@pytest.mark.slow
def test_embeddings_shape(generator):
    texts = ["hello world", "foo bar", "baz qux"]
    embeddings = generator.generate(texts)
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape[0] == 3
    assert embeddings.shape[1] == 384


@pytest.mark.slow
def test_single_embedding_shape(generator):
    embedding = generator.generate(["hello world"])
    assert embedding.shape == (1, 384)


@pytest.mark.slow
def test_similar_texts_higher_similarity(generator):
    embeddings = generator.generate([
        "machine learning in healthcare",
        "AI for medical diagnosis",
        "the best pizza recipe",
    ])
    from numpy.linalg import norm
    sim_01 = np.dot(embeddings[0], embeddings[1]) / (norm(embeddings[0]) * norm(embeddings[1]))
    sim_02 = np.dot(embeddings[0], embeddings[2]) / (norm(embeddings[0]) * norm(embeddings[2]))
    assert sim_01 > sim_02
