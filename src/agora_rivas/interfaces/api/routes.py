from fastapi import APIRouter

from agora_rivas.application.dto.user_dto import CreateUserInput
from agora_rivas.bootstrap.container import build_create_user_use_case

router = APIRouter()


@router.post("/users")
async def create_user(payload: CreateUserInput):
    use_case = build_create_user_use_case()
    return use_case.execute(payload)
