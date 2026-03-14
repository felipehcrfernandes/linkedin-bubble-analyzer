from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LinkedIn Bubble Analyzer"
    debug: bool = False
    database_url: str = "sqlite:///./bubble_analyzer.db"
    embedding_model: str = "all-MiniLM-L6-v2"
    default_n_clusters: int = 5
    simhash_distance_threshold: int = 10
    cosine_similarity_threshold: float = 0.8

    model_config = {"env_prefix": "BUBBLE_"}


settings = Settings()
