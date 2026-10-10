from agora_rivas.application.dto.user_dto import CreateUserInput, UserOutput
from agora_rivas.application.interfaces.user_repository import UserRepository
from agora_rivas.domain.entities.user import User


class CreateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, payload: CreateUserInput) -> UserOutput:
        user = User(id="user-1", name=payload.name, email=payload.email)
        self.user_repository.save(user)
        return UserOutput(id=user.id, name=user.name, email=user.email)
