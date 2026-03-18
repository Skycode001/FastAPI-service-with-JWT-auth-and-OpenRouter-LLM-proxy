from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_auth, routes_chat
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        lifespan=lifespan
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(routes_auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(routes_chat.router, prefix="/chat", tags=["Chat"])

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "environment": settings.ENV}

    return app

app = create_app()