# Jinja2 架构说明

## 架构概述

本项目采用 **前后端分离开发 + 部署时挂载** 的架构模式：

```
开发阶段：
  frontend_src/     ← 前端源码（独立开发）
  backend/          ← 后端代码（独立开发）

部署/运行阶段：
  deploy.py 脚本   → 将 frontend_src 复制到 backend/templates 和 backend/static
  run.py 脚本      → 自动部署并启动应用
```

### 优势

✅ **前后端分离开发**：开发时前后端代码分开，便于管理
✅ **使用Jinja2模板引擎**：符合课程要求，服务端渲染
✅ **自动化部署**：一键部署，无需手动复制文件
✅ **支持监听模式**：前端修改后自动重新部署

---

## 目录结构

```
stockMarketScanner&AlertSystem/
│
├── frontend_src/              # 前端源码（开发目录）
│   ├── templates/             # Jinja2 模板
│   │   ├── base.html          # 基础模板（所有页面继承）
│   │   ├── login.html         # 登录页面
│   │   ├── register.html      # 注册页面
│   │   ├── dashboard.html     # 仪表板
│   │   ├── watchlist.html     # 关注列表
│   │   ├── alerts.html        # 警报管理
│   │   ├── stock-detail.html  # 股票详情
│   │   └── settings.html      # 设置页面
│   │
│   └── static/                # 静态资源
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   ├── config.js
│       │   └── modal.js
│       └── images/
│
├── backend/                   # 后端代码
│   ├── app_jinja2.py          # Flask应用（Jinja2版本）⭐
│   ├── database.py            # 数据库初始化
│   ├── stock_app.db           # SQLite数据库
│   │
│   ├── templates/             # 部署目标（自动生成，不要手动编辑）
│   └── static/                # 部署目标（自动生成，不要手动编辑）
│
├── deploy.py                  # 部署脚本 ⭐
├── run.py                     # 快速启动脚本 ⭐
│
└── frontend/                  # 旧的前端代码（保留作为参考）
```

---

## 核心文件说明

### 1. `frontend_src/templates/base.html`

基础模板，所有页面都继承自它：

```html
{% block navbar %}{% endblock %}
{% block content %}{% endblock %}
{% block extra_js %}{% endblock %}
```

**特性**：
- 统一的导航栏
- Bootstrap 5 集成
- Flash消息显示
- 用户信息注入 (`current_user`)

### 2. `backend/app_jinja2.py`

Flask应用主文件，使用Jinja2模板引擎：

**核心功能**：
- ✅ Session管理（登录状态）
- ✅ 模板渲染 (`render_template()`)
- ✅ 路由保护 (`@login_required`)
- ✅ Flash消息 (`flash()`)
- ✅ 上下文注入 (`@context_processor`)

**路由示例**：
```python
@app.route('/dashboard')
@login_required
def dashboard():
    # 从数据库获取数据
    data = get_data_from_db()
    # 渲染模板并传递数据
    return render_template('dashboard.html', data=data)
```

### 3. `deploy.py`

部署脚本，将前端挂载到后端：

**使用方式**：

```bash
# 单次部署
python deploy.py

# 监听模式（自动检测文件变化并重新部署）
python deploy.py --watch
```

**工作流程**：
1. 清空 `backend/templates` 和 `backend/static`
2. 复制 `frontend_src/templates/` → `backend/templates/`
3. 复制 `frontend_src/static/` → `backend/static/`

### 4. `run.py`

快速启动脚本（推荐使用）：

```bash
python run.py
```

**自动执行**：
1. 运行 `deploy.py` 部署前端
2. 启动 `backend/app_jinja2.py` Flask应用

---

## 开发工作流

### 修改前端代码

1. 编辑 `frontend_src/templates/*.html` 或 `frontend_src/static/*`
2. 运行部署脚本：
   ```bash
   python deploy.py
   ```
3. 刷新浏览器查看效果

**推荐**：使用监听模式自动部署
```bash
python deploy.py --watch
```

### 修改后端代码

1. 编辑 `backend/app_jinja2.py`
2. Flask 自动重启（debug模式）
3. 刷新浏览器查看效果

---

## Jinja2 模板语法示例

### 1. 模板继承

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>{% block head %}{% endblock %}</head>
<body>{% block content %}{% endblock %}</body>
</html>

