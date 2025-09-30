from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path


# 修复打包环境下的导入问题
try:
    # 开发环境下（相对导入）
    from .welcomePage.greeting import router as greeting_router
    from .welcomePage.progress import router as progress_router
    from .welcomePage.tasks import router as tasks_router
    from .welcomePage.my_calendar import router as calendar_router
    from .task.routes import router as task_router
except ImportError:
    # 打包环境下（绝对导入）
    from backend.welcomePage.greeting import router as greeting_router
    from backend.welcomePage.progress import router as progress_router
    from backend.welcomePage.tasks import router as tasks_router
    from backend.welcomePage.my_calendar import router as calendar_router
    from backend.task.routes import router as task_router


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

    # 检查dist目录是否存在，如果存在则提供静态文件服务
    # 支持打包后的路径
    dist_paths = [
        Path(__file__).parent.parent / "frontend" / "dist",  # 开发环境
        Path(__file__).parent / "dist",  # 打包环境
        Path.cwd() / "dist",  # 当前工作目录
    ]
    
    dist_path = None
    for path in dist_paths:
        if path.exists():
            dist_path = path
            break
    
    if dist_path:
        print(f"找到前端文件目录: {dist_path}")
        app.mount("/", StaticFiles(directory=dist_path, html=True), name="frontend")
    else:
        print("警告: 未找到前端文件目录，将只提供API服务")

    @app.get("/health")
    def health_check() -> dict:
        return {"status": "ok"}

    # 添加根路径路由，如果存在静态文件则返回静态文件，否则返回API信息
    @app.get("/")
    def read_root():
        if dist_path.exists():
            # 如果是打包后的exe，返回静态文件
            return {"message": "WeiWan App running in exe mode"}
        else:
            # 如果是开发模式，返回API信息
            return {"message": "Welcome to WeiWan App API", "docs": "/docs"}

    return app


app = create_app()

# Run with: uvicorn backend.main:app --reload --port 8000
