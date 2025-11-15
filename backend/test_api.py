"""
Quick API Testing Script
Test all API endpoints without browser
"""

import requests
import json

API_BASE = 'http://localhost:5001/api'

def test_health():
    """Test API health"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f'{API_BASE}/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n=== Testing Registration ===")
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': '123456'
    }
    response = requests.post(f'{API_BASE}/auth/register', json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code in [201, 400]  # 201 = success, 400 = already exists

def test_login():
    """Test user login"""
    print("\n=== Testing Login ===")
    data = {
        'username': 'testuser',
        'password': '123456'
    }
    response = requests.post(f'{API_BASE}/auth/login', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}")

    if response.status_code == 200:
        return result['user']['id']
    return None

def test_add_stocks(user_id):
    """Test adding stocks to watchlist"""
    print("\n=== Testing Add Stocks ===")
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'DIS']

    for symbol in stocks:
        data = {
            'user_id': user_id,
            'stock_symbol': symbol
        }
        response = requests.post(f'{API_BASE}/watchlist', json=data)
        print(f"{symbol}: {response.status_code} - {response.json()}")

def test_get_watchlist(user_id):
    """Test getting watchlist"""
    print("\n=== Testing Get Watchlist ===")
    response = requests.get(f'{API_BASE}/watchlist/{user_id}')
    print(f"Status: {response.status_code}")
    stocks = response.json()
    print(f"Stocks in watchlist: {len(stocks)}")
    for stock in stocks:
        print(f"  - {stock['stock_symbol']}: ${stock.get('current_price', 'N/A')}")

def main():
    print("=" * 50)
    print("Stock Watch API Testing")
    print("=" * 50)

    # Test 1: Health check
    if not test_health():
        print("\n❌ API is not running!")
        return

    # Test 2: Register
    test_register()

    # Test 3: Login
    user_id = test_login()
    if not user_id:
        print("\n❌ Login failed!")
        return

    print(f"\n✅ Logged in as user ID: {user_id}")

    # Test 4: Add stocks
    test_add_stocks(user_id)

    # Test 5: Get watchlist
    test_get_watchlist(user_id)

    print("\n" + "=" * 50)
    print("✅ All API tests completed!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Run: python fetch_stock_data.py")
    print("2. Open browser: http://localhost:8080")
    print("3. Login with: testuser / 123456")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API!")
        print("Make sure backend is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
