"""
資料庫初始化腳本
執行此腳本建立所有資料表
"""

import sqlite3

def init_database():
    """初始化資料庫,建立所有資料表"""
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()

    print("📦 開始建立資料表...")

    # 1. 用戶表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ users 表已建立")

    # 2. 觀察清單表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stock_symbol VARCHAR(10) NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, stock_symbol)
        )
    ''')
    print("✓ watchlist 表已建立")

    # 3. 股票數據表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_symbol VARCHAR(10) UNIQUE NOT NULL,
            stock_name VARCHAR(100),
            current_price DECIMAL(10, 2),
            open_price DECIMAL(10, 2),
            previous_close DECIMAL(10, 2),
            high_price DECIMAL(10, 2),
            low_price DECIMAL(10, 2),
            change_amount DECIMAL(10, 2),
            change_percent DECIMAL(5, 2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ stock_data 表已建立")

    # 4. 歷史數據表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            close_price DECIMAL(10, 2) NOT NULL,
            volume INTEGER,
            UNIQUE(stock_symbol, date)
        )
    ''')
    print("✓ stock_history 表已建立")

    # 5. 提醒表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stock_symbol VARCHAR(10) NOT NULL,
            condition VARCHAR(10) NOT NULL,
            target_price DECIMAL(10, 2) NOT NULL,
            is_triggered BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            triggered_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    print("✓ alerts 表已建立")

    # 6. 模拟原始数据表（存储1小时的完整模拟数据）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulation_source_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_symbol VARCHAR(10) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            volume INTEGER,
            timestamp INTEGER NOT NULL,
            UNIQUE(stock_symbol, timestamp)
        )
    ''')
    print("✓ simulation_source_data 表已建立")

    # 7. 模拟状态表（记录模拟进度和状态）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulation_status (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            is_running BOOLEAN DEFAULT 0,
            current_timestamp INTEGER DEFAULT 0,
            start_time TIMESTAMP,
            total_seconds INTEGER DEFAULT 3600,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ simulation_status 表已建立")

    # 插入默认的模拟状态记录
    cursor.execute('''
        INSERT OR IGNORE INTO simulation_status (id, is_running, current_timestamp)
        VALUES (1, 0, 0)
    ''')

    conn.commit()
    conn.close()

    print("\n✅ 資料庫初始化完成!")
    print("📂 資料庫檔案: stock_app.db")


if __name__ == "__main__":
    init_database()
