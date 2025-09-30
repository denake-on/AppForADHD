from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# 修复打包环境下的导入问题
try:
    # 开发环境下（相对导入）
    from ..database import get_db
    from ..models import Task, TaskStatus, TaskPriority
except ImportError:
    # 打包环境下（绝对导入）
    from backend.database import get_db
    from backend.models import Task, TaskStatus, TaskPriority

from . import crud
from .BreakDownTask import breakdown_service


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


@router.post("/{task_id}/breakdown", response_model=dict)
def breakdown_task(
    task_id: int,
    prompt: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    AI拆解任务 - 使用OpenRouter API进行智能任务拆解
    """
    # 获取任务信息
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 构建任务信息字典
    task_info = {
        "id": task.id,
        "title": task.title,
        "description": task.description or "无描述",
        "level": task.level,
        "status": task.status.value,
        "priority": task.priority.value,
        "deadline": task.deadline.isoformat() if task.deadline else "无截止日期"
    }
    
    # 打印原始请求信息
    print("\n" + "="*80)
    print("AI拆解任务请求")
    print("="*80)
    print(f"任务ID: {task.id}")
    print(f"任务标题: {task.title}")
    print(f"任务描述: {task.description}")
    print(f"任务层级: Level {task.level}")
    print(f"任务状态: {task.status.value}")
    print(f"任务优先级: {task.priority.value}")
    print(f"截止日期: {task.deadline.isoformat() if task.deadline else '无'}")
    print("-"*80)
    print(f"拆解提示词:\n{prompt}")
    print("="*80 + "\n")
    
    # 调用AI拆解服务
    try:
        breakdown_tasks = breakdown_service.breakdown_task(task_info, prompt)
        
        if breakdown_tasks and len(breakdown_tasks) > 0:
            return {
                "success": True,
                "message": "AI拆解成功",
                "task_id": task.id,
                "task_title": task.title,
                "prompt": prompt,
                "breakdown_tasks": breakdown_tasks,
                "subtask_count": len(breakdown_tasks)
            }
        else:
            return {
                "success": False,
                "message": "AI拆解失败，请稍后重试",
                "task_id": task.id,
                "task_title": task.title,
                "prompt": prompt,
                "breakdown_tasks": [],
                "subtask_count": 0
            }
        
    except Exception as e:
        print(f"❌ 拆解过程中发生错误: {str(e)}")
        return {
            "success": False,
            "message": "AI拆解失败，请稍后重试",
            "task_id": task.id,
            "task_title": task.title,
            "prompt": prompt,
            "error": str(e),
            "breakdown_tasks": [],
            "subtask_count": 0
        }


@router.post("/{task_id}/breakdown/confirm", response_model=dict)
def confirm_breakdown_tasks(
    task_id: int,
    subtasks: List[dict],
    db: Session = Depends(get_db)
):
    """
    确认并保存AI拆解的子任务
    """
    # 获取父任务信息
    parent_task = crud.get_task(db, task_id=task_id)
    if parent_task is None:
        raise HTTPException(status_code=404, detail="Parent task not found")
    
    try:
        created_tasks = []
        
        for subtask_data in subtasks:
            # 解析截止日期
            deadline_date = None
            if subtask_data.get('deadline'):
                try:
                    from datetime import datetime
                    deadline_date = datetime.strptime(subtask_data['deadline'], "%Y-%m-%d").date()
                except ValueError:
                    print(f"⚠️ 无效的截止日期格式: {subtask_data['deadline']}")
            
            # 映射优先级
            priority_map = {
                'high': TaskPriority.HIGH,
                'medium': TaskPriority.MEDIUM,
                'low': TaskPriority.LOW
            }
            priority = priority_map.get(subtask_data.get('priority', 'medium'), TaskPriority.MEDIUM)
            
            # 创建子任务
            db_subtask = crud.create_task(
                db,
                title=subtask_data['title'],
                description=subtask_data.get('description', ''),
                deadline=deadline_date,
                priority=priority,
                parent_id=task_id,
                level=parent_task.level + 1
            )
            
            created_tasks.append({
                "id": db_subtask.id,
                "title": db_subtask.title,
                "description": db_subtask.description,
                "deadline": db_subtask.deadline.isoformat() if db_subtask.deadline else None,
                "priority": db_subtask.priority.value,
                "level": db_subtask.level,
                "parent_id": db_subtask.parent_id
            })
        
        print(f"✅ 成功创建 {len(created_tasks)} 个子任务")
        
        return {
            "success": True,
            "message": f"成功创建 {len(created_tasks)} 个子任务",
            "parent_task_id": task_id,
            "created_tasks": created_tasks
        }
        
    except Exception as e:
        print(f"❌ 创建子任务时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建子任务失败: {str(e)}")
