#!/usr/bin/env python3
"""
WeiWan应用的启动脚本
用于在打包后的exe环境中启动应用
"""

import sys
import os
from pathlib import Path
import uvicorn

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 设置环境变量
os.environ.setdefault('PYTHONPATH', str(current_dir))

def main():
    """启动应用"""
    try:
        print("正在启动WeiWan应用...")
        
        # 导入应用
        from main import app
        
        # 启动服务器
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        print(f"启动应用时出错: {e}")
        print("请检查以下内容:")
        print("1. 所有依赖是否正确安装")
        print("2. 数据库文件是否存在")
        print("3. 前端文件是否正确构建")
        
        # 等待用户输入，防止窗口立即关闭
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
