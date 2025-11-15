# Stock Watch & Alert Web App - 產品需求文檔 (PRD)

## 📋 專案概述

### 專案名稱
Stock Watch & Alert Web App

### 專案目標
開發一個基於 Flask 的股票監控與提醒 Web 應用程式,讓用戶能夠:
- 註冊/登入個人帳戶
- 建立個人股票觀察清單
- 查看股價數據與歷史走勢圖表
- 設定價格提醒通知

### 目標用戶
- 對股票投資有興趣的初學者
- 需要簡單工具追蹤股票的個人投資者
- Flask 初學者作為學習專案

### 技術棧
- **後端**: Flask (Python)
- **前端**: Bootstrap 5
- **資料庫**: SQLite
- **數據獲取**: Python 腳本 (手動執行,不需即時 API)
- **圖表**: Chart.js (簡單易用的 JavaScript 圖表庫)
- **其他**: Flask-Login, werkzeug (密碼加密)

### 專案特點 (適合初學者)
- **無需即時 API**: 使用手動腳本獲取數據,降低複雜度
- **數據庫驅動**: 所有數據存儲在 SQLite,易於理解
- **簡單圖表**: 使用前端圖表庫,無需複雜的 Python 圖表生成
- **循序漸進**: 從基礎功能開始,逐步增加難度

---

## 🎯 功能需求

### 1. 用戶認證系統 (30%)

#### 1.1 用戶註冊
- **功能描述**: 新用戶可以建立帳戶
- **輸入欄位**:
  - 用戶名 (Username): 3-20 字元,唯一性
  - 電子郵件 (Email): 有效的 email 格式,唯一性
  - 密碼 (Password): 最少 6 字元
  - 確認密碼 (Confirm Password): 必須與密碼一致
- **安全要求**:
  - 密碼使用 `werkzeug.security` 進行 hash 儲存
  - 表單驗證防止 SQL injection
- **錯誤處理**:
  - 用戶名或 email 已存在時顯示錯誤訊息
  - 密碼不匹配時提示用戶

#### 1.2 用戶登入
- **功能描述**: 已註冊用戶可以登入系統
- **輸入欄位**:
  - 用戶名或電子郵件
  - 密碼
- **功能要求**:
  - 使用 Flask-Login 管理 session
  - "記住我" 選項 (optional)
  - 登入失敗時顯示友好提示
- **安全要求**:
  - 密碼驗證使用 hash 比對
  - 限制登入嘗試次數 (optional)

#### 1.3 用戶登出
- **功能描述**: 用戶可以安全登出系統
- **要求**: 清除 session,重定向到登入頁面

---

### 2. 股票觀察清單 (Watchlist) (20%)

#### 2.1 新增股票
- **功能描述**: 用戶可以將股票加入觀察清單
- **輸入方式**:
  - 股票代碼輸入框 (例如: AAPL, TSLA, GOOGL)
  - 支援美股代碼
- **驗證**:
  - 檢查股票代碼是否有效
  - 防止重複新增同一股票
- **儲存**: 儲存到 SQLite 資料庫,關聯到當前用戶

#### 2.2 移除股票
- **功能描述**: 用戶可以從觀察清單移除股票
- **操作方式**: 每個股票旁邊有刪除按鈕
- **確認**: 刪除前彈出確認對話框 (optional)

#### 2.3 顯示觀察清單
- **功能描述**: 以表格形式顯示用戶的所有觀察股票
- **顯示資訊**:
  - 股票代碼
  - 股票名稱
  - 當前價格
  - 漲跌幅 (%)
  - 漲跌金額
  - 最後更新時間
- **視覺效果**:
  - 上漲顯示綠色
  - 下跌顯示紅色
  - 使用 Bootstrap 表格樣式

---

### 3. 數據獲取腳本 (Data Fetcher Script) (20%)

