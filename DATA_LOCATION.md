# 📊 Stock Data Location Guide

## 数据存储位置

所有股票数据都存储在 SQLite 数据库中:

```
backend/stock_app.db
```

**完整路径:**
```
/Users/ruler/Documents/partTime/Short-term/stockMarketScanner&AlertSystem/backend/stock_app.db
```

**文件大小:** 108 KB

---

## 数据库结构

### 1. stock_data 表 (当前股票数据)

存储每支股票的最新价格信息:

| 字段 | 类型 | 说明 |
|------|------|------|
| stock_symbol | TEXT | 股票代码 (如 AAPL) |
| stock_name | TEXT | 公司名称 (如 Apple Inc.) |
| current_price | REAL | 当前价格 |
| previous_close | REAL | 前收盘价 |
| open_price | REAL | 开盘价 |
| high_price | REAL | 最高价 |
| low_price | REAL | 最低价 |
| volume | INTEGER | 成交量 |
| change_amount | REAL | 涨跌金额 |
| change_percent | REAL | 涨跌百分比 |
| updated_at | DATETIME | 更新时间 |

**当前数据 (10 支股票):**
```
AAPL   | Apple Inc.                      | $173.79 | -0.69%
AMD    | Advanced Micro Devices Inc.     | $144.23 | +3.02%
AMZN   | Amazon.com Inc.                 | $137.75 | -5.00%
DIS    | The Walt Disney Company         | $93.71  | -1.36%
GOOGL  | Alphabet Inc.                   | $136.79 | -2.29%
META   | Meta Platforms Inc.             | $346.86 | -0.90%
MSFT   | Microsoft Corporation           | $379.99 | -0.00%
NFLX   | Netflix Inc.                    | $465.65 | +3.48%
NVDA   | NVIDIA Corporation              | $519.53 | +4.95%
TSLA   | Tesla Inc.                      | $249.84 | +1.97%
```

### 2. stock_history 表 (历史数据)

存储每支股票的历史价格数据,用于图表显示:

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| stock_symbol | TEXT | 股票代码 |
| date | TEXT | 日期 (YYYY-MM-DD) |
| close_price | REAL | 收盘价 |
| volume | INTEGER | 成交量 |

**历史数据统计:**
```
每支股票: 90 天历史数据
总记录数: 900 条 (10 stocks × 90 days)
日期范围: 2025-08-16 至 2025-11-13
```

### 3. 其他表

- **users** - 用户账户信息
- **watchlist** - 用户观察清单
- **alerts** - 价格提醒设置

---

## 如何查看数据

### 方法 1: 使用 SQLite 命令行

```bash
# 进入数据库目录
cd backend

# 打开数据库
sqlite3 stock_app.db

# 查看所有股票
SELECT stock_symbol, stock_name, current_price, change_percent
FROM stock_data
ORDER BY stock_symbol;

# 查看某支股票的历史数据
SELECT date, close_price
FROM stock_history
WHERE stock_symbol = 'AAPL'
ORDER BY date DESC
LIMIT 10;

# 退出
.quit
```

### 方法 2: 使用 Python

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect('backend/stock_app.db')
cursor = conn.cursor()

# 查询所有股票
cursor.execute("SELECT * FROM stock_data")
stocks = cursor.fetchall()

for stock in stocks:
    print(stock)

conn.close()
```

### 方法 3: 使用数据库可视化工具

推荐工具:
- **DB Browser for SQLite** (免费) - https://sqlitebrowser.org/
- **TablePlus** (付费/免费版) - https://tableplus.com/
- **DBeaver** (免费) - https://dbeaver.io/

---

## 数据导出

### 导出为 CSV

```bash
cd backend

# 导出股票数据
sqlite3 stock_app.db <<EOF
.headers on
.mode csv
.output stock_data.csv
SELECT * FROM stock_data;
.quit
EOF

# 导出历史数据
sqlite3 stock_app.db <<EOF
.headers on
.mode csv
.output stock_history.csv
SELECT * FROM stock_history;
.quit
EOF
```

### 导出为 JSON

创建 Python 脚本 `export_data.py`:

```python
import sqlite3
import json

conn = sqlite3.connect('stock_app.db')
conn.row_factory = sqlite3.Row

# 导出股票数据
cursor = conn.cursor()
cursor.execute("SELECT * FROM stock_data")
stocks = [dict(row) for row in cursor.fetchall()]

with open('stock_data.json', 'w') as f:
    json.dump(stocks, f, indent=2)

print("✅ Data exported to stock_data.json")
conn.close()
```

---

## 数据备份

### 备份数据库

```bash
# 创建备份
cp backend/stock_app.db backend/stock_app_backup_$(date +%Y%m%d).db

# 或使用 SQLite 命令
sqlite3 backend/stock_app.db ".backup backend/stock_app_backup.db"
```

### 恢复数据库

```bash
# 恢复备份
cp backend/stock_app_backup.db backend/stock_app.db
```

---

## 重新生成数据

如果需要重新生成数据:

```bash
cd backend

# 方法 1: 使用模拟数据 (推荐)
python fetch_stock_data.py
# 选择 1 (Mock data)

# 方法 2: 尝试下载真实数据 (可能会遇到速率限制)
python download_batch_data.py
```

---

## 数据文件位置总结

```
stockMarketScanner&AlertSystem/
└── backend/
    ├── stock_app.db           # 主数据库文件 (108 KB)
    │                          # 包含所有表和数据
    │
    ├── fetch_stock_data.py    # 数据生成脚本
    ├── download_batch_data.py # 真实数据下载脚本 (备用)
    └── test_api.py            # API 测试和添加股票
```

---

## 数据更新频率

- **当前数据**: 每次运行 `fetch_stock_data.py` 时更新
- **历史数据**: 每次运行时完全重新生成 90 天数据
- **建议**: 根据需要手动更新,或设置定时任务

---

## 常见问题

### Q: 数据是真实的吗?
A: 当前使用的是模拟数据,基于真实价格范围生成。如果需要真实数据,可以尝试运行 `download_batch_data.py`,但 Yahoo Finance API 有速率限制。

### Q: 如何添加更多股票?
A:
1. 在前端 Watchlist 页面添加股票代码
2. 运行 `python fetch_stock_data.py` 生成数据

### Q: 如何修改历史数据天数?
A: 编辑 `fetch_stock_data.py`,修改 `generate_history()` 函数的 `days` 参数 (默认 90)

### Q: 数据库文件可以删除吗?
A: 可以,删除后运行 `python database.py` 重新初始化数据库。

---

**最后更新**: 2025-11-14 23:03
**数据库大小**: 108 KB
**总股票数**: 10
**总历史记录**: 900 条
