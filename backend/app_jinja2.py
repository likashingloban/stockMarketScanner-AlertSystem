"""
Stock Watch & Alert Web App - Jinja2 Version
Flask Web Application with Server-Side Rendering
"""

from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import secrets
import threading
import time
import random
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

def get_db():
    """Database connection helper"""
    conn = sqlite3.connect('stock_app.db')
    conn.row_factory = sqlite3.Row
    return conn


# ==================== Decorators ====================

def login_required(f):
    """装饰器：要求用户登录"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== Context Processor ====================

@app.context_processor
def inject_user():
    """向所有模板注入当前用户信息"""
    if 'user_id' in session:
        conn = get_db()
        user = conn.execute('SELECT id, username, email FROM users WHERE id = ?',
                           (session['user_id'],)).fetchone()
        conn.close()
        if user:
            return {'current_user': dict(user)}
    return {'current_user': None}


# ==================== Authentication Routes ====================

@app.route('/')
def index():
    """首页 - 如果已登录则跳转到dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if not user:
            flash('User not found', 'danger')
            return render_template('login.html')

        if not check_password_hash(user['password_hash'], password):
            flash('Invalid password', 'danger')
            return render_template('login.html')

        # 登录成功，保存session
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash(f'Welcome back, {user["username"]}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """注册页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # 验证密码
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        password_hash = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists', 'danger')
            return render_template('register.html')
        finally:
            conn.close()

    return render_template('register.html')


@app.route('/logout')
def logout():
    """退出登录"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('login'))


# ==================== Dashboard Routes ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """仪表板"""
    user_id = session['user_id']
    conn = get_db()

    # 获取用户的关注股票
    watchlist = conn.execute('''
        SELECT w.id, w.stock_symbol, s.stock_name, s.current_price, s.change_percent
        FROM watchlist w
        LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
        WHERE w.user_id = ?
        ORDER BY w.added_at DESC
        LIMIT 5
    ''', (user_id,)).fetchall()

    # 获取活跃的警报数量
    alert_count = conn.execute('''
        SELECT COUNT(*) as count
        FROM alerts
        WHERE user_id = ? AND is_active = 1 AND is_triggered = 0
    ''', (user_id,)).fetchone()

    # 获取所有股票
    all_stocks = conn.execute('''
        SELECT stock_symbol, stock_name, current_price, change_percent
        FROM stock_data
        ORDER BY stock_symbol ASC
    ''').fetchall()

    conn.close()

    return render_template('dashboard.html',
                         watchlist=[dict(row) for row in watchlist],
                         alert_count=alert_count['count'],
                         all_stocks=[dict(row) for row in all_stocks])


# ==================== Watchlist Routes ====================

@app.route('/watchlist')
@login_required
def watchlist():
    """关注列表页面"""
    user_id = session['user_id']
    conn = get_db()

    stocks = conn.execute('''
        SELECT w.id, w.stock_symbol, s.stock_name, s.current_price,
               s.change_amount, s.change_percent, s.updated_at
        FROM watchlist w
        LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
        WHERE w.user_id = ?
        ORDER BY w.added_at DESC
    ''', (user_id,)).fetchall()

    # 获取所有可用的股票
    all_stocks = conn.execute('''
        SELECT stock_symbol, stock_name
        FROM stock_data
        ORDER BY stock_symbol ASC
    ''').fetchall()

    conn.close()

    return render_template('watchlist.html',
                         stocks=[dict(row) for row in stocks],
                         all_stocks=[dict(row) for row in all_stocks])


@app.route('/watchlist/add', methods=['POST'])
@login_required
def add_to_watchlist():
    """添加到关注列表"""
    user_id = session['user_id']
    stock_symbol = request.form.get('stock_symbol', '').upper()

    if not stock_symbol:
        flash('Please select a stock', 'warning')
        return redirect(url_for('watchlist'))

    conn = get_db()
    try:
        conn.execute('INSERT INTO watchlist (user_id, stock_symbol) VALUES (?, ?)',
                    (user_id, stock_symbol))
        conn.commit()
        flash(f'{stock_symbol} added to watchlist', 'success')
    except sqlite3.IntegrityError:
        flash('Stock already in watchlist', 'warning')
    finally:
        conn.close()

    return redirect(url_for('watchlist'))


@app.route('/watchlist/remove/<int:watchlist_id>', methods=['POST'])
@login_required
def remove_from_watchlist(watchlist_id):
    """从关注列表删除"""
    conn = get_db()
    conn.execute('DELETE FROM watchlist WHERE id = ? AND user_id = ?',
                (watchlist_id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Removed from watchlist', 'info')
    return redirect(url_for('watchlist'))


# ==================== Alerts Routes ====================

@app.route('/alerts')
@login_required
def alerts():
    """警报页面"""
    user_id = session['user_id']
    conn = get_db()

    # 获取用户的所有警报
    user_alerts = conn.execute('''
        SELECT a.*, s.stock_name, s.current_price
        FROM alerts a
        LEFT JOIN stock_data s ON a.stock_symbol = s.stock_symbol
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
    ''', (user_id,)).fetchall()

    # 获取所有可用的股票
    all_stocks = conn.execute('''
        SELECT stock_symbol, stock_name, current_price
        FROM stock_data
        ORDER BY stock_symbol ASC
    ''').fetchall()

    conn.close()

    return render_template('alerts.html',
                         alerts=[dict(row) for row in user_alerts],
                         all_stocks=[dict(row) for row in all_stocks])


@app.route('/alerts/add', methods=['POST'])
@login_required
def add_alert():
    """添加警报"""
    user_id = session['user_id']
    stock_symbol = request.form.get('stock_symbol', '').upper()
    condition = request.form.get('condition')
    target_price = request.form.get('target_price', type=float)

    if not all([stock_symbol, condition, target_price]):
        flash('All fields are required', 'warning')
        return redirect(url_for('alerts'))

    if condition not in ['above', 'below']:
        flash('Invalid condition', 'danger')
        return redirect(url_for('alerts'))

    conn = get_db()
    conn.execute(
        'INSERT INTO alerts (user_id, stock_symbol, condition, target_price) VALUES (?, ?, ?, ?)',
        (user_id, stock_symbol, condition, target_price)
    )
    conn.commit()
    conn.close()

    flash('Alert created successfully', 'success')
    return redirect(url_for('alerts'))


@app.route('/alerts/delete/<int:alert_id>', methods=['POST'])
@login_required
def delete_alert(alert_id):
    """删除警报"""
    conn = get_db()
    conn.execute('DELETE FROM alerts WHERE id = ? AND user_id = ?',
                (alert_id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Alert deleted', 'info')
    return redirect(url_for('alerts'))


# ==================== Stock Detail Routes ====================

@app.route('/stock/<symbol>')
@login_required
def stock_detail(symbol):
    """股票详情页面"""
    conn = get_db()
    stock = conn.execute('SELECT * FROM stock_data WHERE stock_symbol = ?',
                        (symbol.upper(),)).fetchone()

    if not stock:
        conn.close()
        flash('Stock not found', 'danger')
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('stock-detail.html', stock=dict(stock))


# ==================== Settings Routes ====================

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """设置页面"""
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return render_template('settings.html')

        user_id = session['user_id']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

        if not check_password_hash(user['password_hash'], old_password):
            conn.close()
            flash('Current password is incorrect', 'danger')
            return render_template('settings.html')

        # 更新密码
        new_password_hash = generate_password_hash(new_password)
        conn.execute('UPDATE users SET password_hash = ? WHERE id = ?',
                    (new_password_hash, user_id))
        conn.commit()
        conn.close()

        flash('Password changed successfully', 'success')
        return redirect(url_for('settings'))

    return render_template('settings.html')


# ==================== API Endpoints (for AJAX) ====================

@app.route('/api/stock/<symbol>/history')
@login_required
def api_stock_history(symbol):
    """获取股票历史数据（用于图表）"""
    from datetime import timedelta

    time_range = request.args.get('range', '1h', type=str)
    conn = get_db()
    symbol = symbol.upper()

    if time_range == '1h':
        cutoff_time = datetime.now() - timedelta(hours=1)
        history = conn.execute('''
            SELECT strftime('%H:%M:%S', timestamp) as time, price, volume
            FROM stock_history_second
            WHERE stock_symbol = ? AND timestamp >= ?
            ORDER BY timestamp ASC
        ''', (symbol, cutoff_time)).fetchall()

    elif time_range == '24h':
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
    return jsonify([dict(row) for row in history]), 200


# ==================== Auto Stock Price Updater ====================

def auto_update_prices():
    """后台线程：自动更新股价（每5秒）"""
    print("📊 自动股价更新已启动（每5秒更新一次）")

    while True:
        try:
            conn = get_db()
            current_time = datetime.now()
            current_date = current_time.date()

            stocks = conn.execute('SELECT * FROM stock_data').fetchall()

            for stock in stocks:
                change_percent = random.uniform(-0.5, 0.5)
                current_price = stock['current_price']
                new_price = current_price * (1 + change_percent / 100)

                previous_close = stock['previous_close']
                change_amount = new_price - previous_close
                total_change_percent = (change_amount / previous_close) * 100 if previous_close else 0

                conn.execute('''
                    UPDATE stock_data
                    SET current_price = ?,
                        change_amount = ?,
                        change_percent = ?,
                        updated_at = ?
                    WHERE stock_symbol = ?
                ''', (new_price, change_amount, total_change_percent, current_time, stock['stock_symbol']))

                conn.execute('''
                    INSERT INTO stock_history (stock_symbol, date, close_price, volume)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(stock_symbol, date)
                    DO UPDATE SET close_price = ?, volume = ?
                ''', (stock['stock_symbol'], current_date, new_price, random.randint(1000000, 10000000),
                      new_price, random.randint(1000000, 10000000)))

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

        time.sleep(5)


if __name__ == '__main__':
    print("🚀 Flask Jinja2 Web App starting...")
    print("📍 URL: http://localhost:5001")

    # 启动后台价格更新线程
    price_updater = threading.Thread(target=auto_update_prices, daemon=True)
    price_updater.start()
    print("✅ 自动股价更新线程已启动")

    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
