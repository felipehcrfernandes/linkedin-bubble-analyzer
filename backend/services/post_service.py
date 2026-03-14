from backend.processing.text_cleaner import clean_post
from backend.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def ingest_posts(self, posts: list[dict]) -> int:
        dataset_id = self.repository.next_dataset_id()
        cleaned_posts = [clean_post(post) for post in posts]
        self.repository.save_posts(dataset_id, cleaned_posts)
        return dataset_id

    def get_posts(self, dataset_id: int) -> list[dict]:
        return self.repository.load_posts(dataset_id)

    def list_datasets(self) -> list[int]:
        return self.repository.list_datasets()
