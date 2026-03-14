class BubbleAnalyzerError(Exception):
    """Base exception for the application."""


class PostsNotFoundError(BubbleAnalyzerError):
    """Raised when a dataset of posts is not found."""

    def __init__(self, dataset_id: int):
        self.dataset_id = dataset_id
        super().__init__(f"Dataset '{dataset_id}' not found")


class AnalysisNotFoundError(BubbleAnalyzerError):
    """Raised when an analysis result is not found."""

    def __init__(self, dataset_id: int):
        self.dataset_id = dataset_id
        super().__init__(f"Analysis for dataset '{dataset_id}' not found")


class InsufficientDataError(BubbleAnalyzerError):
    """Raised when there is not enough data to perform analysis."""

    def __init__(self, message: str = "Not enough posts to perform analysis"):
        super().__init__(message)
