import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

def get_base_path():
    """获取应用基础路径"""
    # if getattr(sys, 'frozen', False):
    #     # 打包后的路径
    #     return os.path.dirname(sys.executable)
    if getattr(sys, 'frozen', False):
        # 打包后的路径：使用用户文档目录存储数据
        # 这样数据不会在程序目录下，避免权限问题
        app_data = os.path.join(os.path.expanduser('~'), 'AppForADHD')
        os.makedirs(app_data, exist_ok=True)
        return app_data
    else:
        # 开发环境路径
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库文件路径
base_path = get_base_path()
data_dir = os.path.join(base_path, 'data')
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, 'database.db')

DATABASE_URL = f"sqlite:///{db_path}"
DATA_DIR = Path(data_dir)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True))
Base = declarative_base()


def get_db(): # 获取数据库会话。使用 yield 返回数据库会话，确保在请求完成后关闭会话。
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


