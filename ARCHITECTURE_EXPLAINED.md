# 🏗️ 系统架构说明

## ✅ 正确的设计 (当前实现)

### 核心概念

```
平台 (Platform)
├── 股票池 (Stock Pool)
│   ├── AAPL - Apple Inc.
│   ├── MSFT - Microsoft Corp.
│   ├── GOOGL - Alphabet Inc.
│   └── ... (10支股票)
│
└── 用户 (Users)
    ├── User A
    │   └── Watchlist (观察清单)
    │       ├── → AAPL (引用)
    │       └── → TSLA (引用)
    │
    └── User B
        └── Watchlist (观察清单)
            ├── → AAPL (引用,和 User A 共享数据)
            └── → NVDA (引用)
```

---

## 📊 数据关系

### 1. Platform Stock Data (平台股票数据)

**表**: `stock_data`

| stock_symbol | stock_name | current_price | ... |
|--------------|------------|---------------|-----|
| AAPL | Apple Inc. | $173.79 | ... |
| MSFT | Microsoft Corp. | $380.00 | ... |
| GOOGL | Alphabet Inc. | $136.79 | ... |

**特点**:
- ✅ 平台拥有,所有用户共享
- ✅ 只存储一份数据
- ✅ 实时更新,所有用户同步看到
- ✅ 不属于任何特定用户

---

### 2. User Watchlist (用户观察清单)

**表**: `watchlist`

| id | user_id | stock_symbol |
|----|---------|--------------|
| 1 | 1 | AAPL |
| 2 | 1 | TSLA |
| 3 | 2 | AAPL |
| 4 | 2 | NVDA |

**特点**:
- ✅ 用户选择关注的股票
- ✅ 只存储引用 (user_id + stock_symbol)
- ✅ 不存储实际股价数据
- ✅ 多个用户可以关注同一支股票

---

## 🔄 工作流程

### 场景 1: 用户添加股票到 Watchlist

```
1. 用户 A 在 Watchlist 页面输入 "AAPL"
2. 点击 "Add Stock" 按钮
3. 系统检查:
   ✅ AAPL 存在于 stock_data (平台股票池)
   ✅ 用户 A 还没有添加过 AAPL
4. 系统在 watchlist 表插入一条记录:
   (user_id=1, stock_symbol='AAPL')
5. 用户 A 的 Watchlist 现在显示 AAPL 的实时价格
```

### 场景 2: 查看 Watchlist

```
用户 A 打开 Watchlist 页面
↓
前端调用: GET /api/watchlist/1
↓
后端执行 SQL:
SELECT w.stock_symbol, s.stock_name, s.current_price, s.change_percent
FROM watchlist w
LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
WHERE w.user_id = 1
↓
返回: 用户 A 关注的股票 + 平台的实时价格数据
```

### 场景 3: 多个用户关注同一股票

```
User A Watchlist: AAPL, TSLA
User B Watchlist: AAPL, NVDA

Platform stock_data:
AAPL: $173.79 (只有一份数据)
TSLA: $249.84
NVDA: $519.53

当 AAPL 价格变化:
- 系统只更新 stock_data 表中的一条记录
- User A 和 User B 都能看到更新后的价格
```

---

## 💾 数据库表结构

### stock_data (平台股票池)
```sql
CREATE TABLE stock_data (
    stock_symbol TEXT PRIMARY KEY,    -- 股票代码
    stock_name TEXT,                   -- 公司名称
    current_price REAL,                -- 当前价格
    previous_close REAL,               -- 前收盘价
    open_price REAL,                   -- 开盘价
    high_price REAL,                   -- 最高价
    low_price REAL,                    -- 最低价
    volume INTEGER,                    -- 成交量
    change_amount REAL,                -- 涨跌金额
    change_percent REAL,               -- 涨跌百分比
    updated_at DATETIME                -- 更新时间
);
```

**数据示例**:
```
AAPL | Apple Inc. | 173.79 | 175.00 | ... | 2025-11-14 23:03:48
MSFT | Microsoft  | 380.00 | 380.00 | ... | 2025-11-14 23:03:48
```

### watchlist (用户观察清单)
```sql
CREATE TABLE watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,                   -- 用户ID
    stock_symbol TEXT,                 -- 股票代码 (引用)
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, stock_symbol),    -- 同一用户不能重复添加
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_symbol) REFERENCES stock_data(stock_symbol)
);
```

**数据示例**:
```
1 | 1 | AAPL | 2025-11-14 22:00:00    (User zengevent 关注 AAPL)
2 | 1 | TSLA | 2025-11-14 22:05:00    (User zengevent 关注 TSLA)
3 | 2 | AAPL | 2025-11-14 22:10:00    (User testuser 关注 AAPL)
```

---

## 🎯 优势

