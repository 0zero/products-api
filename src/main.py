from logging import INFO, basicConfig, getLogger

from fastapi import FastAPI

from src.routers import organisation, ping, product

logger = getLogger(__name__)
basicConfig(level=INFO)


def get_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Supplies Demo",
    )
    app.include_router(ping.router)
    app.include_router(product.router)
    app.include_router(organisation.router)
    return app


app = get_app()


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Shutting down...")
