# 🚀 部署指南

前端啟動和部署選項詳解

---

## 📖 目錄

1. [開發環境啟動](#開發環境啟動)
2. [部署選項對比](#部署選項對比)
3. [選項 A: 前後端分離部署](#選項-a-前後端分離部署-推薦)
4. [選項 B: 前端掛載到後端](#選項-b-前端掛載到後端-簡單)
5. [推薦方案](#推薦方案)

---

## 開發環境啟動

### 方法 1: Python HTTP Server (最簡單)

```bash
cd frontend
python -m http.server 8080
```

**訪問**: `http://localhost:8080`

**優點**:
- ✅ 不需要安裝任何工具
- ✅ Python 內建
- ✅ 適合快速測試

---

### 方法 2: VS Code Live Server (最方便)

1. 安裝 VS Code 擴充套件: "Live Server"
2. 右鍵點擊 `frontend/index.html`
3. 選擇 "Open with Live Server"

**訪問**: `http://localhost:5500`

**優點**:
- ✅ 自動刷新
- ✅ 開發效率高
- ✅ 支援熱重載

---

### 方法 3: Node.js http-server (如果有 Node.js)

```bash
cd frontend
npx http-server -p 8080 --cors
```

**優點**:
- ✅ 自動處理 CORS
- ✅ 效能好

---

## 部署選項對比

| 特性 | 選項 A: 分離部署 | 選項 B: 整合部署 |
|------|-----------------|-----------------|
| **架構** | 前後端獨立 | 前端掛載到後端 |
| **伺服器** | 需要 2 個 | 只需要 1 個 |
| **CORS** | 需要處理 | 不需要 |
| **擴展性** | 高 | 中 |
| **部署難度** | 中 | 低 |
| **適合場景** | 生產環境、團隊協作 | 個人專案、快速部署 |

---

## 選項 A: 前後端分離部署 (推薦)

**現在的架構就是這樣**

### 架構圖

```
┌─────────────────────┐         ┌─────────────────────┐
│  Frontend Server    │         │  Backend Server     │
│  (靜態檔案)         │ ──API──→│  (Flask API)        │
│  http://前端.com    │ ←─JSON──│  http://API.com     │
└─────────────────────┘         └─────────────────────┘
```

### 開發啟動

**終端 1 - 後端**:
```bash
cd backend
python app.py
# 運行在 http://localhost:5000
```

**終端 2 - 前端**:
```bash
cd frontend
python -m http.server 8080
# 運行在 http://localhost:8080
```

### 部署方案

#### 前端部署 (選一個):

**1. Netlify (推薦 - 免費)**
```bash
# 1. 建立 netlify.toml
cd frontend
cat > netlify.toml << EOF
[build]
  publish = "."
EOF

# 2. 部署
# 方法 1: 拖曳 frontend 資料夾到 Netlify 網站
# 方法 2: 使用 Netlify CLI
npm install -g netlify-cli
netlify deploy
```

**2. Vercel (免費)**
```bash
npm install -g vercel
cd frontend
vercel
```

**3. GitHub Pages (免費)**
```bash
# 1. 將 frontend 資料夾推送到 GitHub
# 2. 在 GitHub repo 設定中啟用 GitHub Pages
# 3. 選擇 branch 和資料夾
```

#### 後端部署 (選一個):

**1. Render (推薦 - 免費)**
```bash
# 1. 在 Render.com 建立新的 Web Service
# 2. 連接 GitHub repo
# 3. 設定:
#    - Build Command: pip install -r requirements.txt
#    - Start Command: python app.py
```

**2. Railway (免費)**
```bash
# 1. 安裝 Railway CLI
npm install -g @railway/cli

# 2. 部署
cd backend
railway login
railway init
railway up
```

**3. Heroku**
```bash
# 1. 建立 Procfile
cd backend
echo "web: python app.py" > Procfile

# 2. 部署
heroku create
git push heroku main
```

### 修改前端配置

部署後，需要修改 `frontend/js/config.js`:

```javascript
const CONFIG = {
    // 修改為你的後端 API URL
    API_BASE_URL: 'https://你的後端URL.com/api',
    // ... 其他配置
};
```

---

## 選項 B: 前端掛載到後端 (簡單)

**將前端整合到 Flask 中，只需要一個伺服器**

### 架構圖

```
┌─────────────────────────────────┐
│  Flask Server                   │
│                                 │
│  ┌──────────┐   ┌──────────┐   │
│  │ Frontend │   │ API      │   │
│  │ (靜態)   │   │ (/api/*) │   │
│  └──────────┘   └──────────┘   │
│                                 │
│  http://localhost:5000          │
└─────────────────────────────────┘
```

### 實現步驟

#### 步驟 1: 使用整合版的 app.py

```bash
cd backend

# 使用整合版
cp app_with_frontend.py app.py

# 或者重命名
mv app.py app_separated.py
mv app_with_frontend.py app.py
```

#### 步驟 2: 修改前端 config.js

```bash
cd ../frontend/js

# 使用整合版配置
cp config_for_integrated.js config.js
```

#### 步驟 3: 啟動伺服器

```bash
cd backend
python app.py
```

**訪問**: `http://localhost:5000`

✅ 現在前端和後端都在同一個伺服器！

### 部署方案

只需要部署一個 Flask 應用:

**Render 部署**:
```bash
# 1. 在 Render.com 建立 Web Service
# 2. 設定:
#    - Build Command: pip install -r requirements.txt
#    - Start Command: python app.py
# 3. 確保 frontend 資料夾在 repo 中
```

**優點**:
- ✅ 只需要一個伺服器
- ✅ 不需要處理 CORS
- ✅ 部署簡單

**缺點**:
- ⚠️ 前後端耦合
- ⚠️ 擴展性較差

---

## 推薦方案

### 開發階段: 分離部署 ✅

**原因**:
- 前後端可以獨立開發
- 熱重載方便
- 符合兩人協作需求

**啟動方式**:
```bash
# 終端 1
cd backend && python app.py

# 終端 2
cd frontend && python -m http.server 8080
```

---

### 提交作業/展示: 整合部署 ✅

**原因**:
- 只需要一個 URL
- 部署簡單
- 不需要擔心 CORS

**啟動方式**:
```bash
# 使用整合版
cd backend
python app_with_frontend.py

# 訪問 http://localhost:5000
```

---

### 生產環境: 分離部署 ✅

**原因**:
- 可以獨立擴展
- 前端可以使用 CDN
- 更專業的架構

**部署方案**:
```
前端 → Netlify (免費)
後端 → Render (免費)
```

---

## 🎯 快速決策表

| 你的需求 | 推薦方案 |
|---------|---------|
| 兩人協作開發 | **分離部署** (當前架構) |
| 快速展示給老師看 | **整合部署** (app_with_frontend.py) |
| 提交作業 | **整合部署** |
| 學習前後端分離 | **分離部署** |
| 部署到線上 | **分離部署** (Netlify + Render) |

---

## ❓ 常見問題

### Q: 我現在應該用哪種方式?

**A**: 開發時用**分離部署**，提交作業時用**整合部署**

---

### Q: 整合部署需要修改什麼?

**A**:
1. 使用 `app_with_frontend.py` 而不是 `app.py`
2. 修改 `config.js` 的 `API_BASE_URL` 為 `/api`
3. 只啟動後端，訪問 `http://localhost:5000`

---

### Q: 如果我想部署到 Heroku?

**A**:
```bash
# 整合部署方式
cd backend
echo "web: python app_with_frontend.py" > Procfile
heroku create
git push heroku main
```

---

### Q: 前端需要 build 嗎?

**A**: 不需要！這是純 HTML/CSS/JS，不需要 build 步驟

---

## 📝 總結

1. **開發時**: 前後端分開啟動 (當前架構)
2. **展示時**: 可以整合到一起 (app_with_frontend.py)
3. **部署時**: 根據需求選擇

**現在的專案已經支援兩種方式！** 🎉
