from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .welcomePage.greeting import router as greeting_router
from .welcomePage.progress import router as progress_router
from .welcomePage.tasks import router as tasks_router
from .welcomePage.my_calendar import router as calendar_router
from .task.routes import router as task_router


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager EXE Backend", version="0.1.0")

    # Allow frontend dev server to call APIs
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(greeting_router)
    app.include_router(progress_router)
    app.include_router(tasks_router)
    app.include_router(calendar_router)
    app.include_router(task_router)

    @app.get("/health")
    def health_check() -> dict:
        return {"status": "ok"}

    return app


app = create_app()

# Run with: uvicorn backend.main:app --reload --port 8000
