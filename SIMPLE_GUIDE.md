# 📈 股票监控系统 - 简单使用指南

## 🚀 快速启动（2步骤）

### 步骤 1: 启动后端

```bash
cd backend
python app.py
```

看到以下信息表示成功：
```
🚀 Flask API Server starting...
📍 API endpoint: http://localhost:5001
📊 自动股价更新已启动（每5秒更新一次）
✅ 自动股价更新线程已启动
```

**保持此窗口运行！股价会自动每5秒更新一次！** ✨

---

### 步骤 2: 启动前端

**打开新的终端窗口**：

```bash
cd frontend
python -m http.server 8080
```

然后打开浏览器访问：
```
http://localhost:8080
```

---

## 📊 初始化股票数据（首次使用）

**首次使用时需要初始化20只股票的数据**：

```bash
cd backend
python simple_stock_updater.py
# 输入 1 回车
```

这会初始化20只热门股票的数据。

**注意**：初始化后，当你运行 `python app.py` 时，股价会自动每5秒更新，**不需要再手动运行更新脚本**！

---

## 💡 使用流程

1. **注册账户**
   - 访问 http://localhost:8080
   - 点击 "Register now"
   - 填写信息并注册

2. **登录系统**
   - 使用注册的账户登录

3. **添加股票到观察清单**
   - 点击 "Watchlist"
   - 输入股票代码（AAPL, MSFT, GOOGL, TSLA, META等）
   - 点击 "新增股票"

4. **查看实时数据**
   - 在 Watchlist 页面查看价格变化
   - 价格每 5 秒自动刷新（后台自动更新）

5. **设置价格提醒**
   - 点击股票的 "详情"
   - 设置提醒条件（价格高于/低于某个值）
   - 触发时会自动通知

---

## 📋 可用的股票代码

系统预设了20只热门股票：

| 代码 | 公司名称 | 代码 | 公司名称 |
|------|----------|------|----------|
| AAPL | Apple Inc. | DIS | Walt Disney Co. |
| MSFT | Microsoft Corp. | NFLX | Netflix Inc. |
| GOOGL | Alphabet Inc. | INTC | Intel Corp. |
| AMZN | Amazon.com Inc. | AMD | AMD Inc. |
| TSLA | Tesla Inc. | CSCO | Cisco Systems |
| META | Meta Platforms Inc. | PFE | Pfizer Inc. |
| NVDA | NVIDIA Corp. | KO | Coca-Cola Co. |
| JPM | JPMorgan Chase | NKE | Nike Inc. |
| V | Visa Inc. | BA | Boeing Co. |
| WMT | Walmart Inc. | GE | General Electric |

---

## 🔧 常见问题

### Q: 为什么看不到股价数据？

**A**: 首次使用需要初始化股票数据：
```bash
cd backend
python simple_stock_updater.py  # 选择 1（初始化）
```
初始化后，运行 `python app.py` 即可自动更新价格。

### Q: 价格多久更新一次？

**A**: 每 5 秒自动更新一次（在 app.py:388 可修改 `time.sleep(5)` 的值）

### Q: 如何停止价格更新？

**A**: 在运行 `python app.py` 的终端按 `Ctrl+C` 停止后端服务即可

### Q: 可以添加更多股票吗？

**A**: 可以！编辑 `backend/simple_stock_updater.py` 文件中的 `INITIAL_STOCKS` 列表，然后重新运行初始化

---

## 📁 项目结构

```
├── backend/
│   ├── app.py                      # API 服务器
│   ├── database.py                 # 数据库初始化
│   ├── simple_stock_updater.py     # 股价更新器 ⭐
│   └── stock_app.db                # SQLite 数据库
│
├── frontend/
│   ├── index.html                  # 登录页
│   ├── dashboard.html              # 仪表板
│   ├── watchlist.html              # 观察清单
│   ├── alerts.html                 # 提醒管理
│   └── js/
│       └── config.js               # API 配置
│
└── SIMPLE_GUIDE.md                 # 本文件
```

---

## 🎯 核心功能

✅ **用户认证** - 注册、登录、密码管理
✅ **观察清单** - 添加、删除股票
✅ **实时价格** - 每5秒自动更新
✅ **价格提醒** - 设置条件，自动通知
✅ **数据可视化** - 价格趋势图表

---

## 💻 技术栈

- **后端**: Python + Flask
- **前端**: HTML + JavaScript + Bootstrap 5
- **数据库**: SQLite
- **价格更新**: 简单随机波动模拟

---

## 🎉 就这么简单！

只需两个终端窗口：
1. 后端 API (`python app.py`) - 自动更新股价！
2. 前端服务器 (`python -m http.server 8080`)

然后打开浏览器享受吧！🚀

---

## ⚙️ 技术细节

**自动价格更新机制**：
- 后端 app.py 启动时会自动创建一个后台守护线程 (app.py:396)
- 该线程每5秒调用一次 `auto_update_prices()` 函数 (app.py:349-388)
- 使用随机波动算法（-0.5% 到 +0.5%）模拟真实股价变化
- 无需手动运行更新脚本，完全自动化！
