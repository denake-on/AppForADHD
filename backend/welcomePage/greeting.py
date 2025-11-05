from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
GREETINGS_FILE = DATA_DIR / "greetings.json"

router = APIRouter(tags=["greeting"])

@router.get("")
def get_random_greeting() -> Dict[str, Any]:
    """获取随机问候语"""
    print(f"📝 问候语请求")
    print(f"📂 数据目录: {DATA_DIR}")
    print(f"📄 问候语文件: {GREETINGS_FILE}")
    print(f"✓ 文件存在: {GREETINGS_FILE.exists()}")
    
    if not GREETINGS_FILE.exists():
        print(f"❌ 问候语文件不存在: {GREETINGS_FILE}")
        raise HTTPException(status_code=500, detail="greetings.json not found")
    
    try:
        content = GREETINGS_FILE.read_text(encoding="utf-8")
        print(f"📄 文件内容: {content[:100]}")
        
        greetings = json.loads(content)
        print(f"📋 问候语列表长度: {len(greetings) if isinstance(greetings, list) else 'not a list'}")
        
        if not isinstance(greetings, list) or not greetings:
            print("❌ 问候语数据格式错误或为空")
            raise HTTPException(status_code=500, detail="Invalid greetings data")
        
        text = random.choice(greetings)
        print(f"✅ 选中的问候语: {text}")
        
        return {"greeting": text}
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse greetings.json: {str(e)}")
    except Exception as e:
        print(f"❌ 获取问候语失败: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    



if __name__ == "__main__":
    print(get_random_greeting())