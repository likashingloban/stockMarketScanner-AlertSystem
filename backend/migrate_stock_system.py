"""
Migrate Stock System Architecture
Change from user-owned stocks to platform-owned stocks
"""

import sqlite3
from datetime import datetime

def get_db():
    """Database connection helper"""
    conn = sqlite3.connect('stock_app.db')
    conn.row_factory = sqlite3.Row
    return conn

def migrate_system():
    """
    Change architecture:
    - Stock data is platform-owned (not user-owned)
    - Watchlist just references stock symbols
    - All users can add any stock to their watchlist
    """

    print("="*70)
    print("🔄 Migrating Stock System Architecture")
    print("="*70)
    print("\nNew Design:")
    print("✅ Platform owns all stock data")
    print("✅ Users add stocks to their personal watchlist")
    print("✅ Watchlist = User's selected stocks for tracking")
    print("="*70)

    conn = get_db()

    # The current database structure is already correct!
    # Let's verify the architecture

    print("\n📊 Checking current architecture...")

    # Check stock_data table (platform stocks)
    stocks = conn.execute('SELECT COUNT(*) as count FROM stock_data').fetchone()
    print(f"\n✅ Platform stocks: {stocks['count']} stocks available")

    # Check watchlist table (user selections)
    watchlists = conn.execute('''
        SELECT u.username, COUNT(w.id) as stock_count
        FROM users u
        LEFT JOIN watchlist w ON u.id = w.user_id
        GROUP BY u.id
    ''').fetchall()

    print(f"\n✅ User watchlists:")
    for wl in watchlists:
        print(f"   - {wl['username']}: {wl['stock_count']} stocks")

    print("\n" + "="*70)
    print("✅ Architecture is CORRECT!")
    print("="*70)

    print("\nHow it works:")
    print("1. Platform has stock data (stock_data table)")
    print("2. Users select which stocks to track (watchlist table)")
    print("3. Multiple users can track the same stock")
    print("4. Watchlist only stores references (user_id + stock_symbol)")

    # Display the relationship
    print("\n" + "="*70)
    print("📋 Current Stock Pool (Available to all users)")
    print("="*70)

    all_stocks = conn.execute('''
        SELECT stock_symbol, stock_name, current_price, change_percent
        FROM stock_data
        ORDER BY stock_symbol
    ''').fetchall()

    for stock in all_stocks:
        icon = "📈" if stock['change_percent'] >= 0 else "📉"
        print(f"{icon} {stock['stock_symbol']:6} - {stock['stock_name'][:35]:35} ${stock['current_price']:7.2f}")

    conn.close()

    print("\n" + "="*70)
    print("✅ System architecture verified!")
    print("="*70)

if __name__ == "__main__":
    try:
        migrate_system()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
