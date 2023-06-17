from fastapi import APIRouter, Depends
from typing import Dict
from src.config import get_settings, Settings


router = APIRouter()

@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    return {
        "ping": "Yatta!",
        "environment": settings.environment,
        "testing": settings.testing,  # type: ignore
    }
