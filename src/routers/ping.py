from typing import Dict

from fastapi import APIRouter, Depends

from src.config import Settings, get_settings

router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    return {
        "ping": "Yatta!",
        "environment": settings.environment,
        "testing": settings.testing,  # type: ignore
    }
