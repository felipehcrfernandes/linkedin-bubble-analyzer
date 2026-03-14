import numpy as np

from backend.visualization.chart_builder import ChartBuilder
from backend.visualization.umap_projector import UmapProjector


class VisualizationService:
    @staticmethod
    def generate_all_charts(
        embeddings: np.ndarray,
        labels: list[int],
        texts: list[str],
        cluster_summary: list[dict],
        bubble_score: dict,
    ) -> dict[str, str]:
        points = UmapProjector.project_with_metadata(embeddings, labels, texts)
        topic_map = ChartBuilder.topic_map(points)
        distribution_chart = ChartBuilder.distribution_chart(cluster_summary)
        bubble_indicator = ChartBuilder.bubble_indicator(
            score=bubble_score["score"],
            interpretation=bubble_score["interpretation"],
        )
        return {
            "topic_map": topic_map,
            "distribution_chart": distribution_chart,
            "bubble_indicator": bubble_indicator,
        }
