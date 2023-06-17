from typing import Dict

from fastapi import Depends, FastAPI

from src.config import Settings, get_settings

app = FastAPI()


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    return {
        "ping": "Yatta!",
        "environment": settings.environment,
        "testing": settings.testing,  # type: ignore
    }
