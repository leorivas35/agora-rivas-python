from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserInput:
    name: str
    email: str


@dataclass(frozen=True)
class UserOutput:
    id: str
    name: str
    email: str
