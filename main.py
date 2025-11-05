import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback
import sqlite3

app = FastAPI()

try:
    from backend.database.init_db import init_database
    init_database()
    print("✅ 数据库初始化完成")
except Exception as e:
    print(f"❌ 数据库初始化失败: {e}")
    import traceback
    traceback.print_exc()

# 添加全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    print(f"❌ 异常发生: {request.url}")
    print(f"❌ 错误信息: {str(exc)}")
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "detail": "服务器内部错误",
            "path": str(request.url)
        }
    )

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取数据库路径
def get_db_path():
    """获取数据库路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        base_path = Path(sys._MEIPASS)
    else:
        # 开发环境路径
        base_path = Path(__file__).parent
    
    return base_path / "backend" / "data" / "database.db"

# 获取前端文件路径
def get_frontend_path():
    """获取前端文件路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        return Path(sys._MEIPASS) / 'frontend' / 'dist'
    else:
        # 开发环境路径
        project_root = Path(__file__).parent
        # 优先使用构建后的 dist 目录
        dist_path = project_root / 'frontend' / 'dist'
        if dist_path.exists():
            return dist_path
        # 否则返回 frontend 根目录
        return project_root / 'frontend'

# 挂载静态文件
frontend_path = get_frontend_path()
print(f"🔍 前端路径: {frontend_path}")
print(f"🔍 路径是否存在: {frontend_path.exists()}")

if frontend_path.exists():
    # 挂载所有静态资源
    app.mount("/assets", StaticFiles(directory=frontend_path / "assets"), name="assets")
else:
    print(f"⚠️  警告: 前端目录不存在: {frontend_path}")

# 导入 API 路由
try:
    from backend.task.routes import router as task_router
    app.include_router(task_router)
    print("✅ 已加载 task 路由")
except ImportError as e:
    print(f"⚠️  未找到 task 路由: {e}")
except Exception as e:
    print(f"❌ 加载 task 路由失败: {e}")
    traceback.print_exc()

try:
    from backend.welcomePage.greeting import router as greeting_router
    app.include_router(greeting_router, prefix="/api/greeting", tags=["greeting"])
    print("✅ 已加载 greeting 路由")
except ImportError as e:
    print(f"⚠️  未找到 greeting 路由: {e}")

try:
    from backend.welcomePage.my_calendar import router as calendar_router
    app.include_router(calendar_router, prefix="/api/calendar", tags=["calendar"])
    print("✅ 已加载 calendar 路由")
except ImportError as e:
    print(f"⚠️  未找到 calendar 路由: {e}")

try:
    from backend.welcomePage.progress import router as progress_router
    app.include_router(progress_router, prefix="/api/progress", tags=["progress"])
    print("✅ 已加载 progress 路由")
except ImportError as e:
    print(f"⚠️  未找到 progress 路由: {e}")

try:
    from backend.welcomePage.tasks import router as welcome_tasks_router
    app.include_router(welcome_tasks_router, prefix="/api/welcome/tasks", tags=["welcome-tasks"])
    print("✅ 已加载 welcome tasks 路由")
except ImportError as e:
    print(f"⚠️  未找到 welcome tasks 路由: {e}")

@app.get("/")
async def read_root():
    """返回前端首页"""
    index_path = frontend_path / "index.html"
    
    if not frontend_path.exists():
        return {
            "error": "前端文件不存在", 
            "path": str(frontend_path),
            "cwd": os.getcwd()
        }
    
    if not index_path.exists():
        return {
            "error": "index.html 不存在", 
            "path": str(index_path),
            "files": [f.name for f in frontend_path.iterdir()] if frontend_path.exists() else []
        }
    
    return FileResponse(index_path)

@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "frontend_path": str(frontend_path),
        "frontend_exists": frontend_path.exists()
    }

@app.get("/api/debug/routes")
async def debug_routes():
    """调试：列出所有路由"""
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    return {"routes": routes}

@app.get("/api/completion")
async def get_completion():
    """获取任务完成度统计"""
    try:
        db_path = get_db_path()
        
        if not db_path.exists():
            print(f"❌ 数据库文件不存在: {db_path}")
            return {"todo": 0, "in_progress": 0, "done": 0, "cancelled": 0}
        
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            stats = conn.execute(
                """
                SELECT status, COUNT(*) as count
                FROM tasks
                GROUP BY status
                """
            ).fetchall()
            
            result = {
                "todo": 0,
                "in_progress": 0,
                "done": 0,
                "cancelled": 0
            }
            
            for row in stats:
                status = row["status"]
                count = row["count"]
                if status == "TODO":
                    result["todo"] = count
                elif status == "IN_PROGRESS":
                    result["in_progress"] = count
                elif status == "DONE":
                    result["done"] = count
                elif status == "CANCELLED":
                    result["cancelled"] = count
            
            print(f"✅ Completion 统计: {result}")
            return result
            
    except Exception as e:
        print(f"❌ 获取 completion 失败: {e}")
        traceback.print_exc()
        return {"todo": 0, "in_progress": 0, "done": 0, "cancelled": 0}

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """处理前端路由"""
    if full_path.startswith("api/"):
        return {"error": "API endpoint not found"}
    
    file_path = frontend_path / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    
    return {
        "error": "文件不存在", 
        "path": str(file_path),
        "requested": full_path
    }

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time
    
    def open_browser():
        time.sleep(2)
        try:
            print("🌐 正在打开浏览器...")
            webbrowser.open('http://127.0.0.1:8000')
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
    
    print("=" * 50)
    print("🚀 AppForADHD 启动中...")
    print("=" * 50)
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("👋 应用已关闭")
        print("=" * 50)