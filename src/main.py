from logging import INFO, basicConfig, getLogger
from fastapi import FastAPI
from src.routers import ping

logger = getLogger(__name__)
basicConfig(level=INFO)

def get_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Supplies Demo",
    )
    app.include_router(ping.router)
    return app

app = get_app()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")