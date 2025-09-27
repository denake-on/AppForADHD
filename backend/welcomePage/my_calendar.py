from __future__ import annotations

from datetime import date
from typing import Dict, List, Any
import sqlite3
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(tags=["calendar"]) # 创建API路由组


@router.get("/calendar")
def get_calendar() -> Dict[str, List[Dict[str, Any]]]:
    # Return tasks grouped by deadline day for current month
    today = date.today()
    month_start = today.replace(day=1) # 获取当前月份的第一天
    ##########################
    # 获取下个月的第一天
    ##########################
    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1)
        # 当前月份是12月，下一个月是1月
    else:
        next_month_start = month_start.replace(month=month_start.month + 1)

    # 直接从 SQLite 读取
    db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
    start_s = month_start.isoformat()
    next_s = next_month_start.isoformat()

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, title, status, progress_percent, deadline, level
            FROM tasks
            WHERE deadline IS NOT NULL
              AND date(deadline) >= date(?)
              AND date(deadline) < date(?)
            ORDER BY date(deadline) ASC
            """,
            (start_s, next_s),
        ).fetchall()

        for r in rows:
            deadline = r["deadline"]
            if not deadline:
                continue
            key = str(deadline)
            grouped.setdefault(key, []).append({
                "id": r["id"],
                "title": r["title"],
                "status": r["status"],
                "progress": r["progress_percent"],
                "deadline": key,
                "level": r["level"],
            })
    print(grouped)
    return grouped

if __name__ == "__main__":
    get_calendar()

