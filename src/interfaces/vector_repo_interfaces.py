from abc import ABC, abstractmethod
from src.models.vector_model import VectorModel

class VectorRepoInterface(ABC):
    @abstractmethod
    def get_news_vector(self, user_message: str) -> VectorModel | None:
        """Find a news vector by its news text. Returns None if not found"""
        pass