from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any
import sqlite3
from pathlib import Path

from fastapi import APIRouter, Query

router = APIRouter(tags=["tasks"])


# 获取紧急任务列表
@router.get("/tasks/urgent")
def get_urgent_tasks(limit: int = Query(10, ge=1, le=100)) -> List[Dict[str, Any]]:
    # 直接从 SQLite 读取
    db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
    
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
                "progress": row["progress_percent"],
                "level": row["level"]
            })
        return result

if __name__ == "__main__":
    result = get_urgent_tasks(limit=10)
    print(result)
