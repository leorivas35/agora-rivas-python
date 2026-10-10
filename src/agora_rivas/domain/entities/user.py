from dataclasses import dataclass

from agora_rivas.domain.exceptions import InvalidEmailError


@dataclass(frozen=True)
class User:
    id: str
    name: str
    email: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Name cannot be empty.")
        if "@" not in self.email:
            raise InvalidEmailError("Email must contain an '@' symbol.")

    def rename(self, new_name: str) -> "User":
        if not new_name.strip():
            raise ValueError("Name cannot be empty.")
        return User(id=self.id, name=new_name.strip(), email=self.email)
