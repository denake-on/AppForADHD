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
    """获取任务列表"""
    try:
        tasks = crud.get_tasks(
            db, 
            skip=skip, 
            limit=limit, 
            status=status, 
            priority=priority, 
            search=search
        )
        
        # 将SQLAlchemy模型转换为字典
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
                "isInCompletedGroup": crud.is_task_in_completed_group(db, task.id)
            }
            tasks_data.append(task_dict)
        
        print(f"✅ read_tasks: 返回 {len(tasks_data)} 个任务")
        return tasks_data
    except Exception as e:
        print(f"❌ read_tasks 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


@router.get("/hierarchical", response_model=List[dict])
def read_tasks_hierarchical(
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取层级结构的任务列表"""
    try:
        print("📝 调用 read_tasks_hierarchical")
        
        # 获取所有任务
        all_tasks = crud.get_tasks(
            db, 
            skip=0, 
            limit=1000,
            status=status,
            priority=priority,
            search=search
        )
        
        if not all_tasks:
            print("⚠️  没有任务数据")
            return []
        
        # 构建任务字典
        task_dict = {}
        for task in all_tasks:
            task_dict[task.id] = {
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
                "children": [],
                "isInCompletedGroup": crud.is_task_in_completed_group(db, task.id)
            }
        
        # 构建层级关系
        root_tasks = []
        for task_data in task_dict.values():
            parent_id = task_data["parent_id"]
            if parent_id is None or parent_id not in task_dict:
                root_tasks.append(task_data)
            else:
                task_dict[parent_id]["children"].append(task_data)
        
        # 排序
        def sort_tasks(task_list):
            task_list.sort(key=lambda x: (x["level"], x["createdAt"]))
            for task in task_list:
                sort_tasks(task["children"])
        
        sort_tasks(root_tasks)
        
        print(f"✅ read_tasks_hierarchical: 返回 {len(root_tasks)} 个顶级任务")
        return root_tasks
        
    except Exception as e:
        print(f"❌ read_tasks_hierarchical 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


@router.get("/urgent", response_model=List[dict])
def get_urgent_tasks(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取紧急任务列表"""
    try:
        tasks = db.query(Task).filter(
            Task.status != TaskStatus.DONE,
            Task.level == 1
        ).order_by(
            Task.deadline.asc(),
            Task.progress_percent.asc()
        ).limit(limit).all()
        
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "title": task.title,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "status": task.status.value,
                "progress": task.progress_percent,
                "level": task.level,
                "priority": task.priority.value
            })
        
        print(f"✅ get_urgent_tasks: 返回 {len(result)} 个紧急任务")
        return result
        
    except Exception as e:
        print(f"❌ get_urgent_tasks 错误: {str(e)}")
        return []


@router.get("/{task_id}", response_model=dict)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """获取单个任务"""
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


@router.post("/", response_model=dict)
def create_task(
    title: str = Query(..., min_length=1, max_length=255),
    description: Optional[str] = Query(None, max_length=2000),
    deadline: Optional[str] = Query(None),
    priority: TaskPriority = Query(TaskPriority.MEDIUM),
    parent_id: Optional[int] = Query(None),
    level: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """创建新任务"""
    print(f"📝 create_task: {title}")
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
    deadline: Optional[str] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    progress_percent: Optional[int] = Query(None, ge=0, le=100),
    parent_id: Optional[int] = Query(None),
    level: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    """更新任务"""
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
    """删除任务"""
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
    """更新任务状态"""
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
    """更新任务状态及其所有后代任务"""
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = status
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
    """AI拆解任务"""
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = {
        "id": task.id,
        "title": task.title,
        "description": task.description or "无描述",
        "level": task.level,
        "status": task.status.value,
        "priority": task.priority.value,
        "deadline": task.deadline.isoformat() if task.deadline else "无截止日期"
    }
    
    print("\n" + "="*80)
    print("AI拆解任务请求")
    print(f"任务ID: {task.id}, 标题: {task.title}")
    print(f"提示词: {prompt}")
    print("="*80 + "\n")
    
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
                "message": "AI拆解失败",
                "task_id": task.id,
                "breakdown_tasks": []
            }
    except Exception as e:
        print(f"❌ 拆解错误: {str(e)}")
        return {
            "success": False,
            "message": "AI拆解失败",
            "error": str(e),
            "breakdown_tasks": []
        }


@router.post("/{task_id}/breakdown/confirm", response_model=dict)
def confirm_breakdown_tasks(
    task_id: int,
    subtasks: List[dict],
    db: Session = Depends(get_db)
):
    """确认并保存AI拆解的子任务"""
    parent_task = crud.get_task(db, task_id=task_id)
    if parent_task is None:
        raise HTTPException(status_code=404, detail="Parent task not found")
    
    try:
        created_tasks = []
        
        for subtask_data in subtasks:
            deadline_date = None
            if subtask_data.get('deadline'):
                try:
                    from datetime import datetime
                    deadline_date = datetime.strptime(subtask_data['deadline'], "%Y-%m-%d").date()
                except ValueError:
                    pass
            
            priority_map = {
                'high': TaskPriority.HIGH,
                'medium': TaskPriority.MEDIUM,
                'low': TaskPriority.LOW
            }
            priority = priority_map.get(subtask_data.get('priority', 'medium'), TaskPriority.MEDIUM)
            
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
                "level": db_subtask.level
            })
        
        print(f"✅ 成功创建 {len(created_tasks)} 个子任务")
        
        return {
            "success": True,
            "message": f"成功创建 {len(created_tasks)} 个子任务",
            "parent_task_id": task_id,
            "created_tasks": created_tasks
        }
    except Exception as e:
        print(f"❌ 创建子任务错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))