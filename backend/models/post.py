from sqlalchemy import Column, Integer, String, Text

from backend.models.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    cleaned_text = Column(Text, nullable=True)
    date = Column(String, nullable=True)
