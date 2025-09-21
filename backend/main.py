from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import get_settings
from routers.students import router as students_router
from routers.analytics import router as analytics_router
from routers.chat import router as chat_router
from routers.auth import router as auth_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="AI Campus Admin Agent", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=settings.get_cors_methods(),
        allow_headers=settings.get_cors_headers(),
    )

    app.include_router(auth_router, tags=["auth"])
    app.include_router(students_router, prefix="/students", tags=["students"])
    app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
    app.include_router(chat_router, tags=["chat"])

    @app.get("/")
    async def root():
        return {"message": "AI Campus Admin Agent API"}

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

