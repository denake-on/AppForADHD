from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import sys

from sqlalchemy.orm import Session
from sqlalchemy import text

# 确保项目根目录在导入路径中
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.database import engine, DATA_DIR
from backend.models import Base, Task, TaskStatus, TaskPriority



def create_schema() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def add_task(
    session: Session,
    title: str,
    description: str | None = None,
    deadline: date | None = None,
    status: TaskStatus = TaskStatus.NOT_STARTED,
    priority: TaskPriority = TaskPriority.MEDIUM,
    progress: int = 0,
    parent_id: int | None = None,
) -> Task:
    # 计算层级：无父为 1，有父则父的 level + 1
    parent_level = None
    if parent_id is not None:
        parent_level = session.execute(
            text("SELECT level FROM tasks WHERE id = :pid"),
            {"pid": parent_id},
        ).scalar()
        parent_level = parent_level or 1

    task = Task(
        title=title,
        description=description,
        deadline=deadline,
        status=status,
        priority=priority,
        progress_percent=progress,
        parent_id=parent_id,
        level=(parent_level + 1) if parent_level else 1,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def seed_example() -> None:
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    with SessionLocal() as session:
        ##########################################
        # 大任务1
        ##########################################
        project = add_task(
            session,
            title="发布 v1.0",
            description="版本发布大任务",
            deadline=date.today() + timedelta(days=14),
            status=TaskStatus.IN_PROGRESS,
            progress=20,
        )

        # 子任务（deadline 参照父任务，可按比例/缓冲期自行计算）
        design = add_task(
            session,
            title="设计评审",
            deadline=project.deadline and project.deadline - timedelta(days=10),
            parent_id=project.id,
            status=TaskStatus.DONE,
            progress=100,
        )
        dev = add_task(
            session,
            title="功能开发",
            deadline=project.deadline and project.deadline - timedelta(days=4),
            parent_id=project.id,
            status=TaskStatus.IN_PROGRESS,
            progress=50,
        )
        test = add_task(
            session,
            title="测试验收",
            deadline=project.deadline and project.deadline - timedelta(days=1),
            parent_id=project.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )

        # 三级子任务
        add_task(
            session,
            title="单元测试",
            deadline=dev.deadline and dev.deadline - timedelta(days=2),
            parent_id=dev.id,
            status=TaskStatus.IN_PROGRESS,
            progress=30,
        )
        add_task(
            session,
            title="集成测试",
            deadline=dev.deadline and dev.deadline - timedelta(days=1),
            parent_id=dev.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        ##########################################
        # 追加大任务 2：网站改版
        ##########################################
        revamp = add_task(
            session,
            title="网站改版",
            description="首页与详情页重构",
            deadline=date.today() + timedelta(days=21),
            status=TaskStatus.IN_PROGRESS,
            progress=40,
        )
        ui = add_task(
            session,
            title="UI 设计",
            deadline=revamp.deadline and revamp.deadline - timedelta(days=14),
            parent_id=revamp.id,
            status=TaskStatus.IN_PROGRESS,
            progress=60,
        )
        fe = add_task(
            session,
            title="前端实现",
            deadline=revamp.deadline and revamp.deadline - timedelta(days=5),
            parent_id=revamp.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        be = add_task(
            session,
            title="后端接口联调",
            deadline=revamp.deadline and revamp.deadline - timedelta(days=3),
            parent_id=revamp.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        # 三级子任务（前端实现）
        add_task(
            session,
            title="组件开发",
            deadline=fe.deadline and fe.deadline - timedelta(days=3),
            parent_id=fe.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        add_task(
            session,
            title="样式适配",
            deadline=fe.deadline and fe.deadline - timedelta(days=1),
            parent_id=fe.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        ##########################################
        # 追加大任务 3：数据迁移
        ##########################################
        migrate = add_task(
            session,
            title="数据迁移",
            description="从老库迁移到新库",
            deadline=date.today() + timedelta(days=10),
            status=TaskStatus.IN_PROGRESS,
            progress=35,
        )
        assess = add_task(
            session,
            title="评估与映射",
            deadline=migrate.deadline and migrate.deadline - timedelta(days=8),
            parent_id=migrate.id,
            status=TaskStatus.DONE,
            progress=100,
        )
        tooling = add_task(
            session,
            title="迁移脚本编写",
            deadline=migrate.deadline and migrate.deadline - timedelta(days=4),
            parent_id=migrate.id,
            status=TaskStatus.IN_PROGRESS,
            progress=40,
        )
        verify = add_task(
            session,
            title="校验与回滚预案",
            deadline=migrate.deadline and migrate.deadline - timedelta(days=1),
            parent_id=migrate.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )

        ##########################################
        # 追加大任务 4：市场推广
        ##########################################
        marketing = add_task(
            session,
            title="市场推广",
            description="版本上线后的市场投放",
            deadline=date.today() + timedelta(days=30),
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        channels = add_task(
            session,
            title="渠道选择",
            deadline=marketing.deadline and marketing.deadline - timedelta(days=20),
            parent_id=marketing.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        creatives = add_task(
            session,
            title="素材制作",
            deadline=marketing.deadline and marketing.deadline - timedelta(days=12),
            parent_id=marketing.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )
        launch = add_task(
            session,
            title="投放与监控",
            deadline=marketing.deadline and marketing.deadline - timedelta(days=2),
            parent_id=marketing.id,
            status=TaskStatus.NOT_STARTED,
            progress=0,
        )


if __name__ == "__main__":
    create_schema()
    seed_example()
    print(f"Database initialized at: {Path(DATA_DIR) / 'database.db'}")