### ✅ 数据一致性
- 所有用户看到的是同一份数据
- 价格更新一次,全平台生效

### ✅ 节省存储空间
- 不需要为每个用户复制股票数据
- Watchlist 只存储轻量级的引用

### ✅ 易于管理
- 添加新股票:只需在 stock_data 添加一次
- 更新价格:只需更新 stock_data
- 所有用户自动获得更新

### ✅ 灵活性
- 用户可以自由添加/删除观察的股票
- 不影响平台的股票池
- 多个用户可以关注同一股票

---

## 🔄 API 工作方式

### 1. 获取用户的 Watchlist
```
GET /api/watchlist/{user_id}

SQL:
SELECT w.id, w.stock_symbol,
       s.stock_name, s.current_price, s.change_percent
FROM watchlist w
LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
WHERE w.user_id = ?

返回:
[
  {
    "id": 1,
    "stock_symbol": "AAPL",
    "stock_name": "Apple Inc.",
    "current_price": 173.79,
    "change_percent": -0.69
  },
  ...
]
```

### 2. 添加股票到 Watchlist
```
POST /api/watchlist
Body: {
  "user_id": 1,
  "stock_symbol": "AAPL"
}

步骤:
1. 检查 AAPL 是否存在于 stock_data ✅
2. 检查用户是否已添加 AAPL ✅
3. 在 watchlist 插入: (user_id=1, stock_symbol='AAPL')
4. 返回成功

注意: 不需要创建股票数据,只创建引用!
```

### 3. 删除 Watchlist 中的股票
```
DELETE /api/watchlist/{watchlist_id}

步骤:
1. 从 watchlist 表删除记录
2. stock_data 中的数据保持不变 (其他用户可能还在用)
```

---

## 📝 实际例子

### 初始状态

**Platform Stock Pool**:
```
AAPL - $173.79
MSFT - $380.00
GOOGL - $136.79
TSLA - $249.84
NVDA - $519.53
```

**User zengevent Watchlist**: (空)
**User testuser Watchlist**: (空)

---

### Step 1: zengevent 添加 AAPL

```
zengevent 操作: 在 Watchlist 页面输入 "AAPL" → Add Stock

数据库变化:
watchlist 表:
  +1 | 1 | AAPL | 2025-11-14 23:00:00

zengevent 的 Watchlist 显示:
  AAPL - Apple Inc. - $173.79 (-0.69%)
```

---

### Step 2: testuser 也添加 AAPL

```
testuser 操作: 在 Watchlist 页面输入 "AAPL" → Add Stock

数据库变化:
watchlist 表:
  +1 | 1 | AAPL | 2025-11-14 23:00:00
  +2 | 2 | AAPL | 2025-11-14 23:05:00

testuser 的 Watchlist 显示:
  AAPL - Apple Inc. - $173.79 (-0.69%)

注意: 两个用户看到的是同一份数据!
```

---

### Step 3: AAPL 价格更新

```
模拟器运行: python simulate_market.py

数据库变化:
stock_data 表:
  AAPL | Apple Inc. | 175.50 | ... (更新)

结果:
- zengevent 看到: AAPL - $175.50 (+1.0%)
- testuser 看到: AAPL - $175.50 (+1.0%)
- 两个用户同时看到更新!
```

---

### Step 4: zengevent 删除 AAPL

```
zengevent 操作: 在 Watchlist 点击 Delete

数据库变化:
watchlist 表:
  -1 | 1 | AAPL | ... (删除)
   2 | 2 | AAPL | ... (保留)

stock_data 表:
  AAPL | Apple Inc. | 175.50 | ... (不变!)

结果:
- zengevent 的 Watchlist: (空)
- testuser 的 Watchlist: 仍然显示 AAPL
- AAPL 数据在平台上继续存在
```

---

## 🎯 总结

### 当前架构特点

1. **Platform-Owned Stocks** (平台拥有股票)
   - stock_data 表存储所有股票数据
   - 所有用户共享同一份数据

2. **User-Specific Watchlist** (用户个性化观察清单)
   - watchlist 表只存储引用
   - 每个用户选择自己关注的股票

3. **Efficient & Scalable** (高效可扩展)
   - 数据不重复
   - 更新一次,全平台生效
   - 添加新用户不需要复制股票数据

### 这正是你想要的架构! ✅

```
✅ 股票数据不属于某个用户
✅ 股票数据是平台的
✅ 用户只是选择关注哪些股票
✅ 可以自由添加/删除
✅ 多个用户可以关注同一股票
```

---

## 🚀 当前状态

- **Platform Stocks**: 10 支股票 ✅
- **User zengevent**: 10 支股票在 watchlist ✅
- **User testuser**: 10 支股票在 watchlist ✅
- **Architecture**: 完全正确 ✅

**你可以在网页上自由添加/删除股票,不会影响平台的股票池!**
