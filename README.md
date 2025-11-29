# 📈 Stock Watch & Alert System - Jinja2版本

> 基于Flask + Jinja2模板引擎的股票监控与警报系统
>
> **分支**: `feature/jinja2-refactor`

---

## 🎯 项目简介

这是一个使用**Flask框架**和**Jinja2模板引擎**开发的股票监控与警报Web应用，采用**服务端渲染（SSR）**架构，符合Python Web开发课程要求。

### 核心特性

✅ **Flask + Jinja2**：服务端模板渲染
✅ **Bootstrap 5**：响应式设计
✅ **SQLite数据库**：用户、股票、警报数据管理
✅ **Session管理**：安全的用户认证
✅ **实时更新**：后台线程自动更新股价
✅ **前后端分离开发**：保持代码清晰，部署时自动整合

---

## 🚀 快速开始

### 1. 克隆项目并切换分支

```bash
cd stockMarketScanner&AlertSystem
git checkout feature/jinja2-refactor
```

### 2. 一键启动

```bash
python run.py
```

### 3. 访问应用

打开浏览器：http://localhost:5001

---

## 📁 项目结构

```
stockMarketScanner&AlertSystem/
│
├── 📂 frontend_src/           # 🎨 前端源码（开发目录）
│   ├── templates/             # Jinja2 模板
│   │   ├── base.html          # 基础模板
│   │   ├── login.html         # 登录页面
│   │   ├── register.html      # 注册页面
│   │   ├── dashboard.html     # 仪表板
│   │   ├── watchlist.html     # 关注列表
│   │   ├── alerts.html        # 警报管理
│   │   ├── stock-detail.html  # 股票详情
│   │   └── settings.html      # 设置页面
│   └── static/                # 静态资源
│       ├── css/style.css
│       ├── js/config.js
│       └── js/modal.js
│
├── 📂 backend/                # 🔧 后端代码
│   ├── app_jinja2.py          # ⭐ Flask应用（Jinja2版本）
│   ├── database.py            # 数据库初始化
│   ├── stock_app.db           # SQLite数据库
│   ├── templates/             # 🚫 自动生成（运行时挂载）
│   └── static/                # 🚫 自动生成（运行时挂载）
│
├── 📜 deploy.py               # ⭐ 部署脚本
├── 📜 run.py                  # ⭐ 快速启动脚本
├── 📜 .gitignore              # Git忽略规则
│
├── 📖 JINJA2_ARCHITECTURE.md  # 详细架构文档
├── 📖 QUICKSTART_JINJA2.md    # 快速开始指南
├── 📖 REFACTOR_SUMMARY.md     # 重构总结
└── 📖 ARCHITECTURE_COMPARISON.md  # 架构对比
```

---

## 🛠️ 开发指南

### 修改前端代码

1. **编辑** `frontend_src/templates/*.html` 或 `frontend_src/static/*`

2. **重新部署**：
   ```bash
   python deploy.py
   ```

3. **刷新浏览器**查看效果

**推荐**：使用监听模式自动部署
```bash
python deploy.py --watch
```

### 修改后端代码

1. **编辑** `backend/app_jinja2.py`

2. Flask会自动重启（debug模式）

3. **刷新浏览器**查看效果

---

## 📋 功能列表

### ✅ 已实现

- ✅ 用户注册与登录
- ✅ Session管理
- ✅ 股票关注列表
- ✅ 价格警报设置
- ✅ 实时股价更新（后台线程）
- ✅ 响应式设计（Bootstrap 5）
- ✅ Flash消息通知
- ✅ 密码修改

### 🚧 待完善

- [ ] 股票价格趋势图（Chart.js）
- [ ] 邮件警报通知
- [ ] 数据导出（CSV/Excel）
- [ ] 二维码分享功能

---

## 🎓 课程要求对应

根据课程评分标准：

### ✅ Flask (30%)
- ✅ 数据库操作（SQLite）
- ✅ **模板引擎**（Jinja2）⭐
- ✅ 路由和视图函数
- ✅ 表单处理（POST）
- ✅ **Session管理**⭐

### ✅ Bootstrap (10%)
- ✅ 响应式设计（RWD）
- ✅ Bootstrap组件（卡片、表单、导航栏、模态框）
- ✅ Bootstrap布局（Grid系统）

