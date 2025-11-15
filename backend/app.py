"""
Stock Watch & Alert Web App - Backend API
Flask RESTful API Server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import secrets
import threading
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

CORS(app, supports_credentials=True)

def get_db():
    """Database connection helper"""
    conn = sqlite3.connect('stock_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== Authentication API ====================

@app.route('/api/auth/change-password', methods=['POST'])
def change_password():
    """Change user password"""
    data = request.get_json()
    user_id = data.get('user_id')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not user_id or not old_password or not new_password:
        return jsonify({'error': 'All fields are required'}), 400

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404

    from werkzeug.security import check_password_hash, generate_password_hash

    # Verify old password
    if not check_password_hash(user['password_hash'], old_password):
        conn.close()
        return jsonify({'error': 'Current password is incorrect'}), 401

    # Update password
    new_password_hash = generate_password_hash(new_password)
    conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_password_hash, user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Password changed successfully'}), 200


@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    from werkzeug.security import generate_password_hash
    password_hash = generate_password_hash(password)

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        return jsonify({'message': 'Registration successful', 'username': username}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 400
    finally:
        conn.close()


@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 401

    from werkzeug.security import check_password_hash
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid password'}), 401

    token = secrets.token_urlsafe(32)

    return jsonify({
        'message': 'Login successful',
        'user': {'id': user['id'], 'username': user['username'], 'email': user['email']},
        'token': token
    }), 200


# ==================== Watchlist API ====================

@app.route('/api/watchlist/<int:user_id>', methods=['GET'])
def get_watchlist(user_id):
    """Get user's watchlist"""
    conn = get_db()
    stocks = conn.execute('''
        SELECT w.id, w.stock_symbol, s.stock_name, s.current_price,
               s.change_amount, s.change_percent, s.updated_at
        FROM watchlist w
        LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
        WHERE w.user_id = ?
        ORDER BY w.added_at DESC
    ''', (user_id,)).fetchall()
    conn.close()

    return jsonify([dict(row) for row in stocks]), 200


