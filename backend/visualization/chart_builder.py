import json

import plotly.graph_objects as go


class ChartBuilder:
    @staticmethod
    def topic_map(points: list[dict]) -> str:
        clusters = sorted(set(p["cluster"] for p in points))
        fig = go.Figure()
        for cluster_id in clusters:
            cluster_points = [p for p in points if p["cluster"] == cluster_id]
            fig.add_trace(go.Scatter(
                x=[p["x"] for p in cluster_points],
                y=[p["y"] for p in cluster_points],
                mode="markers",
                name=f"Cluster {cluster_id}",
                text=[p["text"] for p in cluster_points],
                hovertemplate="%{text}<extra></extra>",
            ))
        fig.update_layout(
            title="Topic Map (UMAP Projection)",
            xaxis_title="UMAP 1",
            yaxis_title="UMAP 2",
        )
        return fig.to_json()

    @staticmethod
    def distribution_chart(cluster_summary: list[dict]) -> str:
        labels = [
            f"Cluster {s['cluster_id']}: {', '.join(s['top_words'][:3])}"
            for s in cluster_summary
        ]
        values = [s["proportion"] for s in cluster_summary]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title="Topic Distribution")
        return fig.to_json()

    @staticmethod
    def bubble_indicator(score: float, interpretation: str) -> str:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": f"Bubble Score: {interpretation}"},
            gauge={
                "axis": {"range": [0, 1]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 0.3], "color": "red"},
                    {"range": [0.3, 0.6], "color": "yellow"},
                    {"range": [0.6, 1.0], "color": "green"},
                ],
            },
        ))
        fig.update_layout(title="Feed Diversity Score")
        return fig.to_json()
