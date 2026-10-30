from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as research_router


def create_app() -> FastAPI:
    """
    FastAPI application factory.
    """
    app = FastAPI(
        title="AI Multi-Agent Research Assistant API",
        version="1.0.0",
        description="Clean Architecture LangGraph Multi-Agent Research Assistant backend",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(research_router, prefix="/api")

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok", "service": "research-assistant-backend"}

    return app


app = create_app()

