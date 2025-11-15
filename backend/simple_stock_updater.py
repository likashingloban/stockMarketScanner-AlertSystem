"""
超简单的股票价格更新器
不需要外部API，使用随机波动模拟真实股价变化
适合演示和学习
"""

import sqlite3
import random
import time
from datetime import datetime

# 初始股票数据（真实的大概价格范围）
INITIAL_STOCKS = [
    {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': 180.0},
    {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'price': 380.0},
    {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': 140.0},
    {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'price': 145.0},
    {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'price': 245.0},
    {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'price': 350.0},
    {'symbol': 'NVDA', 'name': 'NVIDIA Corp.', 'price': 500.0},
    {'symbol': 'JPM', 'name': 'JPMorgan Chase', 'price': 155.0},
    {'symbol': 'V', 'name': 'Visa Inc.', 'price': 250.0},
    {'symbol': 'WMT', 'name': 'Walmart Inc.', 'price': 165.0},
    {'symbol': 'DIS', 'name': 'Walt Disney Co.', 'price': 95.0},
    {'symbol': 'NFLX', 'name': 'Netflix Inc.', 'price': 450.0},
    {'symbol': 'INTC', 'name': 'Intel Corp.', 'price': 45.0},
    {'symbol': 'AMD', 'name': 'AMD Inc.', 'price': 135.0},
    {'symbol': 'CSCO', 'name': 'Cisco Systems', 'price': 52.0},
    {'symbol': 'PFE', 'name': 'Pfizer Inc.', 'price': 30.0},
    {'symbol': 'KO', 'name': 'Coca-Cola Co.', 'price': 60.0},
    {'symbol': 'NKE', 'name': 'Nike Inc.', 'price': 110.0},
    {'symbol': 'BA', 'name': 'Boeing Co.', 'price': 205.0},
    {'symbol': 'GE', 'name': 'General Electric', 'price': 115.0},
]

def init_stocks():
    """初始化股票数据到数据库"""
    conn = sqlite3.connect('stock_app.db')

    for stock in INITIAL_STOCKS:
        conn.execute('''
            INSERT OR REPLACE INTO stock_data
            (stock_symbol, stock_name, current_price, open_price, previous_close,
             high_price, low_price, change_amount, change_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
        ''', (
            stock['symbol'],
            stock['name'],
            stock['price'],
            stock['price'],
            stock['price'],
            stock['price'],
            stock['price']
        ))

    conn.commit()
    conn.close()
    print("✅ 股票数据已初始化")

def update_prices_once():
    """更新一次所有股票价格（随机小幅波动）"""
    conn = sqlite3.connect('stock_app.db')
    conn.row_factory = sqlite3.Row

    # 获取所有股票
    stocks = conn.execute('SELECT * FROM stock_data').fetchall()

    for stock in stocks:
        # 随机波动：-0.5% 到 +0.5%
        change_percent = random.uniform(-0.5, 0.5)
        current_price = stock['current_price']
        new_price = current_price * (1 + change_percent / 100)

        # 计算涨跌
        previous_close = stock['previous_close']
        change_amount = new_price - previous_close
        total_change_percent = (change_amount / previous_close) * 100 if previous_close else 0

        # 更新价格
        conn.execute('''
            UPDATE stock_data
            SET current_price = ?,
                change_amount = ?,
                change_percent = ?,
                updated_at = ?
            WHERE stock_symbol = ?
        ''', (new_price, change_amount, total_change_percent, datetime.now(), stock['stock_symbol']))

    conn.commit()
    conn.close()

def run_continuous_updates(interval=5):
    """持续更新股价（每N秒一次）"""
    print(f"🚀 开始持续更新股价（每 {interval} 秒）")
    print("按 Ctrl+C 停止\n")

    try:
        while True:
            update_prices_once()

            # 显示当前价格
            conn = sqlite3.connect('stock_app.db')
            conn.row_factory = sqlite3.Row
            stocks = conn.execute(
                'SELECT stock_symbol, current_price, change_percent FROM stock_data LIMIT 5'
            ).fetchall()
            conn.close()

            print(f"[{datetime.now().strftime('%H:%M:%S')}]", end=" ")
            for stock in stocks:
                arrow = '📈' if stock['change_percent'] >= 0 else '📉'
                print(f"{stock['stock_symbol']} ${stock['current_price']:.2f} {arrow}", end="  ")
            print()

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n⏹️  已停止更新")

if __name__ == '__main__':
    import sys

    print("=" * 60)
    print("📊 简单股票价格更新器")
    print("=" * 60)
    print("\n选择操作：")
    print("1. 初始化股票数据")
    print("2. 更新一次")
    print("3. 持续更新（每5秒）")
    print("4. 持续更新（每10秒）")
    print()

    choice = input("请选择 (1/2/3/4): ").strip()

    if choice == '1':
        init_stocks()
    elif choice == '2':
        update_prices_once()
        print("✅ 价格已更新")
    elif choice == '3':
        run_continuous_updates(5)
    elif choice == '4':
        run_continuous_updates(10)
    else:
        print("❌ 无效选择")
