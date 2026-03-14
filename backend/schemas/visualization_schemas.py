from pydantic import BaseModel


class VisualizationResponse(BaseModel):
    dataset_id: int
    topic_map: str
    distribution_chart: str
    bubble_indicator: str
