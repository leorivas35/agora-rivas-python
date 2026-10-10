from agora_rivas.application.use_cases.create_user import CreateUser
from agora_rivas.infrastructure.database.in_memory_user_repository import InMemoryUserRepository


def build_create_user_use_case() -> CreateUser:
    repository = InMemoryUserRepository()
    return CreateUser(repository)
