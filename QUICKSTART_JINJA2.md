# 🚀 Jinja2 版本快速开始

## 一键启动

```bash
# 克隆或进入项目目录
cd stockMarketScanner&AlertSystem

# 切换到 Jinja2 分支
git checkout feature/jinja2-refactor

# 启动应用（自动部署前端并启动Flask）
python run.py
```

访问：http://localhost:5001

---

## 目录说明

```
项目结构：
  frontend_src/    ← 🎨 前端开发目录（在这里编辑HTML/CSS/JS）
  backend/         ← 🔧 后端代码
  deploy.py        ← 📦 部署脚本
  run.py           ← ⚡ 快速启动脚本
```

---

## 开发流程

### 修改前端

1. 编辑 `frontend_src/templates/*.html` 或 `frontend_src/static/*`
2. 重新部署：
   ```bash
   python deploy.py
   ```
3. 刷新浏览器

**或者使用监听模式（推荐）**：
```bash
python deploy.py --watch
```
文件改动会自动重新部署！

### 修改后端

1. 编辑 `backend/app_jinja2.py`
2. Flask 自动重启（debug模式）
3. 刷新浏览器

---

## 默认账号

如果数据库已初始化，可以使用：

- **Username**: `admin`
- **Password**: `123456`

或注册新账号：http://localhost:5001/register

---

## 架构特点

✅ **前后端分离开发**：源码在 `frontend_src`，运行时自动挂载到 `backend`

✅ **Jinja2 模板引擎**：服务端渲染，符合课程要求

✅ **自动化部署**：`deploy.py` 脚本一键部署

✅ **Session 管理**：基于 Flask session，无需 localStorage

---

## 常用命令

```bash
# 部署前端（单次）
python deploy.py

# 部署前端（监听模式）
python deploy.py --watch

# 启动应用（包含部署）
python run.py

# 手动启动Flask
cd backend
python app_jinja2.py
```

---

## 注意事项

⚠️ **不要直接编辑** `backend/templates/` 和 `backend/static/`

✅ **始终编辑** `frontend_src/` 下的文件

✅ **修改后运行** `python deploy.py`

---

详细文档：[JINJA2_ARCHITECTURE.md](JINJA2_ARCHITECTURE.md)
