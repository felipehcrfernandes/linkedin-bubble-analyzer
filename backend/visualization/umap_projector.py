import numpy as np
import umap


class UmapProjector:
    @staticmethod
    def project(embeddings: np.ndarray) -> np.ndarray:
        n_neighbors = min(15, len(embeddings) - 1)
        reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=n_neighbors)
        return reducer.fit_transform(embeddings)

    @staticmethod
    def project_with_metadata(
        embeddings: np.ndarray,
        labels: list[int],
        texts: list[str],
    ) -> list[dict]:
        projection = UmapProjector.project(embeddings)
        points = []
        for i in range(len(texts)):
            points.append({
                "x": float(projection[i, 0]),
                "y": float(projection[i, 1]),
                "cluster": labels[i],
                "text": texts[i],
            })
        return points
