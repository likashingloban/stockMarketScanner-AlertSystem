# 架构对比：API模式 vs Jinja2模式

## 🌳 分支结构

```
main (原始架构)
 └── feature/jinja2-refactor (Jinja2架构)
```

---

## 📊 架构对比图

### 原架构（main分支）：前后端完全分离

```
┌─────────────────────────────────────────────────────────────┐
│                     浏览器 (Browser)                         │
│                                                              │
│  frontend/                                                   │
│  ├── index.html                                              │
│  ├── dashboard.html                                          │
│  └── js/                                                     │
│      ├── config.js ────┐                                     │
│      └── modal.js      │                                     │
│                        │                                     │
│                        │ fetch('/api/login')                 │
│                        │ fetch('/api/watchlist')             │
│                        ▼                                     │
└────────────────────────│─────────────────────────────────────┘
                         │
                         │ HTTP Request (JSON)
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                  Flask Backend (backend/app.py)              │
│                                                              │
│  @app.route('/api/login', methods=['POST'])                 │
│  def login():                                                │
│      data = request.get_json()  # ← JSON                    │
│      return jsonify({'token': ..., 'user': ...})  # ← JSON  │
│                                                              │
│  特点:                                                       │
│  - RESTful API                                               │
│  - 返回 JSON                                                 │
│  - CORS 配置                                                 │
│  - 无 Session                                                │
└──────────────────────────────────────────────────────────────┘
```

**数据流**：
```
用户操作 → JavaScript → fetch API → JSON请求 → Flask → JSON响应 → JavaScript → 更新DOM
```

---

### 新架构（feature/jinja2-refactor）：Jinja2模板渲染

```
┌─────────────────────────────────────────────────────────────┐
│                     浏览器 (Browser)                         │
│                                                              │
│  渲染后的 HTML (服务器生成)                                  │
│  - 包含用户数据                                              │
│  - 包含 Flash 消息                                           │
│  - 动态内容已填充                                            │
│                                                              │
│  <form method="POST" action="/login">                       │
│    <input name="username">                                   │
│    <button type="submit">Login</button>                     │
│  </form>                                 │                   │
│                                          │                   │
│                                          │ POST /login       │
│                                          ▼                   │
└──────────────────────────────────────────│──────────────────┘
                                           │
                                           │ Form Data
                                           │
┌──────────────────────────────────────────▼──────────────────┐
│           Flask Backend (backend/app_jinja2.py)             │
│                                                              │
│  @app.route('/login', methods=['GET', 'POST'])              │
│  def login():                                                │
│      if request.method == 'POST':                            │
│          username = request.form.get('username')  # ← Form  │
│          session['user_id'] = user['id']  # ← Session       │
│          return render_template('dashboard.html', ...)      │
│      return render_template('login.html')                   │
│                                                              │
│  特点:                                                       │
│  - 服务端渲染 (SSR)                                          │
│  - 返回 HTML                                                 │
│  - Session 管理                                              │
│  - Jinja2 模板                                               │
│                         │                                    │
│                         ▼                                    │
│  ┌───────────────────────────────────────┐                  │
│  │   backend/templates/ (运行时挂载)     │                  │
│  │   ├── base.html                       │                  │
│  │   ├── login.html                      │                  │
│  │   └── dashboard.html                  │                  │
│  │                                        │                  │
│  │   {{ current_user.username }}         │                  │
│  │   {% for stock in watchlist %}        │                  │
│  │   {% if condition %}                  │                  │
│  └───────────────────────────────────────┘                  │
│                         ▲                                    │
│                         │                                    │
│                         │ deploy.py 复制                     │
│                         │                                    │
└─────────────────────────│───────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────┐
│           frontend_src/ (开发目录)                           │
│           ├── templates/                                     │
│           │   ├── base.html                                  │
│           │   ├── login.html                                 │
│           │   └── dashboard.html                             │
│           └── static/                                        │
│               ├── css/style.css                              │
│               └── js/modal.js                                │
└──────────────────────────────────────────────────────────────┘
```

