import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Agora Rivas API"
    api_prefix: str = "/api"
    debug: bool = False


def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Agora Rivas API"),
        api_prefix=os.getenv("API_PREFIX", "/api"),
        debug=os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"},
    )
