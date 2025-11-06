from __future__ import annotations

import sys
import os
import json
import random
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["greeting"])


def get_data_dir():
    """获取数据目录"""
    if getattr(sys, 'frozen', False):
        # 打包后，greetings.json 应该在 _MEIPASS 中
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'backend' / 'data'
        else:
            # 或者在 exe 同目录
            return Path(sys.executable).parent / 'backend' / 'data'
    else:
        # 开发环境
        return Path(__file__).resolve().parents[1] / "data"


@router.get("")
def get_random_greeting() -> Dict[str, Any]:
    """获取随机问候语"""
    data_dir = get_data_dir()
    greetings_file = data_dir / "greetings.json"
    
    print(f"📝 问候语请求")
    print(f"📂 数据目录: {data_dir}")
    print(f"📄 问候语文件: {greetings_file}")
    print(f"✓ 文件存在: {greetings_file.exists()}")
    print(f"🔧 打包模式: {getattr(sys, 'frozen', False)}")
    
    if not greetings_file.exists():
        print(f"❌ 问候语文件不存在: {greetings_file}")
        # 如果找不到文件，尝试列出目录内容
        if data_dir.exists():
            print(f"📂 数据目录内容:")
            for item in data_dir.iterdir():
                print(f"  - {item.name}")
        raise HTTPException(status_code=500, detail="greetings.json not found")
    
    try:
        content = greetings_file.read_text(encoding="utf-8")
        print(f"📄 文件内容长度: {len(content)}")
        
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