**数据流**：
```
用户操作 → 表单提交 → POST请求 → Flask → 渲染模板 → HTML响应 → 浏览器显示
```

---

## 🔀 工作流程对比

### API模式（main分支）

```
开发流程：
1. 修改 frontend/index.html
2. 修改 frontend/js/config.js
3. 刷新浏览器
4. JavaScript 调用 API
5. 后端返回 JSON
6. JavaScript 更新页面

部署：
- 前端：独立托管（Nginx/CDN）
- 后端：Flask API服务器
- 跨域：需要CORS配置
```

### Jinja2模式（feature/jinja2-refactor）

```
开发流程：
1. 修改 frontend_src/templates/login.html
2. 运行 python deploy.py
3. 刷新浏览器
4. 表单提交到后端
5. 后端渲染HTML
6. 返回完整页面

部署：
1. python deploy.py    # 部署前端到后端
2. python app_jinja2.py # 启动Flask
3. 访问 http://localhost:5001

快捷方式：
- python run.py  # 一键启动
- python deploy.py --watch  # 监听模式
```

---

## 📝 代码对比

### 登录功能实现

#### API模式（main分支）

**前端** (`frontend/index.html`):
```javascript
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:5001/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        // 保存到 localStorage
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('token', data.token);

        // 前端跳转
        window.location.href = 'dashboard.html';

    } catch (error) {
        alert(error.message);
    }
});
```

**后端** (`backend/app.py`):
```python
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()  # ← 接收 JSON
    username = data.get('username')
    password = data.get('password')

    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid password'}), 401

    token = secrets.token_urlsafe(32)

    # 返回 JSON
    return jsonify({
        'message': 'Login successful',
        'user': {'id': user['id'], 'username': user['username']},
        'token': token
    }), 200
```

---

#### Jinja2模式（feature/jinja2-refactor）

**前端** (`frontend_src/templates/login.html`):
```html
{% extends "base.html" %}

{% block content %}
<form method="POST" action="{{ url_for('login') }}">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
</form>

<!-- Flash 消息自动显示 -->
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
{% endblock %}
```

**后端** (`backend/app_jinja2.py`):
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # ← 接收表单数据
        password = request.form.get('password')

        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if not check_password_hash(user['password_hash'], password):
            flash('Invalid password', 'danger')  # ← Flash 消息
            return render_template('login.html')

        # 保存到 Session
        session['user_id'] = user['id']
        session['username'] = user['username']

        flash(f'Welcome back, {user["username"]}!', 'success')

        # 服务器端重定向
        return redirect(url_for('dashboard'))

    # GET 请求：渲染登录页面
    return render_template('login.html')
```

---

## 📈 关注列表页面对比

### API模式

**前端** (`frontend/watchlist.html`):
```javascript
async function loadWatchlist() {
    const userId = JSON.parse(localStorage.getItem('user')).id;

    const response = await fetch(`http://localhost:5001/api/watchlist/${userId}`);
    const stocks = await response.json();

    const tableBody = document.getElementById('watchlistTable');
    tableBody.innerHTML = stocks.map(stock => `
        <tr>
            <td>${stock.stock_symbol}</td>
            <td>${stock.current_price}</td>
            <td>${stock.change_percent}%</td>
            <td>
                <button onclick="removeStock(${stock.id})">Remove</button>
            </td>
        </tr>
    `).join('');
}

loadWatchlist();
```

### Jinja2模式

**模板** (`frontend_src/templates/watchlist.html`):
```html
{% extends "base.html" %}

{% block content %}
<table class="table">
    <tbody>
        {% for stock in stocks %}
        <tr>
            <td>{{ stock.stock_symbol }}</td>
            <td>${{ stock.current_price|round(2) }}</td>
            <td>{{ stock.change_percent|round(2) }}%</td>
            <td>
                <form method="POST" action="{{ url_for('remove_from_watchlist', watchlist_id=stock.id) }}">
                    <button type="submit">Remove</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

