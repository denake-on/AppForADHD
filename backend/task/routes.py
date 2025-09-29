from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from ..database import get_db
from ..models import Task, TaskStatus, TaskPriority
from . import crud


# 定义层级任务的数据模型
class HierarchicalTask(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    dueDate: Optional[str]
    createdAt: str
    updatedAt: str
    progressPercent: int
    level: int
    parent_id: Optional[int]
    children: List['HierarchicalTask']  # 递归定义
    
# 解决递归模型问题
HierarchicalTask.model_rebuild()

# 为类型注解导入
from typing import List as ListType

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=List[dict])
def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    获取任务列表
    """
    tasks = crud.get_tasks(
        db, 
        skip=skip, 
        limit=limit, 
        status=status, 
        priority=priority, 
        search=search
    )
    
    # 将SQLAlchemy模型转换为字典，以便FastAPI正确序列化
    tasks_data = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "priority": task.priority.value,
            "dueDate": task.deadline.isoformat() if task.deadline else None,
            "createdAt": task.created_at.isoformat(),
            "updatedAt": task.updated_at.isoformat(),
            "progressPercent": task.progress_percent,
            "level": task.level,
            "parent_id": task.parent_id,
            # 添加一个字段表示该任务是否属于已完成的组（即其level 1父任务是否已完成）
            "isInCompletedGroup": crud.is_task_in_completed_group(db, task.id)
        }
        tasks_data.append(task_dict)
    print("调用routes.py的read_tasks成功") #调试
    return tasks_data


@router.get("/hierarchical", response_model=List[HierarchicalTask])
def read_tasks_hierarchical(
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    print("调用routes.py的read_tasks_hierarchical成功") #调试
    """
    获取层级结构的任务列表（以level 1的任务为根节点）
    """
    # 获取所有任务，应用过滤器
    all_tasks = crud.get_tasks(
        db, 
        skip=0, 
        limit=1000,  # 设置足够大的limit获取所有任务
        status=status,
        priority=priority,
        search=search
    )
    
    # 构建层级结构
    task_dict = {}
    root_tasks = []
    
    # 创建任务字典，便于查找
    for task in all_tasks:
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "priority": task.priority.value,
            "dueDate": task.deadline.isoformat() if task.deadline else None,
            "createdAt": task.created_at.isoformat(),
            "updatedAt": task.updated_at.isoformat(),
            "progressPercent": task.progress_percent,
            "level": task.level,
            "parent_id": task.parent_id,
            "children": [],  # 子任务列表
            # 添加一个字段表示该任务是否属于已完成的组（即其level 1父任务是否已完成）
            "isInCompletedGroup": crud.is_task_in_completed_group(db, task.id)
        }
        task_dict[task.id] = task_data
    
    # 构建层级关系
    for task_data in task_dict.values():
        parent_id = task_data["parent_id"]
        if parent_id is None or parent_id not in task_dict:
            # 没有父任务，是根任务（level 1）
            root_tasks.append(task_data)
        else:
            # 有父任务，将其添加到父任务的children中
            parent_task = task_dict[parent_id]
            parent_task["children"].append(task_data)
    
    # 按层级和创建时间排序
    def sort_tasks(task_list):
        # 按层级和创建时间排序
        task_list.sort(key=lambda x: (x["level"], x["createdAt"] if x["createdAt"] else ""))
        for task in task_list:
            sort_tasks(task["children"])  # 递排序子任务
    
    sort_tasks(root_tasks)
    return root_tasks


@router.get("/{task_id}", response_model=dict)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    获取单个任务
    """
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "dueDate": task.deadline.isoformat() if task.deadline else None,
        "createdAt": task.created_at.isoformat(),
        "updatedAt": task.updated_at.isoformat(),
        "progressPercent": task.progress_percent,
        "level": task.level,
        "parent_id": task.parent_id
    }
    # 获取所有任务，应用过滤器
    all_tasks = crud.get_tasks(
        db, 
        skip=0, 
        limit=1000,  # 设置足够大的limit获取所有任务
        status=status,
        priority=priority,
        search=search
    )
    
    # 构建层级结构
    task_dict = {}
    root_tasks = []
    
    # 创建任务字典，便于查找
    for task in all_tasks:
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "priority": task.priority.value,
            "dueDate": task.deadline.isoformat() if task.deadline else None,
            "createdAt": task.created_at.isoformat(),
            "updatedAt": task.updated_at.isoformat(),
            "progressPercent": task.progress_percent,
            "level": task.level,
            "parent_id": task.parent_id,
            "children": []  # 子任务列表
        }
        task_dict[task.id] = task_data
    
    # 构建层级关系
    for task_data in task_dict.values():
        parent_id = task_data["parent_id"]
        if parent_id is None or parent_id not in task_dict:
            # 没有父任务，是根任务（level 1）
            root_tasks.append(task_data)
        else:
            # 有父任务，将其添加到父任务的children中
            parent_task = task_dict[parent_id]
            parent_task["children"].append(task_data)
    
    # 按层级和创建时间排序
    def sort_tasks(task_list):
        # 按层级和创建时间排序
        task_list.sort(key=lambda x: (x["level"], x["createdAt"] if x["createdAt"] else ""))
        for task in task_list:
            sort_tasks(task["children"])  # 递排序子任务
    
    sort_tasks(root_tasks)
    return root_tasks