#### 3.1 手動腳本設計
- **腳本名稱**: `fetch_stock_data.py`
- **執行方式**: 手動在終端執行 `python fetch_stock_data.py`
- **功能描述**:
  - 讀取資料庫中所有用戶觀察的股票代碼
  - 從數據源獲取股價資訊
  - 將數據儲存到 SQLite 資料庫
- **數據來源**:
  - 使用簡單的 CSV 檔案模擬數據 (最簡單)
  - 或使用 `yfinance` 庫 (稍進階)
- **初學者友好設計**:
  - 腳本有清晰的輸出訊息 (例如: "正在獲取 AAPL 數據...")
  - 錯誤處理友好提示
  - 可以看到進度

#### 3.2 儲存的股票數據
- **即時數據** (每次執行腳本更新):
  - 股票代碼
  - 股票名稱
  - 當前價格
  - 開盤價
  - 昨日收盤價
  - 最高價/最低價
  - 漲跌金額
  - 漲跌幅 (%)
  - 更新時間

- **歷史數據** (用於繪製圖表):
  - 日期
  - 收盤價
  - 成交量

#### 3.3 數據顯示
- **顯示方式**: Flask 從資料庫讀取數據顯示
- **刷新機制**:
  - 用戶手動執行腳本更新數據
  - 頁面顯示最後更新時間
  - 頁面有"數據可能過期"提示 (如果超過 1 天未更新)
- **搜尋功能**:
  - 用戶可以查看已在觀察清單中的股票詳情
  - 不需要即時搜尋外部 API

---

### 4. 價格提醒系統 (Alert System) (15%)

#### 4.1 設定提醒
- **功能描述**: 用戶可以為觀察清單中的股票設定價格提醒
- **提醒類型**:
  - 價格高於某值 (Price Above)
  - 價格低於某值 (Price Below)
- **輸入欄位**:
  - 選擇股票 (下拉選單)
  - 提醒條件 (高於/低於)
  - 目標價格
- **儲存**: 儲存到資料庫

#### 4.2 觸發提醒
- **檢查機制** (初學者友好):
  - 當用戶進入 Dashboard 時檢查
  - 比對資料庫中的股價與提醒目標價格
  - 簡單的 if/else 邏輯判斷
- **通知方式**:
  - 頁面頂部顯示 Bootstrap Alert 橫幅 (綠色/紅色)
  - 顯示觸發的提醒清單
  - 例如: "⚠️ AAPL 已高於 $150!"
- **提醒狀態**:
  - 觸發後標記為"已觸發"
  - 用戶可以刪除或重設提醒
  - 簡單的資料庫欄位更新

#### 4.3 管理提醒
- **顯示**: 列表顯示所有提醒規則
- **操作**:
  - 刪除提醒
  - 暫時停用/啟用提醒 (optional)

---

### 5. 股價圖表 (Chart Display) (10%)

#### 5.1 歷史走勢圖
- **圖表類型**: 折線圖
- **圖表庫**: **Chart.js** (前端 JavaScript 圖表庫)
  - 優點: 簡單易用,無需 Python 圖表生成
  - 互動式,無需後端處理
  - Bootstrap 友好
- **時間範圍** (簡化版):
  - 最近 7 天
  - 最近 30 天
  - (可選) 最近 90 天
- **實現方式**:
  - Flask 從資料庫查詢歷史數據
  - 將數據以 JSON 格式傳給前端
  - 使用 Chart.js 在瀏覽器渲染圖表
- **顯示位置**: 股票詳情頁面

#### 5.2 成交量圖 (可選)
- **圖表類型**: 柱狀圖
- **顯示**: 與價格走勢圖分開顯示
- **初學者可跳過**: 先完成價格圖表即可

---

## 🎨 UI/UX 設計需求

### 整體設計原則 (10%)
- **響應式設計**: 支援桌面、平板、手機
- **一致性**: 統一的配色方案和字體
- **簡潔性**: 避免過多視覺干擾
- **可用性**: 操作流程直觀,減少學習成本

