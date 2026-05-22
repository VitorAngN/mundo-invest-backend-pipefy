from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import clientes, webhooks


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mundo Invest - Client Management & Pipefy Integration",
        version="0.1.0",
        description="API para cadastro de clientes e simulacao de integracao Pipefy via GraphQL.",
        lifespan=lifespan,
    )

    app.include_router(clientes.router)
    app.include_router(webhooks.router)

    @app.get("/health", tags=["health"])
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
