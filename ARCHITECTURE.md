# Stock Watch - 前後端分離架構說明

## 📋 專案概述

本專案採用**前後端分離**架構,使用**原生 HTML/CSS/JavaScript** (不使用 React/Vue 等框架) 與 **Flask RESTful API** 進行開發。

---

## 🏗️ 專案結構

```
stockMarketScanner&AlertSystem/
│
├── backend/                    # 後端專案 (Flask API)
│   ├── app.py                 # Flask 主程式 - 所有 API 端點
│   ├── database.py            # 資料庫初始化腳本
│   ├── requirements.txt       # Python 依賴套件
│   └── stock_app.db           # SQLite 資料庫 (執行後生成)
│
├── frontend/                   # 前端專案 (純 HTML/CSS/JS)
│   ├── index.html             # 登入頁面
│   ├── register.html          # 註冊頁面
│   ├── dashboard.html         # 儀表板
│   ├── watchlist.html         # 觀察清單
│   ├── stock-detail.html      # 股票詳情頁 (含圖表)
│   ├── alerts.html            # 提醒管理
│   │
│   ├── css/
│   │   └── style.css          # 自定義樣式
│   │
│   └── js/
│       ├── config.js          # API 配置 & 工具函數
│       ├── auth.js            # 認證邏輯 (可選)
│       ├── dashboard.js       # 儀表板邏輯 (可選)
│       ├── watchlist.js       # 觀察清單邏輯 (可選)
│       ├── stock-detail.js    # 股票詳情邏輯 (可選)
│       └── alerts.js          # 提醒邏輯 (可選)
│
├── PRD.md                     # 產品需求文檔
└── ARCHITECTURE.md            # 本文檔
```

---

## 🔄 前後端交互流程

### 1. 整體流程圖

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  前端 (瀏覽器)  │ ──HTTP─→│  Flask API      │ ──SQL──→│  SQLite 資料庫  │
│  HTML/CSS/JS    │ ←─JSON──│  (後端)         │ ←─Data──│                 │
│                 │         │                 │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### 2. 具體交互範例

#### 範例 1: 用戶登入

**前端** (`index.html`):
```javascript
// 用戶點擊登入按鈕
const username = document.getElementById('username').value;
const password = document.getElementById('password').value;

// 發送 POST 請求到後端 API
const response = await fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
});

// 接收 JSON 回應
const data = await response.json();
// { "user": {...}, "token": "xxx" }

// 儲存用戶資料到 localStorage
localStorage.setItem('user', JSON.stringify(data.user));

// 跳轉到 Dashboard
window.location.href = 'dashboard.html';
```

**後端** (`backend/app.py`):
```python
@app.route('/api/auth/login', methods=['POST'])
def login():
    # 接收前端發來的 JSON
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 查詢資料庫
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()

    # 驗證密碼
    if check_password_hash(user['password_hash'], password):
        # 返回 JSON 給前端
        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username']
            },
            'token': 'xxx'
        }), 200
    else:
        return jsonify({'error': '密碼錯誤'}), 401
```

**數據流**:
```
1. 前端 → 後端: POST /api/auth/login
   Body: { "username": "john", "password": "123456" }

2. 後端處理: 查詢資料庫 → 驗證密碼

3. 後端 → 前端: JSON 回應
   { "user": {...}, "token": "xxx" }

4. 前端處理: 儲存用戶資料 → 跳轉頁面
```

---

#### 範例 2: 獲取觀察清單

**前端** (`watchlist.html`):
```javascript
// 從 localStorage 獲取用戶 ID
const user = JSON.parse(localStorage.getItem('user'));
const userId = user.id;

// 發送 GET 請求到後端
const response = await fetch(`http://localhost:5000/api/watchlist/${userId}`);

// 接收 JSON 數據
const stocks = await response.json();
// [
//   { "stock_symbol": "AAPL", "current_price": 175.5, ... },
//   { "stock_symbol": "TSLA", "current_price": 245.3, ... }
// ]

// 渲染到 HTML 表格
const tbody = document.getElementById('watchlistTable');
tbody.innerHTML = stocks.map(stock => `
    <tr>
        <td>${stock.stock_symbol}</td>
        <td>$${stock.current_price}</td>
        ...
    </tr>
`).join('');
```

**後端** (`backend/app.py`):
```python
@app.route('/api/watchlist/<int:user_id>', methods=['GET'])
def get_watchlist(user_id):
    # 查詢資料庫
    conn = get_db()
    stocks = conn.execute('''
        SELECT w.stock_symbol, s.current_price, s.change_percent
        FROM watchlist w
        LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
        WHERE w.user_id = ?
    ''', (user_id,)).fetchall()

    # 將結果轉為 JSON 並返回
    return jsonify([dict(row) for row in stocks]), 200
