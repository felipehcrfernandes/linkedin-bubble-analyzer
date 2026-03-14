import numpy as np
from sentence_transformers import SentenceTransformer

from backend.core.config import settings


class EmbeddingGenerator:
    def __init__(self, model_name: str | None = None):
        self.model = SentenceTransformer(model_name or settings.embedding_model)

    def generate(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)