@router.post("/", response_model=dict)
def create_task(
    title: str = Query(..., min_length=1, max_length=255),
    description: Optional[str] = Query(None, max_length=2000),
    deadline: Optional[str] = Query(None),  # 日期格式为YYYY-MM-DD
    priority: TaskPriority = Query(TaskPriority.MEDIUM),
    parent_id: Optional[int] = Query(None),
    level: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    print("调用routes.py的create_task成功") #调试
    """
    创建新任务
    """
    from datetime import datetime
    
    deadline_date = None
    if deadline:
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD."
            )
    
    db_task = crud.create_task(
        db,
        title=title,
        description=description,
        deadline=deadline_date,
        priority=priority,
        parent_id=parent_id,
        level=level
    )
    
    return {
        "id": db_task.id,
        "title": db_task.title,
        "description": db_task.description,
        "status": db_task.status.value,
        "priority": db_task.priority.value,
        "dueDate": db_task.deadline.isoformat() if db_task.deadline else None,
        "createdAt": db_task.created_at.isoformat(),
        "updatedAt": db_task.updated_at.isoformat(),
        "progressPercent": db_task.progress_percent,
        "level": db_task.level,
        "parent_id": db_task.parent_id
    }


@router.put("/{task_id}", response_model=dict)
def update_task(
    task_id: int,
    title: Optional[str] = Query(None, min_length=1, max_length=255),
    description: Optional[str] = Query(None, max_length=2000),
    deadline: Optional[str] = Query(None),  # 日期格式为YYYY-MM-DD
    priority: Optional[TaskPriority] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    progress_percent: Optional[int] = Query(None, ge=0, le=100),
    parent_id: Optional[int] = Query(None),
    level: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    print("调用routes.py的update_task成功") #调试
    """
    更新任务
    """
    from datetime import datetime
    
    deadline_date = None
    if deadline:
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD."
            )
    
    task = crud.update_task(
        db,
        task_id=task_id,
        title=title,
        description=description,
        deadline=deadline_date,
        priority=priority,
        status=status,
        progress_percent=progress_percent,
        parent_id=parent_id,
        level=level
    )
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "dueDate": task.deadline.isoformat() if task.deadline else None,
        "createdAt": task.created_at.isoformat(),
        "updatedAt": task.updated_at.isoformat(),
        "progressPercent": task.progress_percent,
        "level": task.level,
        "parent_id": task.parent_id
    }


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    print("调用routes.py的delete_task成功") #调试
    """
    删除任务
    """
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/status", response_model=dict)
def update_task_status(
    task_id: int,
    status: TaskStatus,
    db: Session = Depends(get_db)
):
    print("调用routes.py的update_task_status成功") #调试
    """
    更新任务状态，如果父任务完成则自动完成所有子任务
    """
    task = crud.update_task_status_with_children(db, task_id=task_id, status=status)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "dueDate": task.deadline.isoformat() if task.deadline else None,
        "createdAt": task.created_at.isoformat(),
        "updatedAt": task.updated_at.isoformat(),
        "progressPercent": task.progress_percent,
        "level": task.level,
        "parent_id": task.parent_id
    }


@router.patch("/{task_id}/status-with-descendants", response_model=dict)
def update_task_status_with_descendants(
    task_id: int,
    status: TaskStatus,
    db: Session = Depends(get_db)
):
    print("调用routes.py的update_task_status_with_descendants成功") #调试
    """
    更新任务状态及其所有后代任务的状态（递归更新）
    """
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 更新当前任务状态
    task.status = status
    
    # 获取所有后代任务并更新它们的状态
    descendants = crud.get_all_descendants(db, task_id)
    for descendant in descendants:
        descendant.status = status
    
    db.commit()
    db.refresh(task)
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "dueDate": task.deadline.isoformat() if task.deadline else None,
        "createdAt": task.created_at.isoformat(),
        "updatedAt": task.updated_at.isoformat(),
        "progressPercent": task.progress_percent,
        "level": task.level,
        "parent_id": task.parent_id
    }
