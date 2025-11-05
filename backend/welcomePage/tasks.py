from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any
import sqlite3
from pathlib import Path

from fastapi import APIRouter, Query

router = APIRouter(tags=["tasks"])


# 获取欢迎页任务列表（新增）
@router.get("/")
def get_welcome_tasks() -> List[Dict[str, Any]]:
    """获取所有任务的层级结构"""
    db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, title, description, deadline, status, 
                       progress_percent, level, parent_id, priority
                FROM tasks
                ORDER BY 
                    CASE WHEN parent_id IS NULL THEN 0 ELSE 1 END,
                    level ASC,
                    id ASC
                """
            ).fetchall()
            
            if not rows:
                print("⚠️  数据库中没有任务")
                return []
            
            # 转换为字典列表
            result = []
            for row in rows:
                task_dict = {
                    "id": row["id"],
                    "title": row["title"],
                    "description": row["description"] if row["description"] else "",
                    "deadline": row["deadline"],
                    "status": row["status"],
                    "progress": row["progress_percent"] if row["progress_percent"] else 0,
                    "level": row["level"],
                    "parent_id": row["parent_id"],
                    "priority": row["priority"] if row["priority"] else "medium"
                }
                result.append(task_dict)
            
            print(f"✅ 成功返回 {len(result)} 个任务")
            return result
            
    except sqlite3.Error as e:
        print(f"❌ 数据库错误: {str(e)}")
        return []
    except Exception as e:
        print(f"❌ 获取任务失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


# 获取紧急任务列表
@router.get("/tasks/urgent")
def get_urgent_tasks(limit: int = Query(10, ge=1, le=100)) -> List[Dict[str, Any]]:
    """获取紧急任务列表（按截止日期排序）"""
    db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, title, deadline, status, progress_percent, level
                FROM tasks
                WHERE status != 'DONE'
                    AND level = 1
                ORDER BY 
                    CASE WHEN deadline IS NULL THEN 1 ELSE 0 END,
                    deadline ASC,
                    progress_percent ASC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()
            
            result = []
            for row in rows:
                result.append({
                    "id": row["id"],
                    "title": row["title"],
                    "deadline": row["deadline"],
                    "status": row["status"],
                    "progress": row["progress_percent"] if row["progress_percent"] else 0,
                    "level": row["level"]
                })
            
            print(f"✅ 返回 {len(result)} 个紧急任务")
            return result
            
    except Exception as e:
        print(f"❌ 获取紧急任务失败: {str(e)}")
        return []


# 获取层级任务（新增）
@router.get("/tasks/hierarchical")
def get_hierarchical_tasks() -> List[Dict[str, Any]]:
    """获取层级结构的任务"""
    db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, title, description, deadline, status, 
                       progress_percent, level, parent_id, priority
                FROM tasks
                ORDER BY level ASC, id ASC
                """
            ).fetchall()
            
            if not rows:
                return []
            
            # 构建任务字典
            task_dict = {}
            for row in rows:
                task_dict[row["id"]] = {
                    "id": row["id"],
                    "title": row["title"],
                    "description": row["description"] or "",
                    "deadline": row["deadline"],
                    "status": row["status"],
                    "progress": row["progress_percent"] or 0,
                    "level": row["level"],
                    "parent_id": row["parent_id"],
                    "priority": row["priority"] or "medium",
                    "children": []
                }
            
            # 构建层级结构
            result = []
            for task_id, task_data in task_dict.items():
                parent_id = task_data["parent_id"]
                if parent_id and parent_id in task_dict:
                    task_dict[parent_id]["children"].append(task_data)
                else:
                    result.append(task_data)
            
            print(f"✅ 返回 {len(result)} 个顶级任务")
            return result
            
    except Exception as e:
        print(f"❌ 获取层级任务失败: {str(e)}")
        return []


if __name__ == "__main__":
    print("测试获取任务列表:")
    tasks = get_welcome_tasks()
    print(f"共 {len(tasks)} 个任务")
    
    print("\n测试获取紧急任务:")
    urgent = get_urgent_tasks(limit=10)
    print(f"共 {len(urgent)} 个紧急任务")
    
    print("\n测试获取层级任务:")
    hierarchical = get_hierarchical_tasks()
    print(f"共 {len(hierarchical)} 个顶级任务")