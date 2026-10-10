from agora_rivas.application.dto.user_dto import CreateUserInput
from agora_rivas.application.use_cases.create_user import CreateUser
from agora_rivas.infrastructure.database.in_memory_user_repository import InMemoryUserRepository


def test_create_user_success() -> None:
    repo = InMemoryUserRepository()
    use_case = CreateUser(repo)

    result = use_case.execute(CreateUserInput(name="Alice", email="alice@example.com"))

    assert result.name == "Alice"
    assert result.email == "alice@example.com"
    assert repo.get_by_id("user-1") is not None