### 配色方案
- **主色調**: 深藍色 (#1e3a5f) - 專業、可信
- **輔助色**:
  - 綠色 (#28a745) - 上漲
  - 紅色 (#dc3545) - 下跌
  - 橙色 (#ffc107) - 提醒/警告
- **背景色**: 淺灰 (#f8f9fa)

### 頁面結構

#### 導航欄 (Navbar)
- **Logo**: 網站名稱
- **選單項目**:
  - 首頁 / Dashboard
  - 我的觀察清單
  - 提醒設定
  - 搜尋
- **右側**:
  - 用戶名下拉選單
  - 登出按鈕

#### 頁面佈局
1. **登入/註冊頁面**
   - 居中卡片式設計
   - 表單驗證提示
   - 切換登入/註冊連結

2. **Dashboard (首頁)**
   - 歡迎訊息
   - 觀察清單快速預覽 (前 5 支股票)
   - 活躍提醒數量統計
   - 快速搜尋框

3. **觀察清單頁面**
   - 新增股票輸入框 + 按鈕
   - 股票表格 (Bootstrap Table)
   - 每行有"查看詳情"和"刪除"按鈕
   - 刷新數據按鈕

4. **股票詳情頁面**
   - 股票基本資訊卡片
   - 歷史走勢圖表
   - 時間範圍選擇按鈕
   - 設定提醒按鈕

5. **提醒管理頁面**
   - 提醒規則列表
   - 新增提醒按鈕 (開啟 Modal)
   - 刪除/編輯操作

### 互動元素
- **按鈕**: Bootstrap 按鈕樣式,懸停效果
- **表單**: 清晰的標籤和占位符
- **Modal**: 用於新增提醒、確認刪除等操作
- **Toast/Alert**: 顯示成功/錯誤訊息
- **Loading Spinner**: 數據載入時顯示

---

## 🗄️ 資料庫設計

### 資料表結構

#### 1. Users (用戶表)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. Watchlist (觀察清單表)
```sql
CREATE TABLE watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stock_symbol VARCHAR(10) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, stock_symbol)
);
```

#### 3. Stock_Data (股票數據表) - **新增**
```sql
CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_symbol VARCHAR(10) NOT NULL,
    stock_name VARCHAR(100),
    current_price DECIMAL(10, 2),
    open_price DECIMAL(10, 2),
    previous_close DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    change_amount DECIMAL(10, 2),
    change_percent DECIMAL(5, 2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_symbol)
);
```

#### 4. Stock_History (歷史數據表) - **新增**
```sql
CREATE TABLE stock_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    close_price DECIMAL(10, 2) NOT NULL,
    volume INTEGER,
    FOREIGN KEY (stock_symbol) REFERENCES stock_data(stock_symbol),
    UNIQUE(stock_symbol, date)
);
```

#### 5. Alerts (提醒表)
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stock_symbol VARCHAR(10) NOT NULL,
    condition VARCHAR(10) NOT NULL, -- 'above' or 'below'
    target_price DECIMAL(10, 2) NOT NULL,
    is_triggered BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    triggered_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_symbol) REFERENCES stock_data(stock_symbol)
);
```

### 資料表關係說明
- **Users** ↔ **Watchlist**: 一對多 (一個用戶可以有多個觀察股票)
- **Users** ↔ **Alerts**: 一對多 (一個用戶可以有多個提醒)
- **Stock_Data** ↔ **Stock_History**: 一對多 (一支股票有多筆歷史記錄)
- **Watchlist** → **Stock_Data**: 多對一 (多個用戶可以觀察同一支股票)

---

## 🔧 技術實現細節

### Flask 路由設計

#### 認證路由
- `GET/POST /register` - 註冊頁面
- `GET/POST /login` - 登入頁面
- `GET /logout` - 登出

#### 主要功能路由
- `GET /` 或 `/dashboard` - 首頁
- `GET /watchlist` - 觀察清單頁面
- `POST /watchlist/add` - 新增股票
- `POST /watchlist/remove/<id>` - 移除股票
- `GET /stock/<symbol>` - 股票詳情頁面 (包含圖表)
- `GET /api/stock/<symbol>/history` - 獲取歷史數據 JSON (給 Chart.js 使用)
- `GET /alerts` - 提醒管理頁面
- `POST /alerts/add` - 新增提醒
- `POST /alerts/delete/<id>` - 刪除提醒

---

### 數據獲取腳本實現

#### 方案一: 使用 CSV 檔案模擬 (最簡單,適合初學者)

**步驟 1**: 建立模擬數據 CSV 檔案 `stock_data_mock.csv`
```csv
symbol,name,current_price,open_price,previous_close,high_price,low_price
AAPL,Apple Inc.,175.50,174.20,173.80,176.00,173.50
TSLA,Tesla Inc.,245.30,243.00,242.50,246.80,241.20
GOOGL,Alphabet Inc.,140.80,139.50,139.20,141.50,138.90
```

**步驟 2**: `fetch_stock_data.py` 腳本範例
```python
import sqlite3
import csv
from datetime import datetime

def fetch_and_update_stocks():
    # 連接資料庫
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()

    # 讀取 CSV 數據
    with open('stock_data_mock.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            symbol = row['symbol']
            print(f"正在更新 {symbol} 的數據...")

            # 計算漲跌
            current = float(row['current_price'])
            prev_close = float(row['previous_close'])
            change_amount = current - prev_close
            change_percent = (change_amount / prev_close) * 100

            # 更新或插入股票數據
            cursor.execute('''
                INSERT OR REPLACE INTO stock_data
                (stock_symbol, stock_name, current_price, open_price,
                 previous_close, high_price, low_price, change_amount,
                 change_percent, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (symbol, row['name'], current, row['open_price'],
                  prev_close, row['high_price'], row['low_price'],
                  change_amount, change_percent, datetime.now()))

            print(f"✓ {symbol} 數據已更新")

    conn.commit()
    conn.close()
    print("\n所有股票數據更新完成!")

if __name__ == "__main__":
    fetch_and_update_stocks()
```

#### 方案二: 使用 yfinance (進階,需要網絡)

**安裝**: `pip install yfinance`

```python
import sqlite3
import yfinance as yf
from datetime import datetime

def fetch_stock_from_yahoo(symbol):
    """從 Yahoo Finance 獲取股票數據"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        return {
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'current_price': info.get('currentPrice', 0),
            'open_price': info.get('open', 0),
            'previous_close': info.get('previousClose', 0),
            'high_price': info.get('dayHigh', 0),
            'low_price': info.get('dayLow', 0)
        }
    except Exception as e:
        print(f"錯誤: 無法獲取 {symbol} 的數據 - {e}")
        return None

def update_stock_data(conn, stock_info):
    """更新資料庫中的股票數據"""
    if not stock_info:
        return

    cursor = conn.cursor()

    # 計算漲跌
    current = stock_info['current_price']
    prev_close = stock_info['previous_close']
    change_amount = current - prev_close
    change_percent = (change_amount / prev_close) * 100 if prev_close > 0 else 0

    cursor.execute('''
        INSERT OR REPLACE INTO stock_data
        (stock_symbol, stock_name, current_price, open_price,
         previous_close, high_price, low_price, change_amount,
         change_percent, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (stock_info['symbol'], stock_info['name'], current,
          stock_info['open_price'], prev_close, stock_info['high_price'],
          stock_info['low_price'], change_amount, change_percent,
          datetime.now()))

    conn.commit()

def fetch_all_watchlist_stocks():
    """獲取所有觀察清單中的股票並更新數據"""
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()

    # 獲取所有獨立的股票代碼
    cursor.execute('SELECT DISTINCT stock_symbol FROM watchlist')
    symbols = [row[0] for row in cursor.fetchall()]

    print(f"發現 {len(symbols)} 支股票需要更新\n")

    for symbol in symbols:
        print(f"正在獲取 {symbol} 的數據...")
        stock_info = fetch_stock_from_yahoo(symbol)
        update_stock_data(conn, stock_info)
        print(f"✓ {symbol} 更新完成\n")

    conn.close()
    print("所有股票數據更新完成!")

if __name__ == "__main__":
    fetch_all_watchlist_stocks()
```

---

### 前端圖表實現 (Chart.js)

#### HTML 模板範例 (`stock_detail.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ stock.stock_name }} - 詳情</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h2>{{ stock.stock_name }} ({{ stock.stock_symbol }})</h2>

    <!-- 圖表容器 -->
    <canvas id="priceChart"></canvas>

    <script>
        // 從 Flask 傳來的數據
        const historyData = {{ history_json | safe }};

        // 準備圖表數據
        const dates = historyData.map(item => item.date);
        const prices = historyData.map(item => item.close_price);

        // 建立圖表
        const ctx = document.getElementById('priceChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: '收盤價',
                    data: prices,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '{{ stock.stock_name }} - 歷史走勢'
                    }
                }
            }
        });
    </script>