### ✅ UI (10%)
- ✅ HTML5语义化标签
- ✅ 自定义CSS样式
- ✅ 配色方案和间距

### ✅ UX (20%)
- ✅ 表单交互和验证
- ✅ Flash消息反馈
- ✅ 登录状态保持
- ✅ 友好的错误提示

### 🚧 额外功能 (20% = 4×5%)
1. ✅ **实时股价更新**（后台线程）
2. 📊 **图表可视化**（Chart.js）- 待实现
3. 📧 **邮件警报**（SMTP）- 待实现
4. 📥 **数据导出**（Pandas）- 待实现

---

## 🎨 Jinja2 模板示例

### 模板继承

**base.html**:
```html
<!DOCTYPE html>
<html>
<head>{% block head %}{% endblock %}</head>
<body>
    {% block navbar %}{% endblock %}
    {% block content %}{% endblock %}
</body>
</html>
```

**login.html**:
```html
{% extends "base.html" %}
{% block content %}
  <form method="POST">
    <input name="username">
    <button>Login</button>
  </form>
{% endblock %}
```

### 变量渲染

```html
<h1>Welcome, {{ current_user.username }}!</h1>
<p>Price: ${{ stock.current_price|round(2) }}</p>
```

### 条件和循环

```html
{% if current_user %}
  <p>Hello, {{ current_user.username }}</p>
{% endif %}

{% for stock in watchlist %}
  <tr>
    <td>{{ stock.stock_symbol }}</td>
    <td>${{ stock.current_price }}</td>
  </tr>
{% endfor %}
```

### URL生成

```html
<a href="{{ url_for('dashboard') }}">Dashboard</a>
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

---

## 🔧 常用命令

```bash
# 单次部署前端
python deploy.py

# 监听模式（自动部署）
python deploy.py --watch

# 一键启动（部署 + 启动Flask）
python run.py

# 手动启动Flask
cd backend
python app_jinja2.py
```

---

## ⚠️ 重要提示

### ❌ 不要直接修改
- `backend/templates/`
- `backend/static/`

这些目录是由 `deploy.py` 自动生成的，手动修改会在下次部署时被覆盖！

### ✅ 始终修改
- `frontend_src/templates/`
- `frontend_src/static/`

---

## 🌳 分支说明

### `main` 分支
- 原始架构：RESTful API + 前端JavaScript
- 前后端完全分离
- 使用localStorage存储用户信息

### `feature/jinja2-refactor` 分支（当前）
- Jinja2模板引擎架构
- 服务端渲染（SSR）
- 使用Session管理用户状态
- **推荐用于课程项目** ⭐

切换分支：
```bash
# 切换到API模式
git checkout main

# 切换到Jinja2模式
git checkout feature/jinja2-refactor
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [JINJA2_ARCHITECTURE.md](JINJA2_ARCHITECTURE.md) | 详细架构说明 |
| [QUICKSTART_JINJA2.md](QUICKSTART_JINJA2.md) | 快速开始指南 |
| [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md) | 重构总结 |
| [ARCHITECTURE_COMPARISON.md](ARCHITECTURE_COMPARISON.md) | API vs Jinja2对比 |
| [PRD.md](PRD.md) | 产品需求文档 |

---

## 🐛 常见问题

### Q: 为什么访问页面显示404？

A: 确保已经运行了部署脚本：
```bash
python deploy.py
```

### Q: 修改前端代码不生效？

A: 需要重新部署：
```bash
python deploy.py
```

或使用监听模式：
```bash
python deploy.py --watch
```

### Q: 如何重置数据库？

A: 重新初始化数据库：
```bash
cd backend
python database.py
```

### Q: 监听模式是什么？

A: 运行 `python deploy.py --watch` 后，脚本会每2秒检测 `frontend_src` 的文件变化，自动重新部署。

---

## 🎯 下一步计划

### 高优先级
1. [ ] 完成所有页面的Jinja2模板改造
2. [ ] 添加Chart.js图表功能
3. [ ] 测试所有功能路径

### 中优先级
4. [ ] 实现邮件警报通知
5. [ ] 添加数据导出功能（CSV/Excel）
6. [ ] 优化UI/UX

### 低优先级
7. [ ] 准备演示PPT
8. [ ] 录制功能演示视频

---


---

**最后更新**: 2025-11-15
**分支**: feature/jinja2-refactor
**状态**: 开发中
