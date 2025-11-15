# 🔔 价格提醒 (Alerts) 使用指南

## 什么是 Alerts?

**Alerts** 是价格监控提醒系统,可以在股价达到你设定的目标时自动通知你。

---

## 📖 使用场景

### 场景 1: 买入时机
```
当前价格: AAPL $173.79
你想在: $170 以下买入
设置: Price below $170
结果: 当 AAPL 跌到 $170 以下时,系统会触发提醒
```

### 场景 2: 卖出时机
```
当前价格: TSLA $249.84
你想在: $260 以上卖出
设置: Price above $260
结果: 当 TSLA 涨到 $260 以上时,系统会触发提醒
```

### 场景 3: 止损提醒
```
当前价格: NVDA $519.53
止损价格: $500
设置: Price below $500
结果: 当 NVDA 跌破 $500 时,系统会提醒你止损
```

---

## 🎯 如何设置 Alerts

### 步骤 1: 进入股票详情页
1. 登录系统
2. 在 Dashboard 或 Watchlist 点击任意股票
3. 进入 Stock Detail 页面

### 步骤 2: 设置提醒
在 "Set Price Alert" 区域:

1. **选择条件**:
   - `Price above` (价格高于)
   - `Price below` (价格低于)

2. **输入目标价格**:
   - 例如: 180

3. **点击 "Create Alert"**

4. **成功提示**:
   - 会显示 "Alert created successfully!"

### 步骤 3: 查看提醒
- 点击导航栏的 "Alerts"
- 查看所有已设置的提醒

---

## 📊 Alerts 状态说明

| 状态 | 徽章颜色 | 含义 |
|------|---------|------|
| **Active** | 🔵 蓝色 | 正在监控中,等待触发 |
| **Triggered** | 🟢 绿色 | 已触发,价格条件已满足 |
| **Inactive** | ⚫ 灰色 | 已禁用 |

---

## 🔄 测试 Alerts 功能

### 方法 1: 使用股市模拟器 (推荐)

我们创建了一个股市模拟器,可以自动改变股价并触发提醒!

#### 启动模拟器:
```bash
cd backend
python simulate_market.py
```

#### 模拟器功能:
```
1. Single Update        - 更新一次价格
2. Continuous Mode      - 每 5 秒自动更新
3. Fast Mode            - 每 2 秒自动更新
4. Show Current Prices  - 显示当前价格
5. Show Active Alerts   - 显示所有提醒
6. Exit                 - 退出
```

---

## 🎮 完整测试流程

### 第一步: 设置提醒

1. 访问 http://localhost:8080
2. 登录系统
3. 点击任意股票(例如 AAPL)
4. 在股票详情页设置提醒:
   ```
   条件: Price above
   目标价格: 180
   ```
5. 点击 "Create Alert"

再设置一个:
   ```
   条件: Price below
   目标价格: 170
   ```

### 第二步: 查看提醒

1. 点击导航栏 "Alerts"
2. 你会看到刚才设置的 2 个提醒
3. 状态都是 "Active" (蓝色)

### 第三步: 启动模拟器

打开**新的终端窗口**:
```bash
cd backend
python simulate_market.py
```

选择 `2` (Continuous Mode) 或 `3` (Fast Mode)

### 第四步: 观察变化

**模拟器会**:
- 每隔几秒更新股价 (±2% 随机变化)
- 自动检查所有提醒
- 当价格满足条件时触发提醒

**你会看到**:
```
🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔
⚠️  ALERT TRIGGERED for zengevent!
📊 Stock: AAPL (Apple Inc.)
🎯 Condition: Price above $180.00
💰 Current Price: $182.45
🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔

✅ 1 alert(s) triggered!
```

### 第五步: 刷新网页查看

1. 回到浏览器
2. 刷新 Dashboard 页面
3. 你会看到黄色警告框显示触发的提醒!

---

## 💡 实际使用建议

### 设置合理的价格目标

**当前价格**: $173.79

**好的设置** ✅:
- Price above $180 (涨 3.5%)
- Price below $170 (跌 2%)

**不好的设置** ❌:
- Price above $200 (涨 15% - 太高)
- Price below $150 (跌 14% - 太低)

### 多个提醒策略

为同一支股票设置多个提醒:
```
AAPL 当前价格: $173.79

提醒 1: Price above $175  → 小涨,继续持有
提醒 2: Price above $180  → 大涨,考虑卖出
提醒 3: Price below $170  → 小跌,加仓机会
提醒 4: Price below $165  → 大跌,止损
```

---

## 🎯 示例场景

### 场景: 模拟一天的交易

**早上 9:00 - 设置提醒**
```
AAPL: $173.79
设置: Price above $180 (目标卖出价)
设置: Price below $170 (止损价)
```

**上午 10:30 - 启动模拟器**
```bash
python simulate_market.py
选择: 2 (Continuous Mode)
```

**中午 12:00 - 提醒触发**
```
🔔 ALERT! AAPL reached $180.50
Action: 考虑卖出获利
```

**下午 3:00 - 查看结果**
- 在 Alerts 页面看到提醒已触发
- 在 Dashboard 看到黄色通知
- 决定是否执行交易

---

## 📋 Alerts API 说明

### 创建提醒
```
POST /api/alerts
Body:
{
  "user_id": 1,
  "stock_symbol": "AAPL",
  "condition": "above",  // 或 "below"
  "target_price": 180.00
}
```

### 查看提醒
```
GET /api/alerts/{user_id}
```

### 检查触发
```
GET /api/alerts/check/{user_id}
```

### 删除提醒
```
DELETE /api/alerts/{alert_id}
```

---

## 🔧 模拟器命令说明

### 单次更新
```bash
python simulate_market.py
选择: 1
```
- 更新一次所有股价
- 检查一次提醒
- 适合快速测试

### 持续模式 (5秒)
```bash
python simulate_market.py
选择: 2
```
- 每 5 秒更新一次
- 自动循环运行
- 适合长时间观察

### 快速模式 (2秒)
```bash
python simulate_market.py
选择: 3
```
- 每 2 秒更新一次
- 更快看到提醒触发
- 适合演示和测试

### 查看当前价格
```bash
python simulate_market.py
选择: 4
```
- 显示所有股票当前价格
- 显示涨跌幅
- 不修改数据

### 查看活跃提醒
```bash
python simulate_market.py
选择: 5
```
- 显示所有用户的提醒
- 显示当前价格
- 显示提醒状态

---

## ❓ 常见问题

### Q: 提醒会发送邮件或短信吗?
A: 目前只在网页上显示。你可以扩展添加邮件/短信功能。

### Q: 提醒触发后会自动删除吗?
A: 不会。提醒会保持在列表中,状态变为 "Triggered"。

### Q: 可以设置多少个提醒?
A: 没有限制,可以为每支股票设置多个提醒。

### Q: 提醒触发后可以重置吗?
A: 需要删除旧提醒,创建新的提醒。

### Q: 模拟器会影响历史数据吗?
A: 不会,模拟器只更新当前价格,不会修改历史数据。

---

## 🎉 开始使用!

1. **设置一些提醒** (在网页上)
2. **运行模拟器** (在终端)
3. **观察触发** (刷新网页查看)

```bash
cd backend
python simulate_market.py
```

**Enjoy! 🚀**
