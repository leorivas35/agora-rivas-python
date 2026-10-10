# Clean Architecture for a Python Project

## Goal

Keep business rules independent from frameworks, databases, and delivery mechanisms. The system should be organized so that the core domain can evolve without being tightly coupled to FastAPI, SQLAlchemy, CLI tooling, or external services.

## Core principle: dependencies point inward

The cleanest dependency direction is:

- Domain -> independent
- Application -> depends on Domain
- Infrastructure -> implements interfaces defined by the inner layers
- Interfaces/API -> adapts external input and output
- Bootstrap -> wires everything together

In practical terms:

- The `domain` layer should not know about HTTP, databases, or ORMs.
- The `application` layer should not know how persistence is implemented.
- The `infrastructure` layer may depend on domain and application contracts.
- The `interfaces` layer should stay thin and focused on transport details.

---

## Recommended project structure

```text
project_root/
├─ src/
│  └─ my_app/
│     ├─ domain/
│     │  ├─ __init__.py
│     │  ├─ entities/
│     │  │  ├─ __init__.py
│     │  │  └─ user.py
│     │  ├─ value_objects/
│     │  │  ├─ __init__.py
│     │  │  └─ email.py
│     │  ├─ repositories/
│     │  │  ├─ __init__.py
│     │  │  └─ user_repository.py
│     │  ├─ services/
│     │  │  ├─ __init__.py
│     │  │  └─ user_policy.py
│     │  └─ exceptions.py
│     │
│     ├─ application/
│     │  ├─ __init__.py
│     │  ├─ interfaces/
│     │  │  ├─ __init__.py
│     │  │  └─ user_repository.py
│     │  ├─ use_cases/
│     │  │  ├─ __init__.py
│     │  │  ├─ create_user.py
│     │  │  └─ get_user.py
│     │  ├─ dto/
│     │  │  ├─ __init__.py
│     │  │  └─ user_dto.py
│     │  └─ services/
│     │     ├─ __init__.py
│     │     └─ user_service.py
│     │
│     ├─ infrastructure/
│     │  ├─ __init__.py
│     │  ├─ database/
│     │  │  ├─ __init__.py
│     │  │  ├─ models.py
│     │  │  └─ user_repository_impl.py
│     │  ├─ config/
│     │  │  └─ settings.py
│     │  ├─ external/
│     │  │  └─ email_client.py
│     │  └─ persistence/
│     │     └─ session.py
│     │
│     ├─ interfaces/
│     │  ├─ __init__.py
│     │  ├─ api/
│     │  │  ├─ __init__.py
│     │  │  ├─ routes.py
│     │  │  └─ schemas.py
│     │  └─ cli/
│     │     └─ commands.py
│     │
│     ├─ bootstrap/
│     │  ├─ __init__.py
│     │  └─ container.py
│     │
│     └─ main.py
│
├─ tests/
│  ├─ unit/
│  │  ├─ domain/
│  │  └─ application/
│  ├─ integration/
│  │  └─ infrastructure/
│  └─ e2e/
│
├─ pyproject.toml
├─ requirements.txt
├─ README.md
├─ .env.example
├─ Makefile
└─ .gitignore
```

---

## Layer responsibilities

### 1) Domain layer

This is the heart of the system. It should contain:

- entities
- value objects
- domain rules
- repository interfaces
- domain exceptions

This layer should be framework-agnostic. It should not import:

- FastAPI
- Flask
- SQLAlchemy
- Django models
- HTTP request/response classes

Example:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: str
    email: str
    name: str

    def change_email(self, new_email: str) -> None:
        if "@" not in new_email:
            raise ValueError("Invalid email")
        object.__setattr__(self, "email", new_email)
```

This is valid domain logic because it is about the business rule, not the transport layer or persistence layer.

---

### 2) Application layer

This layer orchestrates use cases. It contains:

- use cases
- DTOs
- application services
- interfaces to infrastructure

This is the place where features are implemented as actions the system can do.

Example:

```python
from my_app.domain.repositories.user_repository import UserRepository
from my_app.domain.entities.user import User

class CreateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, name: str, email: str) -> User:
        user = User(id="generated-id", name=name, email=email)
        self.user_repository.save(user)
        return user
```

The use case knows what the system does, but not how it is stored or transported.

---

### 3) Infrastructure layer

This is where implementation details live:

- database access
- ORMs
- file storage
- API clients
- message brokers
- config loading
- email integration

Example repository implementation:

```python
from my_app.application.interfaces.user_repository import UserRepository
from my_app.domain.entities.user import User

class SqlUserRepository(UserRepository):
    def save(self, user: User) -> None:
        # insert into database
        pass
```

This layer can depend on abstractions defined by the inner layers, but it should not contain business logic.

---

### 4) Interface layer

This layer exposes the app through a delivery mechanism:

- REST API routes
- CLI commands
- GraphQL endpoints
- background job handlers
- UI adapters

Example FastAPI route:

```python
from fastapi import APIRouter
from my_app.application.use_cases.create_user import CreateUser

router = APIRouter()

@router.post("/users")
async def create_user(payload: dict):
    use_case = CreateUser(user_repository=my_repository)
    return use_case.execute(payload["name"], payload["email"])
```

The route should be thin. It should adapt incoming HTTP data to application-level operations.

---

### 5) Bootstrap / composition root

This is where dependencies are assembled. It is the place where the application tells the system which concrete implementations to use.

Example:

```python
from my_app.infrastructure.database.user_repository_impl import SqlUserRepository
from my_app.application.use_cases.create_user import CreateUser


def build_create_user_use_case() -> CreateUser:
    repo = SqlUserRepository()
    return CreateUser(repo)
```

This is the application’s wiring layer. It should exist in one clearly defined place.

---

## Practical rules to follow

### 1) Keep business rules in the domain

If validation, policy, or rules affect the business, they belong in the domain or application layers, not in API handlers.

### 2) Depend on abstractions, not implementations

Use interfaces for repository contracts and external service boundaries.

### 3) Do not leak framework types into the core

Avoid passing database models or HTTP objects deep into the business logic.

### 4) Prefer thin controllers and routers

Routes should adapt input/output; not implement business logic.

### 5) Keep a clear dependency direction

Inner layers should not depend on outer layers.

---

## Common anti-patterns to avoid

- Putting business logic in API routes
- Writing ORM models directly as domain entities
- Having one `models.py` file that mixes everything
- Creating a giant `services.py` module with random logic
- Letting the database layer control the business rules

---

## Testing strategy

### Unit tests

Test:

- domain entities
- value objects
- use cases
- business rules

### Integration tests

Test:

- database repository implementations
- API integration with test database
- external service adapters in controlled environments

### E2E tests

Test:

- full user flows through the application interface

This structure keeps the most valuable logic independent and testable.

---

## Recommended Python technology stack for this structure

A common and practical stack is:

- FastAPI for web interfaces
- SQLAlchemy or SQLModel for persistence
- Pydantic for DTO validation
- pytest for testing
- dataclasses or Pydantic models for domain entities
- dependency injection container or factory functions for wiring

---

## Final recommendation

The simplest clean architecture rule to remember is:

- Domain: what is true
- Application: what the system does
- Infrastructure: how it is implemented
- Interface: how users or systems access it
- Bootstrap: how everything is wired together

This keeps the project maintainable, testable, and resilient to changing frameworks.

---

## Suggested root-level folder

A strong root-level choice is:

```text
docs/
```

This keeps architecture documentation separated from application code and makes it easy to add more project-level documentation later, such as:

- `docs/architecture/`
- `docs/development/`
- `docs/api/`
- `docs/testing/`

If the project grows, `docs/architecture/` is the most organized long-term folder.
