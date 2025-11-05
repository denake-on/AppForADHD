from __future__ import annotations

from typing import Dict, Any
from datetime import date
import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["progress"])


@router.get("")
def get_progress_summary() -> Dict[str, Any]:
    """统计每种状态的数量用于饼图显示"""
    try:
        db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
        
        if not db_path.exists():
            print(f"❌ 数据库文件不存在: {db_path}")
            raise HTTPException(status_code=500, detail="Database not found")
        
        print(f"📊 查询进度统计，数据库路径: {db_path}")
        
        result = {}
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT level, status, COUNT(*) as count
                FROM tasks
                WHERE level = 1
                GROUP BY level, status
                ORDER BY level, status
                """
            ).fetchall()
            
            print(f"📋 查询到 {len(rows)} 条统计记录")
            
            # 首先找出所有的层级
            levels = set()
            for row in rows:
                levels.add(row["level"])
                print(f"  - Level {row['level']}, Status: {row['status']}, Count: {row['count']}")
            
            # 初始化所有存在的层级
            for level in levels:
                result[f"level_{level}"] = {
                    "TODO": 0,
                    "IN_PROGRESS": 0,
                    "DONE": 0,
                    "CANCELLED": 0
                }
            
            # 填充计数
            for row in rows:
                level = row["level"]
                status = row["status"]
                count = row["count"]
                
                level_key = f"level_{level}"
                if status in ["TODO", "IN_PROGRESS", "DONE", "CANCELLED"]:
                    result[level_key][status] = count
        
        print(f"✅ 进度统计结果: {result}")
        return result
        
    except sqlite3.Error as e:
        print(f"❌ 数据库查询失败: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        print(f"❌ 获取进度失败: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/completion")
def get_today_completion() -> Dict[str, int]:
    """获取今日完成度"""
    try:
        today = date.today().isoformat()
        print(f"📅 查询今日完成度: {today}")
        
        db_path = Path(__file__).resolve().parents[1] / "data" / "database.db"
        
        if not db_path.exists():
            print(f"❌ 数据库文件不存在: {db_path}")
            raise HTTPException(status_code=500, detail="Database not found")
        
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # 统计今日截止的任务总数
            total_row = conn.execute(
                "SELECT COUNT(*) as count FROM tasks WHERE date(deadline) = date(?)",
                (today,)
            ).fetchone()
            total = total_row["count"] if total_row else 0
            
            # 统计今日截止且已完成的任务数（注意：状态是 DONE，不是 done）
            done_row = conn.execute(
                "SELECT COUNT(*) as count FROM tasks WHERE date(deadline) = date(?) AND status = 'DONE'",
                (today,)
            ).fetchone()
            done = done_row["count"] if done_row else 0
            
            print(f"📊 今日任务: 总数={total}, 完成={done}")
            
            if total > 0:
                completion = int((done / total) * 100)
                print(f"✅ 今日完成度: {completion}%")
                return {"today": completion}
            else:
                print("⚠️  没有今日截止的任务")
                return {"today": -1}
                
    except sqlite3.Error as e:
        print(f"❌ 数据库查询失败: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        print(f"❌ 获取今日完成度失败: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print(get_progress_summary())
    print(get_today_completion())