</body>
</html>
```

#### Flask 路由範例
```python
from flask import render_template, jsonify
import json

@app.route('/stock/<symbol>')
def stock_detail(symbol):
    # 獲取股票基本數據
    stock = db.execute(
        'SELECT * FROM stock_data WHERE stock_symbol = ?',
        (symbol,)
    ).fetchone()

    # 獲取歷史數據
    history = db.execute(
        'SELECT date, close_price FROM stock_history '
        'WHERE stock_symbol = ? ORDER BY date DESC LIMIT 30',
        (symbol,)
    ).fetchall()

    # 轉換為 JSON
    history_json = json.dumps([
        {'date': row['date'], 'close_price': float(row['close_price'])}
        for row in history
    ])

    return render_template('stock_detail.html',
                          stock=stock,
                          history_json=history_json)
```

---

## ✅ 對應 Project Requirements

| Requirement | 佔分 | 對應功能 |
|-------------|------|----------|
| **Flask** | 30% | - 完整的路由系統 (註冊/登入/觀察清單/提醒/詳情頁)<br>- Jinja2 模板渲染<br>- SQLite 資料庫整合 (5 個表)<br>- Flask-Login 認證管理 |
| **Bootstrap** | 10% | - 響應式佈局 (手機/平板/桌面)<br>- Navbar、Card、Table、Modal 組件<br>- 表單樣式和驗證提示<br>- Alert 橫幅 (提醒通知) |
| **UI** | 10% | - 清晰的 Dashboard 設計<br>- 一致的配色方案 (藍/綠/紅)<br>- Chart.js 股價圖表視覺化<br>- 卡片式資訊呈現 |
| **UX** | 20% | - 流暢的登入/註冊流程<br>- 直觀的觀察清單操作 (新增/刪除)<br>- 即時反饋和錯誤提示<br>- 簡單的提醒設定流程<br>- 數據更新狀態顯示 |
| **Extra Features** | 20% | - **密碼 hash 加密** (werkzeug.security)<br>- **數據獲取腳本** (Python CSV/yfinance)<br>- **前端圖表** (Chart.js)<br>- **資料庫設計** (5 表關聯)<br>- 股價提醒邏輯判斷 |
| **Documentation** | 10% | - 完整的 PRD 文檔<br>- 程式碼註釋<br>- README 使用說明 |

### 🎯 為什麼這個設計適合初學者?

1. **技術難度適中**:
   - 不需要處理複雜的即時 API 請求
   - 使用簡單的 SQLite (不需要 MySQL/PostgreSQL)
   - Chart.js 比 Python 圖表庫更簡單

2. **清晰的學習路徑**:
   - 先學 Flask 路由 → 再學資料庫 → 最後整合前端
   - 可以用 CSV 模擬數據,無需網絡依賴

3. **可展示性強**:
   - 有完整的前後端功能
   - 視覺效果好 (圖表、提醒、響應式設計)
   - 符合所有 project requirements

4. **容易除錯**:
   - 數據在資料庫中,可以直接查看
   - 腳本手動執行,方便測試
   - 無需處理異步、WebSocket 等複雜技術

---

## 🚀 開發階段規劃 (適合初學者)

### Phase 1: 基礎架構 (第 1-2 天)
- [ ] 建立 Flask 專案結構
  - 建立資料夾: `templates/`, `static/css`, `static/js`
  - 建立 `app.py` (主程式)
  - 建立 `database.py` (資料庫初始化)
- [ ] 設定 SQLite 資料庫
  - 建立 5 個資料表
  - 測試資料庫連接
- [ ] 建立基礎 Bootstrap 模板
  - `base.html` (基礎模板,包含 Navbar)
  - 引入 Bootstrap 5 CDN

### Phase 2: 用戶認證系統 (第 3-4 天)
- [ ] 實現用戶註冊功能
  - 建立註冊表單
  - 密碼 hash 加密
  - 儲存到資料庫
- [ ] 實現用戶登入/登出
  - 使用 Flask-Login
  - Session 管理
  - 測試登入流程

### Phase 3: 觀察清單功能 (第 5-6 天)
- [ ] 實現觀察清單 CRUD
  - 新增股票 (輸入股票代碼)
  - 顯示觀察清單 (Bootstrap Table)
  - 刪除股票
- [ ] 建立數據獲取腳本
  - 先使用 CSV 模擬數據 (簡單)
  - 測試腳本執行
  - 數據寫入資料庫

### Phase 4: 股票詳情與圖表 (第 7-8 天)
- [ ] 建立股票詳情頁面
  - 顯示股票基本資訊
  - 漲跌顏色標示
- [ ] 整合 Chart.js 圖表
  - 引入 Chart.js CDN
  - 從資料庫讀取歷史數據
  - 繪製折線圖

### Phase 5: 價格提醒系統 (第 9-10 天)
- [ ] 實現提醒設定功能
  - 建立提醒表單 (Modal)
  - 儲存提醒規則
- [ ] 實現提醒檢查邏輯
  - Dashboard 載入時檢查
  - 顯示觸發的提醒 (Alert 橫幅)
- [ ] 提醒管理頁面
  - 顯示所有提醒
  - 刪除提醒

### Phase 6: UI/UX 優化 (第 11-12 天)
- [ ] 美化頁面設計
  - 統一配色
  - 響應式調整
  - 新增圖標和按鈕樣式
- [ ] 新增錯誤處理
  - 表單驗證提示
  - 友好錯誤訊息
- [ ] 測試使用流程

### Phase 7: 測試與文檔 (第 13-14 天)
- [ ] 功能測試
  - 測試所有路由
  - 測試資料庫操作
- [ ] 撰寫文檔
  - README.md (安裝與使用說明)
  - 程式碼註釋
- [ ] 準備展示
  - 截圖/影片
  - Demo 數據準備

---

## 📝 初學者學習重點

### Flask 基礎概念
1. **路由** (Routes): `@app.route('/path')`
2. **模板渲染**: `render_template('page.html', data=data)`
3. **請求處理**: `request.form.get('field_name')`
4. **資料庫操作**: SQLite 的 CRUD 操作
5. **Session 管理**: Flask-Login

### Bootstrap 使用
1. **Grid System**: 響應式佈局 (`container`, `row`, `col`)
2. **組件**: Navbar, Card, Table, Button, Form, Modal
3. **工具類**: 顏色 (`text-success`, `bg-danger`), 間距 (`mt-3`, `p-4`)

### JavaScript (Chart.js)
1. **基礎語法**: 變數、陣列、map 函數
2. **Chart.js 配置**: 建立折線圖
3. **與 Flask 整合**: 使用 `{{ data | safe }}` 傳遞 JSON

---

## 💡 常見問題與解決方案

### Q1: 如何驗證股票代碼是否有效?
**A**: 簡化版可以直接讓用戶輸入,不做驗證。進階版可以檢查資料庫中是否有該股票數據。

### Q2: 如果忘記執行數據腳本怎麼辦?
**A**: 在頁面顯示"數據最後更新時間",如果超過 24 小時提示用戶執行腳本。

### Q3: Chart.js 不顯示圖表?
**A**: 檢查:
- 是否正確引入 CDN
- JSON 數據格式是否正確
- 瀏覽器 Console 是否有錯誤訊息

### Q4: 資料庫操作出錯?
**A**:
- 檢查資料表是否已建立
- 使用 SQLite Browser 工具查看資料庫
- 確認 SQL 語法正確 (使用 `?` 佔位符防止 SQL injection)

---

## 📝 可選增強功能 (Optional)

如果時間充足且想挑戰更高分數,可以考慮:

### 簡單增強 (推薦)
1. **成交量圖表**
   - 在價格圖表下方新增柱狀圖
   - 使用 Chart.js 的混合圖表

2. **搜尋功能**
   - 在 Dashboard 新增搜尋框
   - 搜尋觀察清單中的股票

3. **排序功能**
   - 觀察清單按漲跌幅排序
   - 點擊表頭排序

4. **個人資料頁面**
   - 修改密碼
   - 查看帳戶資訊

### 進階增強 (挑戰)
5. **Email 通知**
   - 使用 Flask-Mail
   - 提醒觸發時發送郵件

6. **多股票對比**
   - 在同一圖表對比多支股票
   - Chart.js 多條折線

7. **深色模式**
   - Bootstrap 主題切換
   - 儲存用戶偏好

---

## 📚 參考資源

### 官方文檔
- [Flask 官方文檔](https://flask.palletsprojects.com/) - 後端框架
- [Bootstrap 5 文檔](https://getbootstrap.com/docs/5.0/) - 前端框架
- [Chart.js 文檔](https://www.chartjs.org/docs/latest/) - 圖表庫
- [Flask-Login 文檔](https://flask-login.readthedocs.io/) - 認證系統
- [SQLite 教學](https://www.sqlitetutorial.net/) - 資料庫

### 教學資源
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) - 完整 Flask 教學
- [Bootstrap 5 Crash Course](https://www.youtube.com/watch?v=4sosXZsdy-s) - Bootstrap 快速入門
- [Chart.js Tutorial](https://www.chartjs.org/docs/latest/getting-started/) - 圖表教學

### 工具
- [DB Browser for SQLite](https://sqlitebrowser.org/) - 資料庫管理工具
- [Postman](https://www.postman.com/) - API 測試工具
- [VS Code](https://code.visualstudio.com/) - 程式碼編輯器

---

## 📄 授權與聲明

本專案僅供教育用途,股票數據僅供參考,不構成投資建議。

---

## 🎉 總結

這個 PRD 為你提供了:
- ✅ **完整的功能需求** - 涵蓋所有 project requirements
- ✅ **詳細的技術設計** - 資料庫結構、路由設計、範例程式碼
- ✅ **適合初學者** - 使用手動腳本,無需複雜的即時 API
- ✅ **14 天開發計劃** - 清晰的時間規劃
- ✅ **學習重點整理** - Flask、Bootstrap、Chart.js 核心概念
- ✅ **常見問題解答** - 提前預防可能遇到的問題

### 下一步建議:
1. **建立專案資料夾結構** - 開始組織你的檔案
2. **設定開發環境** - 安裝 Python、Flask、相關套件
3. **按照 Phase 1 開始** - 建立基礎架構
4. **每天檢視進度** - 對照開發計劃調整

祝你專案順利! 如果有任何問題,隨時詢問。💪
