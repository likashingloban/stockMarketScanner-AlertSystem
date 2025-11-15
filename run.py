#!/usr/bin/env python3
"""
快速启动脚本：部署前端并启动Flask应用
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()

def main():
    print("=" * 60)
    print("🚀 Stock Watch & Alert System - 快速启动")
    print("=" * 60)
    print("")

    # 1. 部署前端
    print("📦 步骤 1/2: 部署前端到后端...")
    try:
        subprocess.run([sys.executable, str(ROOT_DIR / "deploy.py")], check=True)
    except subprocess.CalledProcessError:
        print("❌ 部署失败!")
        return 1

    print("")
    print("=" * 60)

    # 2. 启动Flask应用
    print("🚀 步骤 2/2: 启动Flask应用...")
    print("=" * 60)
    print("")

    try:
        subprocess.run(
            [sys.executable, str(ROOT_DIR / "backend" / "app.py")],
            cwd=str(ROOT_DIR / "backend")
        )
    except KeyboardInterrupt:
        print("\n\n👋 应用已停止")
        return 0

if __name__ == "__main__":
    sys.exit(main())
