# 📈 Stock Watch & Alert System

股票監控與提醒 Web 應用程式 - 前後端分離版本

---

## 🎯 專案特點

- ✅ **前後端完全分離** - 後端 Flask API + 前端原生 HTML/CSS/JavaScript
- ✅ **不使用框架** - 無需學習 React/Vue,適合初學者
- ✅ **RESTful API** - 標準 JSON 格式通訊
- ✅ **兩人協作友好** - 前後端可獨立開發
- ✅ **符合課程要求** - Flask 30% + Bootstrap 10% + UI/UX 30% + Extra 20%

---

## 📁 專案結構

```
stockMarketScanner&AlertSystem/
│
├── backend/                # 後端 Flask API
│   ├── app.py             # 主程式 (API 端點)
│   ├── database.py        # 資料庫初始化
│   └── requirements.txt   # Python 依賴
│
├── frontend/               # 前端 HTML/CSS/JS
│   ├── index.html         # 登入頁面
│   ├── watchlist.html     # 觀察清單
│   ├── css/style.css      # 樣式
│   └── js/config.js       # API 配置
│
├── PRD.md                 # 產品需求文檔
├── ARCHITECTURE.md        # 架構說明文檔
└── README.md              # 本文件
```

---

## 🚀 快速啟動

### 步驟 1: 啟動後端

```bash
# 進入後端目錄
cd backend

# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
python database.py

# 啟動 Flask API 伺服器
python app.py
```

✅ 後端將運行在 `http://localhost:5000`

---

### 步驟 2: 啟動前端

**方法 1: 使用 VS Code Live Server (推薦)**
1. 在 VS Code 安裝 "Live Server" 擴充套件
2. 右鍵點擊 `frontend/index.html`
3. 選擇 "Open with Live Server"

✅ 前端將運行在 `http://localhost:5500`

**方法 2: 使用 Python HTTP Server**
```bash
cd frontend
python -m http.server 8080
```

✅ 前端將運行在 `http://localhost:8080`

---

### 步驟 3: 測試

1. 開啟瀏覽器訪問前端 URL
2. 註冊新帳戶
3. 登入系統
4. 新增股票到觀察清單
5. 查看股票詳情

---

## 📡 API 端點

### 認證
- `POST /api/auth/register` - 用戶註冊
- `POST /api/auth/login` - 用戶登入

### 觀察清單
- `GET /api/watchlist/<user_id>` - 獲取觀察清單
- `POST /api/watchlist` - 新增股票
- `DELETE /api/watchlist/<id>` - 刪除股票

### 股票數據
- `GET /api/stock/<symbol>` - 獲取股票詳情
- `GET /api/stock/<symbol>/history` - 獲取歷史數據

### 提醒
- `GET /api/alerts/<user_id>` - 獲取提醒列表
- `POST /api/alerts` - 新增提醒
- `DELETE /api/alerts/<id>` - 刪除提醒
- `GET /api/alerts/check/<user_id>` - 檢查觸發的提醒

詳細 API 文檔請查看 `ARCHITECTURE.md`

---

## 🔄 前後端交互流程

```
前端 (瀏覽器)              後端 (Flask API)           資料庫 (SQLite)
     │                           │                           │
     │  HTTP Request (JSON)      │                           │
     ├──────────────────────────>│                           │
     │                           │  SQL Query                │
     │                           ├──────────────────────────>│
     │                           │                           │
     │                           │  Data                     │
     │                           │<──────────────────────────┤
     │  JSON Response            │                           │
     │<──────────────────────────┤                           │
     │                           │                           │
     │  JavaScript 渲染 HTML     │                           │
     └───────────────────────────┘                           │
```

---

## 👥 兩人協作開發

### 後端開發者
1. 負責 `backend/` 資料夾
2. 編寫 API 端點
3. 測試 API (使用 Postman)
4. 提供 API 文檔給前端

### 前端開發者
1. 負責 `frontend/` 資料夾
2. 設計頁面 UI (HTML/CSS)
3. 編寫 JavaScript 調用 API
4. 處理用戶交互

### 協作流程
1. **後端先行**: 建立 API 並測試
2. **前端對接**: 根據 API 文檔調用接口
3. **聯調測試**: 同時運行前後端,測試完整流程

---

## 🛠️ 技術棧

### 後端
- Python 3.x
- Flask 3.0
- Flask-CORS
- SQLite
- Werkzeug (密碼加密)

### 前端
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Chart.js (圖表)

---

## 📚 文檔

- **PRD.md** - 完整的產品需求文檔
- **ARCHITECTURE.md** - 詳細的架構說明和範例
- **README.md** - 本快速啟動指南

---

## 🎓 學習重點

### 後端 (Flask)
- RESTful API 設計
- JSON 數據處理
- 資料庫操作 (SQLite)
- CORS 處理

### 前端 (原生 JS)
- Fetch API 使用
- JSON 解析
- DOM 操作
- LocalStorage 使用

### 整合
- 前後端數據傳遞
- 用戶認證流程
- 錯誤處理

---

## ❓ 常見問題

### Q: 為什麼選擇前後端分離?
**A**:
- 更接近實際開發流程
- 兩人可以同時開發
- 易於維護和擴展
- 為未來學習 React/Vue 打基礎

### Q: 為什麼不用 React/Vue?
**A**:
- 降低學習成本
- 專注理解前後端分離概念
- 原生 JavaScript 是基礎

### Q: 遇到 CORS 錯誤怎麼辦?
**A**:
- 確保後端已安裝 `flask-cors`
- 確保前端使用 HTTP Server (不是直接開啟 HTML)
- 檢查 API URL 是否正確

### Q: 如何測試 API?
**A**:
- 使用 Postman 或 Insomnia
- 使用瀏覽器開發者工具 (Network tab)
- 查看 Flask 終端輸出

---

## 📝 開發檢查清單

### 後端
- [ ] 資料庫已初始化
- [ ] 所有 API 端點已實現
- [ ] API 已測試通過 (Postman)
- [ ] CORS 已正確配置

### 前端
- [ ] 所有頁面已建立
- [ ] API 配置正確
- [ ] 用戶認證流程正常
- [ ] 所有功能可正常使用

### 整合
- [ ] 前後端可正常通訊
- [ ] 錯誤處理完善
- [ ] UI/UX 友好
- [ ] 響應式設計測試通過

---

## 📄 授權

本專案僅供教育用途。

---

## 🎉 下一步

1. 查看 `ARCHITECTURE.md` 了解詳細架構
2. 查看 `PRD.md` 了解完整需求
3. 開始編寫程式碼!

**祝開發順利! 💪**
