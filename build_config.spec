# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# 项目根目录
PROJECT_ROOT = Path('E:\\AppForADHD')

a = Analysis(
    ['main.py'],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[
        # 前端构建文件（整个 dist 目录）
        (str(PROJECT_ROOT / 'frontend' / 'dist'), 'frontend/dist'),
        
        # 后端数据文件
        (str(PROJECT_ROOT / 'backend' / 'data'), 'backend/data'),
        
        # 配置文件
        (str(PROJECT_ROOT / 'config.json'), '.'),
    ],
    hiddenimports=[
        # FastAPI 核心
        'fastapi',
        'fastapi.routing',
        'fastapi.responses',
        'fastapi.exceptions',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'fastapi.staticfiles',
        'fastapi.templating',
        
        # Uvicorn 服务器
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        
        # Starlette (FastAPI 基础)
        'starlette',
        'starlette.applications',
        'starlette.routing',
        'starlette.middleware',
        'starlette.middleware.base',
        'starlette.middleware.cors',
        'starlette.responses',
        'starlette.staticfiles',
        'starlette.exceptions',
        
        # Pydantic (数据验证)
        'pydantic',
        'pydantic.fields',
        'pydantic.types',
        'pydantic.networks',
        'pydantic.error_wrappers',
        'pydantic.validators',
        
        # 标准库
        'sqlite3',
        'json',
        'pathlib',
        'datetime',
        'typing',
        'traceback',
        'webbrowser',
        'threading',
        'time',
        'os',
        'sys',
        'random',
        
        # HTTP 客户端
        'requests',
        'urllib3',
        'httpx',
        
        # 你的后端模块
        'backend',
        'backend.task',
        'backend.task.routes',
        'backend.task.models',
        'backend.task.BreakDownTask',
        'backend.welcomePage',
        'backend.welcomePage.greeting',
        'backend.welcomePage.my_calendar',
        'backend.welcomePage.progress',
        'backend.welcomePage.tasks',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的大型库
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'tkinter',
        'PyQt5',
        'PySide2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AppForADHD',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 开发调试时设为 True，发布时改为 False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标: 'icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AppForADHD'
)