```

**數據流**:
```
1. 前端 → 後端: GET /api/watchlist/1

2. 後端處理: 查詢資料庫 (JOIN 操作)

3. 後端 → 前端: JSON 陣列
   [{"stock_symbol": "AAPL", "current_price": 175.5}, ...]

4. 前端處理: 動態生成 HTML 表格
```

---

#### 範例 3: 新增股票到觀察清單

**前端** (`watchlist.html`):
```javascript
// 用戶輸入股票代碼
const symbol = document.getElementById('stockSymbolInput').value;

// 發送 POST 請求
const response = await fetch('http://localhost:5000/api/watchlist', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        user_id: user.id,
        stock_symbol: symbol
    })
});

const data = await response.json();
// { "message": "AAPL 已加入觀察清單" }

// 重新載入觀察清單
loadWatchlist();
```

**後端** (`backend/app.py`):
```python
@app.route('/api/watchlist', methods=['POST'])
def add_to_watchlist():
    data = request.get_json()
    user_id = data.get('user_id')
    stock_symbol = data.get('stock_symbol')

    # 插入資料庫
    conn = get_db()
    conn.execute('''
        INSERT INTO watchlist (user_id, stock_symbol)
        VALUES (?, ?)
    ''', (user_id, stock_symbol))
    conn.commit()

    return jsonify({'message': f'{stock_symbol} 已加入觀察清單'}), 201
```

---

## 🔑 關鍵技術點

### 1. CORS (跨域資源共享)

由於前後端分離,前端 (`file://` 或 `http://localhost:8080`) 需要訪問後端 API (`http://localhost:5000`),會遇到跨域問題。

**解決方案**: 使用 `flask-cors`

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
```

---

### 2. 用戶認證

**簡化版**: 使用 `localStorage` 儲存用戶資料

```javascript
// 登入後儲存
localStorage.setItem('user', JSON.stringify({
    id: 1,
    username: 'john',
    token: 'xxx'
}));

// 其他頁面讀取
const user = JSON.parse(localStorage.getItem('user'));

// 登出時清除
localStorage.removeItem('user');
```

**進階版**: 可以使用 JWT (JSON Web Token)

---

### 3. 數據格式

**統一使用 JSON**:
- 前端 → 後端: `JSON.stringify(data)`
- 後端 → 前端: `jsonify(data)`

---

### 4. 錯誤處理

**後端**:
```python
try:
    # 處理邏輯
    return jsonify({'data': result}), 200
except Exception as e:
    return jsonify({'error': str(e)}), 400
```

**前端**:
```javascript
try {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error('請求失敗');
    }
    const data = await response.json();
} catch (error) {
    alert('錯誤: ' + error.message);
}
```

---

## 📡 完整 API 端點列表

### 認證 API

| 方法 | 端點 | 說明 | 請求體 | 回應 |
|------|------|------|--------|------|
| POST | `/api/auth/register` | 用戶註冊 | `{username, email, password}` | `{message, username}` |
| POST | `/api/auth/login` | 用戶登入 | `{username, password}` | `{user, token}` |

### 觀察清單 API

| 方法 | 端點 | 說明 | 請求體 | 回應 |
|------|------|------|--------|------|
| GET | `/api/watchlist/<user_id>` | 獲取觀察清單 | - | `[{stock...}]` |
| POST | `/api/watchlist` | 新增股票 | `{user_id, stock_symbol}` | `{message}` |
| DELETE | `/api/watchlist/<id>` | 刪除股票 | - | `{message}` |

### 股票數據 API

| 方法 | 端點 | 說明 | 請求體 | 回應 |
|------|------|------|--------|------|
| GET | `/api/stock/<symbol>` | 獲取股票詳情 | - | `{stock_data}` |
| GET | `/api/stock/<symbol>/history?days=30` | 獲取歷史數據 | - | `[{date, price}]` |

### 提醒 API

| 方法 | 端點 | 說明 | 請求體 | 回應 |
|------|------|------|--------|------|
| GET | `/api/alerts/<user_id>` | 獲取提醒列表 | - | `[{alert...}]` |
| POST | `/api/alerts` | 新增提醒 | `{user_id, stock_symbol, condition, target_price}` | `{message}` |
| DELETE | `/api/alerts/<id>` | 刪除提醒 | - | `{message}` |
| GET | `/api/alerts/check/<user_id>` | 檢查觸發的提醒 | - | `[{triggered...}]` |

### Dashboard API

| 方法 | 端點 | 說明 | 請求體 | 回應 |
|------|------|------|--------|------|
| GET | `/api/dashboard/<user_id>` | 獲取儀表板數據 | - | `{top_stocks, alert_count}` |

---

## 🚀 如何運行專案

### 1. 啟動後端 (Flask API)

```bash
# 進入後端目錄
cd backend

# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
python database.py

# 啟動 Flask 伺服器
python app.py
```

後端將運行在: `http://localhost:5000`

---

### 2. 啟動前端 (HTML)

**方法 1: 使用 Live Server (推薦)**
- 在 VS Code 安裝 "Live Server" 擴充套件
- 右鍵點擊 `frontend/index.html` → "Open with Live Server"
- 前端將運行在: `http://localhost:5500` (或其他端口)

**方法 2: 使用 Python HTTP Server**
```bash
cd frontend
python -m http.server 8080
```
前端將運行在: `http://localhost:8080`

**方法 3: 直接開啟 HTML 檔案**
- 雙擊 `index.html` 即可 (但可能遇到 CORS 問題)

---

### 3. 測試流程

1. 開啟前端 (`http://localhost:5500`)
2. 註冊新帳戶
3. 登入
4. 新增股票到觀察清單
5. 執行數據腳本更新股價 (如果有)
6. 查看股票詳情和圖表
7. 設定價格提醒

---

## 👥 兩人協作開發流程

### 分工建議

**後端開發者 (負責 `backend/`)**:
1. 建立資料庫結構
2. 編寫 API 端點
3. 測試 API (使用 Postman)
4. 提供 API 文檔給前端

**前端開發者 (負責 `frontend/`)**:
1. 設計頁面佈局 (HTML/CSS)
2. 編寫 JavaScript 邏輯
3. 調用後端 API
4. 處理用戶交互

---

### 協作步驟

#### Step 1: 後端先行
1. 後端開發者建立 API
2. 使用 Postman 測試 API
3. 提供 API 文檔 (端點、請求格式、回應格式)

#### Step 2: 前端對接
1. 前端開發者根據 API 文檔調用接口
2. 使用 `fetch()` 或 `axios` 發送請求
3. 處理返回的 JSON 數據
4. 渲染到 HTML 頁面

#### Step 3: 聯調測試
1. 同時運行前後端
2. 測試完整流程
3. 修復 bug

---

### 溝通要點

**後端提供給前端**:
- API 端點 URL
- 請求方法 (GET/POST/DELETE)
- 請求體格式 (JSON 結構)
- 回應格式 (JSON 結構)
- 錯誤碼和錯誤訊息

**前端提供給後端**:
- 需要哪些數據
- 數據的格式要求
- 頁面交互邏輯

---

## 📝 與 Jinja2 模板方式的對比

| 特性 | 前後端分離 (當前) | Jinja2 模板 (傳統) |
|------|------------------|-------------------|
| **數據傳遞** | JSON (API) | HTML 中嵌入變數 |
| **頁面渲染** | 前端 (JavaScript) | 後端 (Flask) |
| **協作方式** | 前後端可分開開發 | 需要同時處理前後端 |
| **學習難度** | 需要理解 API 概念 | 較簡單 |
| **靈活性** | 高 (前端可獨立開發) | 低 (耦合度高) |
| **適合場景** | 大型專案、團隊協作 | 小型專案、個人開發 |

---

## ✅ 總結

### 優點:
- ✅ 前後端完全分離,可以兩人同時開發
- ✅ 使用標準的 RESTful API,易於擴展
- ✅ 不需要學習 React/Vue,降低學習成本
- ✅ 符合現代 Web 開發趨勢

### 缺點:
- ⚠️ 需要處理 CORS 問題
- ⚠️ 需要手動管理用戶狀態 (localStorage)
- ⚠️ 比 Jinja2 模板稍微複雜一點

### 適合:
- 👥 兩人協作開發
- 📚 學習前後端分離概念
- 🚀 為未來學習 React/Vue 打基礎

---

## 📚 延伸學習

如果想進一步提升,可以學習:
1. **JWT 認證** - 更安全的用戶認證方式
2. **Axios** - 更強大的 HTTP 請求庫
3. **React/Vue** - 現代前端框架
4. **Docker** - 容器化部署
5. **Nginx** - 反向代理,解決 CORS 問題

---

**祝開發順利! 🎉**
