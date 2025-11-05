from __future__ import annotations

from datetime import date
from typing import Dict, List, Any
import sqlite3
from pathlib import Path

from fastapi import APIRouter, Query, HTTPException

router = APIRouter(tags=["calendar"])


@router.get("")
def get_calendar(
    year: int = Query(None, description="年份"),
    month: int = Query(None, description="月份 (1-12)")
) -> Dict[str, List[Dict[str, Any]]]:
    """获取指定月份的日历任务"""
    try:
        print(f"📅 收到日历请求: year={year}, month={month}")
        
        # 如果没有指定年月，使用当前月份
        if year is None or month is None:
            today = date.today()
            target_date = today.replace(day=1)
            print(f"📅 使用当前月份: {target_date.year}-{target_date.month}")
        else:
            target_date = date(year, month, 1)
            print(f"📅 查询指定月份: {year}-{month}")
        
        month_start = target_date
        
        # 获取下个月的第一天
        if month_start.month == 12:
            next_month_start = month_start.replace(year=month_start.year + 1, month=1)
        else:
            next_month_start = month_start.replace(month=month_start.month + 1)

        # 直接从 SQLite 读取
        db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
        
        if not db_path.exists():
            print(f"❌ 数据库文件不存在: {db_path}")
            raise HTTPException(status_code=500, detail="Database not found")
        
        print(f"📂 数据库路径: {db_path}")
        
        start_s = month_start.isoformat()
        next_s = next_month_start.isoformat()
        
        print(f"📊 查询范围: {start_s} 到 {next_s}")

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

            print(f"📊 查询到 {len(rows)} 条任务记录")

            for r in rows:
                deadline = r["deadline"]
                if not deadline:
                    continue
                    
                key = str(deadline)
                task_data = {
                    "id": r["id"],
                    "title": r["title"],
                    "status": r["status"],
                    "progress": r["progress_percent"] if r["progress_percent"] is not None else 0,
                    "deadline": key,
                    "level": r["level"],
                }
                
                grouped.setdefault(key, []).append(task_data)
                print(f"  📌 {key}: {task_data['title']}")
        
        print(f"✅ 返回 {len(grouped)} 天的任务数据")
        print(f"📋 日期列表: {list(grouped.keys())}")
        return grouped
        
    except sqlite3.Error as e:
        print(f"❌ 数据库查询失败: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        print(f"❌ 获取日历失败: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    result = get_calendar()
    print(f"结果: {result}")