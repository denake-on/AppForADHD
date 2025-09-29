from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
GREETINGS_FILE = DATA_DIR / "greetings.json"

router = APIRouter(tags=["greeting"])


@router.get("/greeting")
def get_random_greeting() -> Dict[str, Any]:
    if not GREETINGS_FILE.exists():
        raise HTTPException(status_code=500, detail="greetings.json not found")
        # 如果文件不存在 报错500
    greetings = json.loads(GREETINGS_FILE.read_text(encoding="utf-8"))
    if not isinstance(greetings, list) or not greetings:
        raise HTTPException(status_code=500, detail="Invalid greetings data")
        # 如果数据不是列表或者为空，返回500
    text = random.choice(greetings)
    print(text)
    return {"greeting": f"{text}"}


if __name__ == "__main__":
    get_random_greeting()