@app.route('/api/watchlist', methods=['POST'])
def add_to_watchlist():
    """Add stock to watchlist"""
    data = request.get_json()
    user_id = data.get('user_id')
    stock_symbol = data.get('stock_symbol', '').upper()

    if not user_id or not stock_symbol:
        return jsonify({'error': 'Missing required parameters'}), 400

    conn = get_db()
    try:
        conn.execute('INSERT INTO watchlist (user_id, stock_symbol) VALUES (?, ?)',
                    (user_id, stock_symbol))
        conn.commit()
        return jsonify({'message': f'{stock_symbol} added to watchlist'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Stock already in watchlist'}), 400
    finally:
        conn.close()


@app.route('/api/watchlist/<int:watchlist_id>', methods=['DELETE'])
def remove_from_watchlist(watchlist_id):
    """Remove stock from watchlist"""
    conn = get_db()
    conn.execute('DELETE FROM watchlist WHERE id = ?', (watchlist_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Removed'}), 200


# ==================== Stock Data API ====================

@app.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    """Get all available stocks"""
    conn = get_db()
    stocks = conn.execute('''
        SELECT stock_symbol, stock_name, current_price,
               change_amount, change_percent, updated_at
        FROM stock_data
        ORDER BY stock_symbol ASC
    ''').fetchall()
    conn.close()

    return jsonify([dict(row) for row in stocks]), 200


@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_detail(symbol):
    """Get stock details"""
    conn = get_db()
    stock = conn.execute('SELECT * FROM stock_data WHERE stock_symbol = ?',
                        (symbol.upper(),)).fetchone()

    if not stock:
        conn.close()
        return jsonify({'error': 'Stock not found'}), 404

    return jsonify(dict(stock)), 200


@app.route('/api/stock/<symbol>/history', methods=['GET'])
def get_stock_history(symbol):
    """Get stock history for charts - 支持不同时间范围"""
    from datetime import timedelta

    # 获取参数：range 可以是 '1h', '24h', '7d'
    time_range = request.args.get('range', '1h', type=str)

    conn = get_db()
    symbol = symbol.upper()

    if time_range == '1h':
        # 1小时：10秒级数据
        cutoff_time = datetime.now() - timedelta(hours=1)
        history = conn.execute('''
            SELECT strftime('%H:%M:%S', timestamp) as time, price, volume
            FROM stock_history_second
            WHERE stock_symbol = ? AND timestamp >= ?
            ORDER BY timestamp ASC
        ''', (symbol, cutoff_time)).fetchall()

    elif time_range == '24h':
        # 24小时：按分钟聚合（从10秒数据聚合）
        cutoff_time = datetime.now() - timedelta(hours=24)
        history = conn.execute('''
            SELECT strftime('%H:%M', timestamp) as time,
                   AVG(price) as price,
                   SUM(volume) as volume
            FROM stock_history_second
            WHERE stock_symbol = ? AND timestamp >= ?
            GROUP BY strftime('%Y-%m-%d %H:%M', timestamp)
            ORDER BY time ASC
        ''', (symbol, cutoff_time)).fetchall()

    elif time_range == '7d':
        # 7天：小时级聚合（从10秒数据聚合）
        cutoff_time = datetime.now() - timedelta(days=7)
        history = conn.execute('''
            SELECT strftime('%m-%d %H:00', timestamp) as time,
                   AVG(price) as price,
                   SUM(volume) as volume
            FROM stock_history_second
            WHERE stock_symbol = ? AND timestamp >= ?
            GROUP BY strftime('%Y-%m-%d %H', timestamp)
            ORDER BY time ASC
        ''', (symbol, cutoff_time)).fetchall()
    else:
        conn.close()
        return jsonify({'error': 'Invalid range parameter'}), 400

    conn.close()

    result = [dict(row) for row in history]
    return jsonify(result), 200


# ==================== Alerts API ====================

@app.route('/api/alerts/<int:user_id>', methods=['GET'])
def get_alerts(user_id):
    """Get user's alerts"""
    conn = get_db()
    alerts = conn.execute('''
        SELECT a.*, s.stock_name, s.current_price
        FROM alerts a
        LEFT JOIN stock_data s ON a.stock_symbol = s.stock_symbol
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
    ''', (user_id,)).fetchall()
    conn.close()

    return jsonify([dict(row) for row in alerts]), 200


@app.route('/api/alerts', methods=['POST'])
def add_alert():
    """Create price alert"""
    data = request.get_json()
    user_id = data.get('user_id')
    stock_symbol = data.get('stock_symbol', '').upper()
    condition = data.get('condition')
    target_price = data.get('target_price')

    if not all([user_id, stock_symbol, condition, target_price]):
        return jsonify({'error': 'Missing required parameters'}), 400

    if condition not in ['above', 'below']:
        return jsonify({'error': 'Condition must be "above" or "below"'}), 400

    conn = get_db()
    conn.execute(
        'INSERT INTO alerts (user_id, stock_symbol, condition, target_price) VALUES (?, ?, ?, ?)',
        (user_id, stock_symbol, condition, target_price)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Alert created'}), 201


@app.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete alert"""
    conn = get_db()
    conn.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Alert deleted'}), 200


@app.route('/api/alerts/check/<int:user_id>', methods=['GET'])
def check_alerts(user_id):
    """Check for triggered alerts"""
    conn = get_db()

    alerts = conn.execute('''
        SELECT a.id, a.stock_symbol, a.condition, a.target_price,
               s.stock_name, s.current_price
        FROM alerts a
        JOIN stock_data s ON a.stock_symbol = s.stock_symbol
        WHERE a.user_id = ? AND a.is_active = 1 AND a.is_triggered = 0
    ''', (user_id,)).fetchall()

    triggered = []

    for alert in alerts:
        alert_dict = dict(alert)
        current_price = alert_dict['current_price']
        target_price = alert_dict['target_price']
        condition = alert_dict['condition']

        # Check if triggered
        if (condition == 'above' and current_price >= target_price) or \
           (condition == 'below' and current_price <= target_price):

            conn.execute(
                'UPDATE alerts SET is_triggered = 1, triggered_at = ? WHERE id = ?',
                (datetime.now(), alert_dict['id'])
            )

            triggered.append({
                'stock_symbol': alert_dict['stock_symbol'],
                'stock_name': alert_dict['stock_name'],
                'condition': condition,
                'target_price': target_price,
                'current_price': current_price
            })

    conn.commit()
    conn.close()

    return jsonify(triggered), 200


# ==================== Dashboard API ====================

@app.route('/api/dashboard/<int:user_id>', methods=['GET'])
def get_dashboard_data(user_id):
    """Get dashboard overview data"""
    conn = get_db()

    # Top 5 stocks
    top_stocks = conn.execute('''
        SELECT w.stock_symbol, s.stock_name, s.current_price, s.change_percent
        FROM watchlist w
        LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
        WHERE w.user_id = ?
        ORDER BY w.added_at DESC
        LIMIT 5
    ''', (user_id,)).fetchall()

    # Active alerts count
    alert_count = conn.execute('''
        SELECT COUNT(*) as count
        FROM alerts
        WHERE user_id = ? AND is_active = 1 AND is_triggered = 0
    ''', (user_id,)).fetchone()

    conn.close()

    return jsonify({
        'top_stocks': [dict(row) for row in top_stocks],
        'active_alerts_count': alert_count['count']
    }), 200


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Stock Watch API is running',
        'timestamp': datetime.now().isoformat()
    }), 200


# ==================== Auto Stock Price Updater ====================

def auto_update_prices():
    """后台线程：自动更新股价（每5秒）"""
    print("📊 自动股价更新已启动（每5秒更新一次）")

    while True:
        try:
            conn = get_db()
            current_time = datetime.now()
            current_date = current_time.date()

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

                # 更新实时价格
                conn.execute('''
                    UPDATE stock_data
                    SET current_price = ?,
                        change_amount = ?,
                        change_percent = ?,
                        updated_at = ?
                    WHERE stock_symbol = ?
                ''', (new_price, change_amount, total_change_percent, current_time, stock['stock_symbol']))

                # 更新或插入当天的历史数据（每天一条记录，用于7天图表）
                conn.execute('''
                    INSERT INTO stock_history (stock_symbol, date, close_price, volume)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(stock_symbol, date)
                    DO UPDATE SET close_price = ?, volume = ?
                ''', (stock['stock_symbol'], current_date, new_price, random.randint(1000000, 10000000),
                      new_price, random.randint(1000000, 10000000)))

                # 插入秒级历史数据（用于1小时和24小时图表）
                # 截断到10秒级别（更平滑的曲线）
                current_10s = current_time.replace(second=(current_time.second // 10) * 10, microsecond=0)
                conn.execute('''
                    INSERT INTO stock_history_second (stock_symbol, timestamp, price, volume)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(stock_symbol, timestamp)
                    DO UPDATE SET price = ?, volume = ?
                ''', (stock['stock_symbol'], current_10s, new_price, random.randint(100000, 1000000),
                      new_price, random.randint(100000, 1000000)))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"⚠️  价格更新错误: {e}")

        # 每5秒更新一次
        time.sleep(5)


if __name__ == '__main__':
    print("🚀 Flask API Server starting...")
    print("📍 API endpoint: http://localhost:5001")

    # 启动后台价格更新线程
    price_updater = threading.Thread(target=auto_update_prices, daemon=True)
    price_updater.start()
    print("✅ 自动股价更新线程已启动")

    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
