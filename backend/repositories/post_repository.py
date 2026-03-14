from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.core.exceptions import PostsNotFoundError
from backend.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def next_dataset_id(self) -> int:
        max_id = self.db.query(func.max(Post.dataset_id)).scalar()
        return (max_id or 0) + 1

    def save_posts(self, dataset_id: int, posts: list[dict]) -> int:
        for post_data in posts:
            post = Post(
                dataset_id=dataset_id,
                author=post_data["author"],
                content=post_data["content"],
                cleaned_text=post_data.get("cleaned_text"),
                date=post_data.get("date"),
            )
            self.db.add(post)
        self.db.commit()
        return dataset_id

    def load_posts(self, dataset_id: int) -> list[dict]:
        posts = self.db.query(Post).filter(Post.dataset_id == dataset_id).all()
        if not posts:
            raise PostsNotFoundError(dataset_id)
        return [
            {
                "author": p.author,
                "content": p.content,
                "cleaned_text": p.cleaned_text,
                "date": p.date,
            }
            for p in posts
        ]

    def list_datasets(self) -> list[int]:
        rows = self.db.query(Post.dataset_id).distinct().all()
        return [r[0] for r in rows]
