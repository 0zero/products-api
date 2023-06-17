from fastapi import FastAPI, Depends

from src.config import get_settings, Settings


app = FastAPI()


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "Yatta!",
        "environment": settings.environment,
        "testing": settings.testing
    }