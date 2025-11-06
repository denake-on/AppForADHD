# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

# 项目根目录
ROOT_DIR = Path.cwd()

# 收集数据文件
datas = [
    (str(ROOT_DIR / 'frontend' / 'dist'), 'frontend/dist'),
    (str(ROOT_DIR / 'backend' / 'data' / 'greetings.json'), 'backend/data'),  # 添加 greetings.json
    (str(ROOT_DIR / 'config.json'), '.'),
]

# 如果需要打包初始数据库（可选）
# datas.append((str(ROOT_DIR / 'backend' / 'data' / 'database.db'), 'backend/data'))

# 隐藏导入
hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi',
    'sqlalchemy',
    'sqlalchemy.ext.declarative',
    'sqlite3',
    'pydantic',
    'starlette',
    'backend.database',
    'backend.models',
    'backend.task.routes',
    'backend.task.BreakDownTask',
    'backend.welcomePage.greeting',
    'backend.welcomePage.my_calendar',
    'backend.welcomePage.progress',
    'backend.welcomePage.tasks',
]

a = Analysis(
    ['main.py'],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AppForADHD',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)