from agora_rivas.application.interfaces.user_repository import UserRepository
from agora_rivas.domain.entities.user import User


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def get_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)
