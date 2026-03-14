from sqlalchemy import Column, Integer, Text

from backend.models.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, nullable=False, unique=True, index=True)
    result_json = Column(Text, nullable=False)
