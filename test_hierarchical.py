"""
测试后端层级任务API返回的数据
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from backend.task.crud import get_tasks
from backend.database import SessionLocal
from backend.task.routes import read_tasks_hierarchical

def test_hierarchical_api():
    """测试层级任务API"""
    # 获取数据库会话
    db = SessionLocal()
    try:
        # 直接调用层级任务函数（内部实现）
        # 我们需要手动模拟依赖注入
        from backend.task import crud
        from typing import List
        
        # 获取所有任务
        all_tasks = crud.get_tasks(db, skip=0, limit=1000)
        
        print(f"总共获取到 {len(all_tasks)} 个任务")
        
        # 构建层级结构（使用与API端点相同的逻辑）
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
            task_list.sort(key=lambda x: (x["level"], x["createdAt"]))
            for task in task_list:
                sort_tasks(task["children"])  # 递归排序子任务

        sort_tasks(root_tasks)
        
        # print("层级任务结构:")
        # for i, task in enumerate(root_tasks):
        #     print(f"  {i+1}. 根任务: {task['title']} (ID: {task['id']}, Level: {task['level']})")
        #     if task['children']:
        #         for j, child in enumerate(task['children']):
        #             print(f"     {j+1}.1 子任务: {child['title']} (ID: {child['id']}, Level: {child['level']})")
        #             if child['children']:
        #                 for k, subchild in enumerate(child['children']):
        #                     print(f"       {k+1}.1.1 孙任务: {subchild['title']} (ID: {subchild['id']}, Level: {subchild['level']})")
        
        return root_tasks
        
    finally:
        db.close()

if __name__ == "__main__":
    result = test_hierarchical_api()
    print(result)