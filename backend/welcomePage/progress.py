from __future__ import annotations

from typing import Dict
from datetime import date
import sqlite3
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(tags=["progress"])


# 统计每种状态的数量用于饼图的显示
@router.get("/progress")
def get_progress_summary() -> Dict[str, Dict[str, int]]:
    # 直接从 SQLite 读取，按层级分组统计
    db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
    
    result = {}
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT level, status, COUNT(*) as count
            FROM tasks
            GROUP BY level, status
            ORDER BY level, status
            """
        ).fetchall()
        
        # 首先找出所有的层级，为每个层级初始化状态计数
        levels = set()
        for row in rows:
            levels.add(row["level"])
        
        # 初始化所有存在的层级
        for level in levels:
            result[f"level_{level}"] = {"NOT_STARTED": 0, "IN_PROGRESS": 0, "DONE": 0}
        
        # 然后填充计数
        for row in rows:
            level = row["level"]
            status = row["status"].upper()  # 转换为大写以匹配预定义状态
            count = row["count"]
            
            level_key = f"level_{level}"
            # 确保状态是预定义的值之一
            if status in ["NOT_STARTED", "IN_PROGRESS", "DONE"]:
                result[level_key][status] = count
    print(result)
    return result


@router.get("/completion")
def get_today_completion() -> Dict[str, int]:
    today = date.today().isoformat()
    
    db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        
        # 统计今日截止的任务总数
        total_row = conn.execute(
            "SELECT COUNT(*) as count FROM tasks WHERE date(deadline) = date(?)",
            (today,)
        ).fetchone()
        total = total_row["count"] if total_row else 0
        
        # 统计今日截止且已完成的任务数
        done_row = conn.execute(
            "SELECT COUNT(*) as count FROM tasks WHERE date(deadline) = date(?) AND status = 'done'",
            (today,)
        ).fetchone()
        done = done_row["count"] if done_row else 0
        
        if total > 0:
            completion = int((done / total) * 100)
            # 目标完成度先固定为 80，可在前端设置或引入配置表扩展
            print(f"今日完成：{completion}")
            return {"today": completion}
        else:
            # 没有今日截止的任务，返回-1,前端处理
            print("没有今日截止的任务")
            return {"today": -1}


if __name__ == "__main__":
    get_progress_summary()
    get_today_completion()