<!-- login.html -->
{% extends "base.html" %}
{% block content %}
  <h1>Login Page</h1>
{% endblock %}
```

### 2. 变量渲染

```html
<h1>Welcome, {{ current_user.username }}!</h1>
<p>Price: ${{ stock.current_price|round(2) }}</p>
```

### 3. 条件判断

```html
{% if current_user %}
  <p>Hello, {{ current_user.username }}</p>
{% else %}
  <a href="{{ url_for('login') }}">Login</a>
{% endif %}
```

### 4. 循环

```html
{% for stock in watchlist %}
  <tr>
    <td>{{ stock.stock_symbol }}</td>
    <td>{{ stock.current_price }}</td>
  </tr>
{% endfor %}
```

### 5. URL生成

```html
<a href="{{ url_for('dashboard') }}">Dashboard</a>
<a href="{{ url_for('stock_detail', symbol='AAPL') }}">AAPL</a>

<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/config.js') }}"></script>
```

### 6. Flash消息

```python
# 后端
flash('Login successful!', 'success')
flash('Error occurred!', 'danger')
```

```html
<!-- 前端模板 -->
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
```

---

## 启动应用

### 方式1：快速启动（推荐）

```bash
python run.py
```

### 方式2：手动启动

```bash
# 1. 部署前端
python deploy.py

# 2. 启动应用
cd backend
python app_jinja2.py
```

### 访问应用

打开浏览器访问：http://localhost:5001

---

## 与前后端分离的区别

| 特性 | 前后端分离 | Jinja2架构 |
|------|-----------|------------|
| 前端技术 | React/Vue + API调用 | Jinja2模板 + 表单提交 |
| 数据传输 | JSON (API) | HTML渲染 |
| 路由 | 前端路由 | 后端路由 |
| 状态管理 | localStorage/JWT | Session |
| 页面跳转 | 前端路由切换 | 服务器重定向 |

**Jinja2架构的优势**：
- ✅ 更简单，适合学习
- ✅ SEO友好（服务端渲染）
- ✅ 无需复杂的前端框架
- ✅ 符合Flask课程要求

---

## 注意事项

⚠️ **不要直接修改** `backend/templates/` 和 `backend/static/`，这些是自动生成的！

✅ **始终修改** `frontend_src/` 下的文件

✅ **修改后运行** `python deploy.py` 重新部署

✅ **推荐使用** `python run.py` 一键启动

---

## 课程评分对应

根据课程要求（`final project.pdf`）：

### ✅ Flask (30%)
- ✅ 数据库集成（SQLite）
- ✅ 模板引擎（Jinja2）⭐
- ✅ 路由和视图
- ✅ 表单处理
- ✅ Session管理

### ✅ Bootstrap (10%)
- ✅ 响应式设计（RWD）
- ✅ Bootstrap组件（卡片、表单、导航栏）
- ✅ Bootstrap布局（Grid系统）

### ✅ UI (10%)
- ✅ HTML5语义化
- ✅ CSS样式
- ✅ 配色和间距

### ✅ UX (20%)
- ✅ 表单交互
- ✅ Flash消息反馈
- ✅ 登录状态保持
- ✅ 友好的错误提示

### ✅ 额外功能 (20% = 4×5%)
可以添加以下任意4个功能：
1. 实时股价更新（后台线程）✅
2. 图表可视化（Chart.js）
3. 邮件警报通知
4. 数据导出（CSV/Excel）
5. 二维码分享
6. 爬虫获取真实股价

---

## 下一步

1. 完善其他页面的Jinja2模板（dashboard, watchlist, alerts等）
2. 添加前端表单验证
3. 实现图表功能（Chart.js）
4. 添加额外功能（达到20分要求）
5. 准备演示PPT

---

## 常见问题

### Q: 为什么要分离 frontend_src 和 backend？

A: 为了保持开发的独立性和清晰性。前端开发者可以专注于 `frontend_src`，后端开发者专注于 `backend`，部署时通过脚本自动整合。

### Q: 能否直接在 backend/templates 中开发？

A: 可以，但不推荐。一旦重新运行 `deploy.py`，你的修改会被覆盖。

### Q: 监听模式 (--watch) 是如何工作的？

A: 脚本会每2秒检查 `frontend_src` 的文件变化（通过MD5哈希），一旦检测到变化就自动重新部署。

### Q: 如何切换回API模式？

A: 使用 `backend/app.py`（原始的RESTful API版本）代替 `app_jinja2.py`。
