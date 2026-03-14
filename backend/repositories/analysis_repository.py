import json

from sqlalchemy.orm import Session

from backend.core.exceptions import AnalysisNotFoundError
from backend.models.analysis import Analysis


class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_analysis(self, dataset_id: int, result: dict) -> None:
        existing = (
            self.db.query(Analysis)
            .filter(Analysis.dataset_id == dataset_id)
            .first()
        )
        if existing:
            existing.result_json = json.dumps(result)
        else:
            analysis = Analysis(
                dataset_id=dataset_id,
                result_json=json.dumps(result),
            )
            self.db.add(analysis)
        self.db.commit()

    def load_analysis(self, dataset_id: int) -> dict:
        analysis = (
            self.db.query(Analysis)
            .filter(Analysis.dataset_id == dataset_id)
            .first()
        )
        if not analysis:
            raise AnalysisNotFoundError(dataset_id)
        return json.loads(analysis.result_json)
