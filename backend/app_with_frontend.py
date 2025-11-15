"""
Stock Watch & Alert Web App - Backend API with Frontend
Flask API + Static Frontend (All-in-one deployment)
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime
import secrets
import os

app = Flask(__name__,
            static_folder='../frontend',  # Point to frontend folder
            template_folder='../frontend')  # Point to frontend folder

app.config['SECRET_KEY'] = secrets.token_hex(16)

CORS(app, supports_credentials=True)

def get_db():
    """Database connection helper"""
    conn = sqlite3.connect('stock_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== Frontend Routes ====================

@app.route('/')
def index():
    """Serve login page"""
    return render_template('index.html')

@app.route('/register')
def register_page():
    """Serve register page"""
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Serve dashboard page"""
    return render_template('dashboard.html')

@app.route('/watchlist')
def watchlist_page():
    """Serve watchlist page"""
    return render_template('watchlist.html')

@app.route('/stock-detail')
def stock_detail_page():
    """Serve stock detail page"""
    return render_template('stock-detail.html')

@app.route('/alerts')
def alerts_page():
    """Serve alerts page"""
    return render_template('alerts.html')

# Serve static files (CSS, JS)
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

# ==================== Authentication API ====================

@app.route('/api/auth/register', methods=['POST'])
def register_api():
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
def login_api():
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
    """Get stock history for charts"""
    days = request.args.get('days', 30, type=int)

    conn = get_db()
    history = conn.execute('''
        SELECT date, close_price, volume
        FROM stock_history
        WHERE stock_symbol = ?
        ORDER BY date DESC
        LIMIT ?
    ''', (symbol.upper(), days)).fetchall()
    conn.close()

    history = list(reversed([dict(row) for row in history]))
    return jsonify(history), 200


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

    top_stocks = conn.execute('''
        SELECT w.stock_symbol, s.stock_name, s.current_price, s.change_percent
        FROM watchlist w
        LEFT JOIN stock_data s ON w.stock_symbol = s.stock_symbol
        WHERE w.user_id = ?
        ORDER BY w.added_at DESC
        LIMIT 5
    ''', (user_id,)).fetchall()

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


@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Stock Watch API is running',
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    print("🚀 Flask Server starting (Frontend + API)...")
    print("📍 Frontend: http://localhost:5000")
    print("📍 API: http://localhost:5000/api")
    app.run(debug=True, host='0.0.0.0', port=5000)
