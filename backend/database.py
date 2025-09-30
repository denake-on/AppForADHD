import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

def get_base_path():
    """获取应用基础路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        return os.path.dirname(sys.executable)
    else:
        # 开发环境路径
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库文件路径
base_path = get_base_path()
data_dir = os.path.join(base_path, 'backend', 'data')
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, 'database.db')

DATABASE_URL = f"sqlite:///{db_path}"

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


