"""数据库模块"""
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from .init_db import get_db_path

# 先创建 Base
Base = declarative_base()

# 获取数据库路径（使用统一的 get_db_path 函数）
DB_PATH = get_db_path()

# 创建 SQLAlchemy engine
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# 创建 SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """获取数据库会话（用于依赖注入）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 在 Base 创建后导入模型（避免循环导入）
from backend.models import Task, TaskStatus, TaskPriority

# 创建所有表
Base.metadata.create_all(bind=engine)

__all__ = [
    'get_db_path',
    'get_db', 
    'engine', 
    'SessionLocal', 
    'Base',
    'Task',
    'TaskStatus',
    'TaskPriority'
]