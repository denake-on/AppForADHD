from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# 修复打包环境下的导入问题
try:
    # 开发环境下（相对导入）
    from ..models import Task, TaskStatus, TaskPriority
except ImportError:
    # 打包环境下（绝对导入）
    from backend.models import Task, TaskStatus, TaskPriority


def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None
) -> List[Task]:
    """
    获取任务列表，支持分页、状态筛选、优先级筛选和搜索
    """
    query = db.query(Task)
    
    # 应用状态筛选
    if status:
        query = query.filter(Task.status == status)
    
    # 应用优先级筛选
    if priority:
        query = query.filter(Task.priority == priority)
    
    # 搜索功能，按标题或描述搜索
    if search:
        query = query.filter(
            or_(
                Task.title.contains(search),
                Task.description.contains(search) if Task.description else False
            )
        )
    
    # 按创建时间倒序排列
    query = query.order_by(Task.created_at.desc())
    
    return query.offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """
    根据ID获取单个任务
    """
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(
    db: Session, 
    title: str, 
    description: Optional[str] = None, 
    deadline: Optional[date] = None,
    priority: TaskPriority = TaskPriority.MEDIUM,
    parent_id: Optional[int] = None,
    level: int = 1
) -> Task:
    """
    创建新任务
    """
    db_task = Task(
        title=title,
        description=description,
        deadline=deadline,
        priority=priority,
        parent_id=parent_id,
        level=level
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    deadline: Optional[date] = None,
    priority: Optional[TaskPriority] = None,
    status: Optional[TaskStatus] = None,
    progress_percent: Optional[int] = None,
    parent_id: Optional[int] = None,
    level: Optional[int] = None
) -> Optional[Task]:
    """
    更新任务信息
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    # 更新字段，只更新传入的参数
    if title is not None:
        db_task.title = title
    if description is not None:
        db_task.description = description
    if deadline is not None:
        db_task.deadline = deadline
    if priority is not None:
        db_task.priority = priority
    if status is not None:
        db_task.status = status
    if progress_percent is not None:
        db_task.progress_percent = progress_percent
    if parent_id is not None:
        db_task.parent_id = parent_id
    if level is not None:
        db_task.level = level
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    删除任务
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


def update_task_status(db: Session, task_id: int, status: TaskStatus) -> Optional[Task]:
    """
    专门用于更新任务状态的方法，同时更新父任务状态
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    # 记录旧状态，用于判断是否需要更新父任务
    old_status = db_task.status
    db_task.status = status
    
    # 更新父任务状态
    update_parent_task_status(db, db_task.parent_id, db_task.level)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def are_all_descendants_completed(db: Session, task_id: int) -> bool:
    """
    检查任务的所有后代（子任务、孙任务等）是否都已完成
    """
    # 获取所有后代任务
    descendants = get_all_descendants(db, task_id)
    
    # 检查是否所有后代都已完成
    for descendant in descendants:
        if descendant.status != TaskStatus.DONE:
            return False
    
    return True


def update_parent_task_status(db: Session, parent_id: Optional[int], child_level: int):
    """
    更新父任务状态：
    1. 如果子任务状态变为进行中或已完成，且父任务状态为未开始，则将父任务状态改为进行中
    2. 如果是level 1的任务（顶级任务），不需要更新父任务
    """
    # 如果是顶级任务（level 1）或没有父任务，直接返回
    if parent_id is None or child_level <= 1:
        return
    
    parent_task = db.query(Task).filter(Task.id == parent_id).first()
    if not parent_task:
        return
    
    # 获取所有直接子任务
    children = db.query(Task).filter(Task.parent_id == parent_id).all()
    
    # 如果父任务状态为未开始且有子任务变为进行中或完成，则将父任务改为进行中
    if parent_task.status == TaskStatus.NOT_STARTED:
        for child in children:
            if child.status in [TaskStatus.IN_PROGRESS, TaskStatus.DONE]:
                parent_task.status = TaskStatus.IN_PROGRESS
                break
    
    # 检查是否所有子任务都已完成，如果是，则将父任务状态改为已完成
    all_children_completed = True
    for child in children:
        if child.status != TaskStatus.DONE:
            all_children_completed = False
            break
    
    if all_children_completed and all(child.status == TaskStatus.DONE for child in children):
        # 检查所有后代是否都已完成（包括子任务的子任务等）
        if are_all_descendants_completed(db, parent_task.id):
            parent_task.status = TaskStatus.DONE
    
    # 递归更新上层父任务
    update_parent_task_status(db, parent_task.parent_id, parent_task.level)


def update_task_status_with_children(db: Session, task_id: int, status: TaskStatus) -> Optional[Task]:
    """
    更新任务状态，允许任何任务被单独标记为完成
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    # 记录旧状态
    old_status = db_task.status
    db_task.status = status
    
    # 如果是父任务完成，则完成所有子任务
    if status == TaskStatus.DONE:
        update_all_children_status(db, task_id, TaskStatus.DONE)
    
    # 更新父任务状态
    update_parent_task_status(db, db_task.parent_id, db_task.level)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def update_all_children_status(db: Session, parent_id: int, status: TaskStatus) -> None:
    """
    递归更新所有子任务的状态
    """
    # 获取直接子任务
    children = db.query(Task).filter(Task.parent_id == parent_id).all()
    
    for child in children:
        child.status = status
        
        # 递归更新子任务的子任务
        update_all_children_status(db, child.id, status)


def get_all_descendants(db: Session, parent_id: int) -> List[Task]:
    """
    递归获取任务的所有后代任务
    """
    descendants = []
    
    # 获取直接子任务
    children = db.query(Task).filter(Task.parent_id == parent_id).all()
    
    for child in children:
        descendants.append(child)
        # 递归获取子任务的后代
        descendants.extend(get_all_descendants(db, child.id))
    
    return descendants


def get_root_task(db: Session, task_id: int) -> Task:
    """
    获取任务的顶级父任务（level 1）
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task or not task.parent_id:
        return task
    
    current = task
    while current.parent_id:
        parent = db.query(Task).filter(Task.id == current.parent_id).first()
        if not parent:
            break
        current = parent
    
    return current


def is_task_in_completed_group(db: Session, task_id: int) -> bool:
    """
    检查一个任务是否属于一个已完成的任务组（即其根任务是否已完成）
    """
    root_task = get_root_task(db, task_id)
    return root_task and root_task.status == TaskStatus.DONE