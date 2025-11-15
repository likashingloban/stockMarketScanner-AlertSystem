#!/usr/bin/env python3
"""
部署脚本：将前端代码挂载到后端指定目录
用于开发和部署环境
"""

import os
import shutil
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.absolute()

# 前端源码目录
FRONTEND_SRC = ROOT_DIR / "frontend_src"
FRONTEND_TEMPLATES = FRONTEND_SRC / "templates"
FRONTEND_STATIC = FRONTEND_SRC / "static"

# 后端目标目录
BACKEND_DIR = ROOT_DIR / "backend"
BACKEND_TEMPLATES = BACKEND_DIR / "templates"
BACKEND_STATIC = BACKEND_DIR / "static"


def clean_backend_dirs():
    """清空后端的templates和static目录"""
    print("🧹 清理后端目录...")

    if BACKEND_TEMPLATES.exists():
        shutil.rmtree(BACKEND_TEMPLATES)
    if BACKEND_STATIC.exists():
        shutil.rmtree(BACKEND_STATIC)

    BACKEND_TEMPLATES.mkdir(parents=True, exist_ok=True)
    BACKEND_STATIC.mkdir(parents=True, exist_ok=True)

    print("✅ 后端目录已清理")


def copy_templates():
    """复制模板文件到后端"""
    print("📄 复制模板文件...")

    if not FRONTEND_TEMPLATES.exists():
        print("⚠️  警告: frontend_src/templates 目录不存在")
        return

    # 复制所有HTML模板
    for template_file in FRONTEND_TEMPLATES.glob("**/*.html"):
        relative_path = template_file.relative_to(FRONTEND_TEMPLATES)
        target_file = BACKEND_TEMPLATES / relative_path

        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template_file, target_file)
        print(f"  ✓ {relative_path}")

    print("✅ 模板文件复制完成")


def copy_static():
    """复制静态资源到后端"""
    print("📦 复制静态资源...")

    if not FRONTEND_STATIC.exists():
        print("⚠️  警告: frontend_src/static 目录不存在")
        return

    # 复制所有静态文件
    for static_file in FRONTEND_STATIC.glob("**/*"):
        if static_file.is_file():
            relative_path = static_file.relative_to(FRONTEND_STATIC)
            target_file = BACKEND_STATIC / relative_path

            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(static_file, target_file)
            print(f"  ✓ {relative_path}")

    print("✅ 静态资源复制完成")


def deploy(clean=True):
    """
    执行部署

    Args:
        clean: 是否先清理目标目录
    """
    print("=" * 60)
    print("🚀 开始部署前端到后端")
    print("=" * 60)

    if clean:
        clean_backend_dirs()

    copy_templates()
    copy_static()

    print("=" * 60)
    print("✅ 部署完成!")
    print("=" * 60)
    print(f"📁 模板目录: {BACKEND_TEMPLATES}")
    print(f"📁 静态资源目录: {BACKEND_STATIC}")
    print("")
    print("💡 提示:")
    print("  - 现在可以运行 Flask 应用: cd backend && python app.py")
    print("  - 前端源码保存在: frontend_src/")
    print("  - 修改前端后重新运行此脚本即可更新")
    print("")


def watch_mode():
    """监听模式：自动检测文件变化并重新部署"""
    try:
        import time
        import hashlib

        print("👀 监听模式已启动 (Ctrl+C 退出)")
        print("   监听目录:", FRONTEND_SRC)
        print("")

        last_hash = None

        while True:
            # 计算前端目录的哈希值
            current_hash = hashlib.md5()

            for file_path in sorted(FRONTEND_SRC.glob("**/*")):
                if file_path.is_file():
                    current_hash.update(file_path.read_bytes())

            current_hash = current_hash.hexdigest()

            # 检测到变化
            if last_hash and current_hash != last_hash:
                print("\n🔄 检测到文件变化，重新部署...")
                deploy(clean=True)

            last_hash = current_hash
            time.sleep(2)  # 每2秒检查一次

    except KeyboardInterrupt:
        print("\n👋 监听模式已停止")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        # 先部署一次
        deploy(clean=True)
        # 进入监听模式
        watch_mode()
    else:
        # 单次部署
        deploy(clean=True)
