from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import Optional

from sqlalchemy import Integer, String, DateTime, Date, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# 从 database 模块导入 Base
from backend.database import Base

# 定义任务的三种状态
class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"  # 添加取消状态

# 定义任务优先级
class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    __tablename__ = "tasks"  # 数据库的表名

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus), 
        nullable=False, 
        default=TaskStatus.NOT_STARTED
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority), 
        nullable=False, 
        default=TaskPriority.MEDIUM
    )
    progress_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # 任务层级：顶层为 1，子任务为 2，依次类推
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    # 父子层级：自引用父任务
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), 
        nullable=True
    )
    
    parent: Mapped[Optional["Task"]] = relationship(
        "Task", 
        remote_side="Task.id", 
        back_populates="children"
    )
    children: Mapped[list["Task"]] = relationship(
        "Task", 
        back_populates="parent", 
        cascade="all, delete-orphan"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

__all__ = ["Task", "TaskStatus", "TaskPriority"]