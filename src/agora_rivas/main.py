from fastapi import FastAPI

from agora_rivas.infrastructure.config.settings import get_settings
from agora_rivas.interfaces.api.routes import router

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agora_rivas.main:app", host="0.0.0.0", port=8000, reload=settings.debug)