**后端** (`backend/app_jinja2.py`):
```python
@app.route('/watchlist')
@login_required
def watchlist():
    user_id = session['user_id']  # ← 从 Session 获取

    stocks = db.execute('''
        SELECT w.id, w.stock_symbol, s.current_price, s.change_percent
        FROM watchlist w
        LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
        WHERE w.user_id = ?
    ''', (user_id,)).fetchall()

    # 渲染模板并传递数据
    return render_template('watchlist.html', stocks=[dict(row) for row in stocks])
```

---

## 🎯 优缺点对比

### API模式（main分支）

**优点** ✅：
- 前后端完全解耦
- 适合多端应用（Web、Mobile、Desktop）
- 前端可以独立部署到CDN
- 支持客户端路由（单页应用）
- API可被第三方调用

**缺点** ❌：
- 学习曲线较陡（需要理解异步编程、Promise等）
- SEO不友好（需要SSR或预渲染）
- 需要处理CORS
- 状态管理复杂（localStorage、JWT等）
- 不符合课程要求（未使用模板引擎）

---

### Jinja2模式（feature/jinja2-refactor）

**优点** ✅：
- ✅ **符合课程要求**（Flask + Jinja2模板引擎）
- 学习曲线平缓（传统Web开发）
- SEO友好（服务端渲染）
- 无需CORS配置
- Session管理简单
- 代码量更少
- 调试更容易

**缺点** ❌：
- 前后端耦合度高
- 每次交互都需要刷新页面（可以用AJAX优化）
- 不适合复杂的交互应用
- 服务器负载相对更高

---

## 🎓 课程评分对应

| 评分项 | API模式 | Jinja2模式 |
|--------|---------|-----------|
| **Flask (30%)** | | |
| - 数据库 | ✅ | ✅ |
| - **模板引擎** | ❌ (未使用) | ✅ (Jinja2) |
| - 路由 | ✅ | ✅ |
| - 表单处理 | ❌ (JSON) | ✅ (Form) |
| **Bootstrap (10%)** | ✅ | ✅ |
| **UI (10%)** | ✅ | ✅ |
| **UX (20%)** | ✅ | ✅ |
| **额外功能 (20%)** | ✅ | ✅ |

**结论**：Jinja2模式更符合课程要求！

---

## 🚀 如何在两种模式间切换

### 切换到 API 模式

```bash
git checkout main
cd backend
python app.py
```

访问：http://localhost:5001
前端：直接打开 `frontend/index.html`

### 切换到 Jinja2 模式

```bash
git checkout feature/jinja2-refactor
python run.py
```

访问：http://localhost:5001

---

## 📌 选择建议

### 选择 API 模式 (main分支) 如果：
- 你想学习现代Web开发
- 需要开发移动APP
- 需要API给第三方使用
- 想要单页应用体验

### 选择 Jinja2 模式 (feature/jinja2-refactor) 如果：
- ✅ **课程项目**（强烈推荐）
- 学习Flask基础
- 快速开发MVP
- SEO是主要考虑
- 追求代码简洁

---

## 📚 学习价值

### API模式适合学习：
- RESTful API设计
- 前后端分离架构
- 异步JavaScript编程
- 状态管理（localStorage）
- CORS处理

### Jinja2模式适合学习：
- Flask核心功能
- 模板引擎使用
- 服务端渲染（SSR）
- Session管理
- 表单处理
- **符合课程要求** ⭐

---

## 🎯 总结

| 特性 | API模式 | Jinja2模式 |
|------|---------|-----------|
| 复杂度 | 高 | 低 |
| 学习曲线 | 陡峭 | 平缓 |
| 代码量 | 多 | 少 |
| 性能 | 客户端渲染 | 服务端渲染 |
| SEO | ❌ | ✅ |
| 课程匹配 | ❌ | ✅ ⭐ |

**推荐**：使用 `feature/jinja2-refactor` 分支完成课程项目！
