import json
from dataclasses import asdict

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from agora_rivas.application.dto.user_dto import CreateUserInput
from agora_rivas.bootstrap.container import build_create_user_use_case
from agora_rivas.domain.exceptions import DomainError


@require_GET
def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


@require_POST
def create_user(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Request body must be valid JSON."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"detail": "Request body must be a JSON object."}, status=400)

    name = payload.get("name")
    email = payload.get("email")
    if not isinstance(name, str) or not isinstance(email, str):
        return JsonResponse({"detail": "'name' and 'email' must be strings."}, status=400)

    try:
        output = build_create_user_use_case().execute(CreateUserInput(name=name, email=email))
    except (DomainError, ValueError) as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    return JsonResponse(asdict(output))
