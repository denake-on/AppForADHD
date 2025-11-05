"""数据库初始化模块"""
import sys
from pathlib import Path
from datetime import datetime, timedelta


def get_db_path():
    """获取数据库路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        base_path = Path(sys._MEIPASS)
    else:
        # 开发环境路径
        base_path = Path(__file__).resolve().parents[1]
    
    db_path = base_path / "data" / "database.db"
    
    # 确保数据目录存在
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    return db_path


def init_database():
    """初始化数据库表结构"""
    db_path = get_db_path()
    
    print(f"🔍 数据库路径: {db_path}")
    print(f"🔍 数据库目录: {db_path.parent}")
    print(f"🔍 目录是否存在: {db_path.parent.exists()}")
    
    # 使用 SQLAlchemy 创建表
    try:
        from backend.database import Base, engine, SessionLocal
        from backend.models import Task, TaskStatus, TaskPriority
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功（使用 SQLAlchemy）")
        
        # 检查是否需要插入示例数据
        with SessionLocal() as session:
            task_count = session.query(Task).count()
            
            if task_count == 0:
                print("📝 插入示例数据...")
                insert_sample_data_sqlalchemy(session)
            else:
                print(f"📊 当前任务数量: {task_count}")
                
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        raise


def insert_sample_data_sqlalchemy(session):
    """使用 SQLAlchemy 插入示例数据"""
    from backend.models import Task, TaskStatus, TaskPriority
    from datetime import date, timedelta
    
    # 大任务1：发布 v1.0
    project1 = Task(
        title="发布 v1.0",
        description="版本发布大任务",
        deadline=date.today() + timedelta(days=14),
        status=TaskStatus.NOT_STARTED,
        priority=TaskPriority.HIGH,
        level=1
    )
    session.add(project1)
    session.flush()  # 获取 ID
    
    # 子任务
    design = Task(
        title="设计评审",
        deadline=date.today() + timedelta(days=4),
        status=TaskStatus.NOT_STARTED,
        priority=TaskPriority.MEDIUM,
        level=2,
        parent_id=project1.id
    )
    session.add(design)
    
    dev = Task(
        title="功能开发",
        deadline=date.today() + timedelta(days=10),
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH,
        progress_percent=30,
        level=2,
        parent_id=project1.id
    )
    session.add(dev)
    session.flush()
    
    # 三级子任务
    session.add(Task(
        title="单元测试",
        deadline=date.today() + timedelta(days=8),
        status=TaskStatus.NOT_STARTED,
        level=3,
        parent_id=dev.id
    ))
    
    session.add(Task(
        title="集成测试",
        deadline=date.today() + timedelta(days=9),
        status=TaskStatus.NOT_STARTED,
        level=3,
        parent_id=dev.id
    ))
    
    # 添加更多示例任务...
    project2 = Task(
        title="网站改版",
        description="首页与详情页重构",
        deadline=date.today() + timedelta(days=21),
        status=TaskStatus.NOT_STARTED,
        priority=TaskPriority.MEDIUM,
        level=1
    )
    session.add(project2)
    
    # 今日任务
    session.add(Task(
        title="今日紧急任务",
        description="测试今日完成度",
        deadline=date.today(),
        priority=TaskPriority.HIGH,
        level=1
    ))
    
    session.commit()
    print("✅ 示例数据插入成功")


if __name__ == "__main__":
    init_database()
    print(f"✅ 数据库初始化完成: {get_db_path()}")