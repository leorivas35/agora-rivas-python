from abc import ABC, abstractmethod

from agora_rivas.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        """Persist a user."""

    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None:
        """Return a user stored under the given ID."""
